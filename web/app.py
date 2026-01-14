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


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
