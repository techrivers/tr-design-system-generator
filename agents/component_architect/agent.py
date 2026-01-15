"""Component Architect Agent - Defines component inventory and specifications with enhanced autonomy."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import DesignPrinciples, ComponentInventory, ComponentSpec
import json
from litellm import completion
from dotenv import load_dotenv
from agents.knowledge_base import KnowledgeBase
from agents.prompts import PromptTemplates

load_dotenv()

class ComponentArchitectAgent:
    """Agent that defines the complete component inventory and their specifications."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        # Auto-detect model based on API key if MODEL_NAME not explicitly set
        if os.getenv("MODEL_NAME"):
            self.model = os.getenv("MODEL_NAME")
        elif os.getenv("GEMINI_API_KEY"):
            self.model = "gemini/gemini-1.5-pro-latest"
        elif os.getenv("OPENAI_API_KEY"):
            self.model = "gpt-5"  # Best for complex reasoning and structured JSON output
        elif os.getenv("ANTHROPIC_API_KEY"):
            self.model = "claude-3-5-sonnet-20241022"
        else:
            self.model = "gemini/gemini-1.5-pro-latest"  # fallback default

    def generate_component_inventory(self, principles: DesignPrinciples, product_context: str) -> ComponentInventory:
        """
        Generate a complete component inventory based on design principles and product context.
        """
        industry = principles.industry_context.industry if principles.industry_context else "unknown"
        
        # Base component inventory that every system needs
        base_components = [
            ComponentSpec(
                name="Button",
                category="button",
                variants=["primary", "secondary", "tertiary", "danger"],
                states=["default", "hover", "focus", "disabled", "loading"],
                description="Primary action component",
                accessibility_notes="Must meet WCAG 2.1 AA, keyboard navigable, focus indicators"
            ),
            ComponentSpec(
                name="Input",
                category="input",
                variants=["text", "email", "password", "number"],
                states=["default", "focus", "error", "disabled"],
                description="Text input component",
                accessibility_notes="Include labels, error messages, ARIA attributes"
            ),
            ComponentSpec(
                name="Select",
                category="input",
                variants=["default", "multi"],
                states=["default", "focus", "error", "disabled"],
                description="Dropdown selection component",
                accessibility_notes="Keyboard navigable, screen reader support"
            ),
            ComponentSpec(
                name="Modal",
                category="feedback",
                variants=["default", "large", "small"],
                states=["default", "open", "closing"],
                description="Overlay dialog component",
                accessibility_notes="Focus trap, ESC to close, ARIA modal attributes"
            ),
            ComponentSpec(
                name="Alert",
                category="feedback",
                variants=["success", "error", "warning", "info"],
                states=["default", "dismissible"],
                description="Notification component",
                accessibility_notes="ARIA live regions, role=alert"
            ),
            ComponentSpec(
                name="Card",
                category="layout",
                variants=["default", "elevated", "outlined"],
                states=["default", "hover", "interactive"],
                description="Container component",
                accessibility_notes="Semantic HTML, proper heading hierarchy"
            ),
            ComponentSpec(
                name="Table",
                category="data",
                variants=["default", "striped", "bordered"],
                states=["default", "loading", "empty"],
                description="Data table component",
                accessibility_notes="Table headers, keyboard navigation, screen reader support"
            ),
            ComponentSpec(
                name="Navigation",
                category="navigation",
                variants=["horizontal", "vertical"],
                states=["default", "active", "hover"],
                description="Navigation component",
                accessibility_notes="ARIA nav, keyboard navigation, current page indication"
            ),
        ]

        # Get industry-specific components
        industry_components = KnowledgeBase.get_components_for_industry(industry)
        
        # Add specialized components based on industry and AI analysis
        additional_components = []
        component_variants = {}
        component_states = {}
        reasoning = ""
        
        if self.api_key:
            try:
                prompt = PromptTemplates.component_architect_prompt(principles, product_context, industry, base_components)
                
                response = completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                
                data = json.loads(response.choices[0].message.content)
                additional_components = data.get("additional_components", [])
                component_variants = data.get("component_variants", {})
                component_states = data.get("component_states", {})
                reasoning = data.get("reasoning", "")
            except Exception as e:
                print(f"AI Component selection failed, falling back to rules: {e}")
        
        # Fallback: Use industry knowledge base
        if not additional_components:
            # Get components from knowledge base that aren't in base set
            for comp_name in industry_components:
                if comp_name not in [c.name for c in base_components]:
                    additional_components.append(comp_name)
        
        # Add specialized components
        specialized_components = []
        for comp_name in additional_components:
            # Check if component already exists
            if any(c.name == comp_name for c in base_components):
                continue
            
            # Determine category
            category = "contextual"
            if comp_name in ["Hero", "Header", "Footer", "Sidebar"]:
                category = "layout"
            elif comp_name in ["DataTable", "DashboardStat", "PricingTable"]:
                category = "data"
            elif comp_name in ["Pagination", "Breadcrumb", "Tabs"]:
                category = "navigation"
            elif comp_name in ["Progress", "Skeleton", "Accordion"]:
                category = "feedback"
            
            # Get variants and states from AI or use defaults
            variants = component_variants.get(comp_name, ["default"])
            states = component_states.get(comp_name, ["default"])
            
            # Enhance with common variants/states based on component type
            if comp_name == "Hero":
                variants = ["default", "centered", "split"]
                states = ["default"]
            elif comp_name == "DataTable":
                variants = ["default", "sortable", "filterable"]
                states = ["default", "loading", "empty"]
            elif comp_name == "Pagination":
                variants = ["default", "compact"]
                states = ["default", "disabled"]
            elif comp_name == "Tabs":
                variants = ["default", "pills", "underline"]
                states = ["default", "active", "disabled"]
            elif comp_name == "Progress":
                variants = ["default", "circular", "linear"]
                states = ["default", "indeterminate"]
            
            specialized_components.append(ComponentSpec(
                name=comp_name,
                category=category,
                variants=variants,
                states=states,
                description=f"Specialized {comp_name} component for {industry} products",
                accessibility_notes="Context-specific semantic markup and ARIA attributes"
            ))
        
        # Add component dependencies
        all_component_names = [c.name for c in base_components + specialized_components]
        for component in base_components + specialized_components:
            dependencies = KnowledgeBase.get_component_dependencies(component.name)
            for dep in dependencies:
                if dep not in all_component_names:
                    # Add missing dependency
                    specialized_components.append(ComponentSpec(
                        name=dep,
                        category="contextual",
                        variants=["default"],
                        states=["default"],
                        description=f"Required dependency for {component.name}",
                        accessibility_notes="Standard accessibility requirements"
                    ))
                    all_component_names.append(dep)
        
        # Combine all components
        all_components = base_components + specialized_components
        
        # Categorize components
        reusable_components = ["Button", "Input", "Select", "Modal", "Alert", "Card", "Badge", "Tooltip", "Container", "Stack", "Grid"]
        contextual_components = [c.name for c in all_components if c.name not in reusable_components]
        
        # Generate reasoning if not provided
        if not reasoning:
            reasoning = f"Component inventory generated for {industry} industry. Base components provide core functionality, while specialized components ({', '.join([c.name for c in specialized_components])}) address specific needs of {product_context}."
        
        return ComponentInventory(
            components=all_components,
            reusable_components=reusable_components,
            contextual_components=contextual_components,
            reasoning=reasoning
        )
