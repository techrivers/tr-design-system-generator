"""Web interface for the Design System Generator."""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from datetime import datetime
from pathlib import Path

from main import DesignSystemGenerator
from typing import Optional, List
from models import DesignSystemInput, TargetUser, BrandTrait, Platform

app = FastAPI(title="Design System Generator", description="AI-powered autonomous design system creation")

# Mount static files and templates
# In Vercel, static files are served via routes, so we only mount if directory exists
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Initialize the generator
generator = DesignSystemGenerator()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate_design_system(
    product_idea: str = Form(...),
    target_users: Optional[List[str]] = Form(default=None),
    brand_traits: Optional[List[str]] = Form(default=None),
    platforms: Optional[List[str]] = Form(default=None)
):
    """Generate a design system based on user input."""

    try:
        # Convert string inputs to enums if provided (None or empty lists become None)
        input_data = DesignSystemInput(
            product_idea=product_idea,
            target_users=[TargetUser(user) for user in target_users] if target_users and len(target_users) > 0 else None,
            brand_traits=[BrandTrait(trait) for trait in brand_traits] if brand_traits and len(brand_traits) > 0 else None,
            platforms=[Platform(platform) for platform in platforms] if platforms and len(platforms) > 0 else None
        )

        # Generate the design system
        result = generator.generate_design_system(input_data)

        # Save to file (only if filesystem is writable, e.g., not in serverless)
        output_file = None
        try:
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            output_file = f"generated/design-system-{timestamp}.json"
            Path("generated").mkdir(exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(result.model_dump(), f, indent=2)
        except (PermissionError, OSError):
            # Filesystem is read-only (e.g., Vercel serverless)
            output_file = None

        # Extract agent reasoning for display
        reasoning_info = {}
        if result.principles.reasoning:
            reasoning_info["design_strategist"] = {
                "reasoning": result.principles.reasoning.reasoning,
                "confidence": {
                    "users": result.principles.reasoning.confidence.users,
                    "traits": result.principles.reasoning.confidence.traits,
                    "platforms": result.principles.reasoning.confidence.platforms
                },
                "overrides": result.principles.reasoning.overrides or []
            }
        
        if result.tokens.color_rationale:
            reasoning_info["visual_identity"] = {
                "color_rationale": result.tokens.color_rationale.overall
            }
        
        if result.components.reasoning:
            reasoning_info["component_architect"] = {
                "reasoning": result.components.reasoning
            }
        
        return JSONResponse({
            "success": True,
            "message": "Design system generated successfully!",
            "output_file": output_file,
            "data": result.model_dump(),
            "reasoning": reasoning_info,
            "validation": {
                k: {
                    "valid": v.valid,
                    "score": v.score,
                    "issues": v.issues,
                    "warnings": v.warnings
                }
                for k, v in (result.validation or {}).items()
            } if result.validation else None
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/editor", response_class=HTMLResponse)
async def editor(request: Request):
    """Visual design token editor page."""
    return templates.TemplateResponse("editor.html", {"request": request})


@app.get("/api/tokens/{file_id}")
async def get_tokens(file_id: str):
    """Load design tokens from a generated file."""
    try:
        # Try to find the file
        file_path = Path(f"generated/design-system-{file_id}.json")
        if not file_path.exists():
            # Try without prefix
            file_path = Path(f"generated/{file_id}.json")
        if not file_path.exists():
            # Try in root
            file_path = Path(f"{file_id}.json")
        
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Extract tokens
            tokens = {
                "colors": data.get("tokens", {}).get("colors", []),
                "typography": data.get("tokens", {}).get("typography", []),
                "spacing": data.get("tokens", {}).get("spacing", []),
                "border_radius": data.get("tokens", {}).get("border_radius", {}),
                "shadows": data.get("tokens", {}).get("shadows", {})
            }
            return {"success": True, "tokens": tokens}
        else:
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Design system file not found"}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/playground", response_class=HTMLResponse)
async def playground(request: Request):
    """Component playground page."""
    return templates.TemplateResponse("playground.html", {"request": request})


@app.get("/roi-calculator", response_class=HTMLResponse)
async def roi_calculator(request: Request):
    """ROI calculator page."""
    return templates.TemplateResponse("roi-calculator.html", {"request": request})


@app.get("/api/playground/{component_name}")
async def get_component_code(component_name: str, file_id: Optional[str] = None):
    """Get component code for playground."""
    try:
        # Load design system if file_id provided
        design_system = None
        if file_id:
            file_path = Path(f"generated/design-system-{file_id}.json")
            if file_path.exists():
                with open(file_path, 'r') as f:
                    design_system = json.load(f)
        
        # Generate component code
        from templates.components.generator import ComponentGenerator
        if design_system:
            comp_gen = ComponentGenerator(design_system.get("tokens", {}))
        else:
            # Use default tokens
            from models import DesignTokens
            default_tokens = DesignTokens(colors=[], typography=[], spacing=[])
            comp_gen = ComponentGenerator(default_tokens)
        
        # Get component code (simplified - would need actual component spec)
        component_code = f"// {component_name} component code would be generated here"
        
        return {"success": True, "code": component_code, "component": component_name}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.post("/api/integrate")
async def integrate_project(
    framework: Optional[str] = Form(None),
    directory: Optional[str] = Form(None),
    file_id: Optional[str] = Form(None)
):
    """Integrate design system into existing project."""
    try:
        from cli.integrate import ProjectIntegrator
        from pathlib import Path
        
        project_dir = Path(directory or ".").resolve()
        integrator = ProjectIntegrator(project_dir)
        
        # Load design system if file_id provided
        design_system = None
        if file_id:
            file_path = Path(f"generated/design-system-{file_id}.json")
            if file_path.exists():
                with open(file_path, 'r') as f:
                    data = json.load(f)
                from models import DesignSystemOutput
                design_system = DesignSystemOutput(**data)
        
        if not design_system:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Design system file not found"}
            )
        
        results = integrator.integrate(
            design_system,
            auto_install=False,
            explicit_framework=framework
        )
        
        return JSONResponse({
            "success": len(results.get("errors", [])) == 0,
            "results": results
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/api/roi")
async def calculate_roi(
    team_size: int = 5,
    dev_rate: float = 100,
    designer_rate: float = 80,
    timeline: int = 6,
    ds_creation: int = 80,
    component_dev: int = 200,
    documentation: int = 40
):
    """Calculate ROI for design system generator."""
    try:
        # Traditional approach costs
        traditional_ds = ds_creation * designer_rate
        traditional_components = component_dev * dev_rate
        traditional_docs = documentation * (designer_rate * 0.5 + dev_rate * 0.5)
        traditional_total = traditional_ds + traditional_components + traditional_docs
        
        # With design system generator
        generated_ds = (ds_creation * 0.1) * designer_rate
        generated_components = (component_dev * 0.2) * dev_rate
        generated_docs = (documentation * 0.1) * (designer_rate * 0.5 + dev_rate * 0.5)
        generated_total = generated_ds + generated_components + generated_docs
        
        cost_savings = traditional_total - generated_total
        time_savings = (ds_creation + component_dev + documentation) * 0.8
        roi = (cost_savings / generated_total * 100) if generated_total > 0 else 0
        
        return JSONResponse({
            "success": True,
            "traditional": {
                "cost": traditional_total,
                "time": ds_creation + component_dev + documentation
            },
            "generated": {
                "cost": generated_total,
                "time": (ds_creation * 0.1) + (component_dev * 0.2) + (documentation * 0.1)
            },
            "savings": {
                "cost": cost_savings,
                "time": time_savings,
                "roi_percent": round(roi, 2)
            }
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
