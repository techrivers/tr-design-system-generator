"""Design Strategist Agent - The core decision-making engine with enhanced autonomy."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import DesignSystemInput, DesignPrinciples, AgentReasoning, ConfidenceScore, IndustryContext
import json
from litellm import completion
from dotenv import load_dotenv
from agents.knowledge_base import KnowledgeBase
from agents.prompts import PromptTemplates

load_dotenv()

class DesignStrategistAgent:
    """Agent that defines design principles and system philosophy based on product requirements."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        self.model = os.getenv("MODEL_NAME", "gemini/gemini-1.5-pro-latest")

    def analyze_product_requirements(self, input_data: DesignSystemInput) -> DesignPrinciples:
        """
        Analyze the product requirements and generate design principles with enhanced reasoning.
        """
        # Step 1: Detect industry from product description
        industry = KnowledgeBase.detect_industry(input_data.product_idea)
        
        # Step 2: Get industry context
        industry_context = {
            "philosophy": KnowledgeBase.get_philosophy_for_industry(industry),
            "density": KnowledgeBase.get_density_for_industry(industry),
            "warmth": KnowledgeBase.get_warmth_for_industry(industry),
            "clarity": KnowledgeBase.get_clarity_for_industry(industry),
            "speed": KnowledgeBase.get_speed_for_industry(industry)
        }
        
        # Step 3: Check for trait conflicts
        user_traits = [t.value for t in input_data.brand_traits] if input_data.brand_traits else []
        trait_conflicts = KnowledgeBase.check_trait_conflicts(user_traits)
        
        # Step 4: Use AI with enhanced prompt if available
        if self.api_key:
            try:
                prompt = PromptTemplates.design_strategist_prompt(input_data, industry, industry_context)
                
                response = completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                
                data = json.loads(response.choices[0].message.content)
                
                # Extract reasoning if provided
                reasoning = None
                if "reasoning" in data or "confidence" in data or "overrides" in data:
                    confidence_data = data.get("confidence", {})
                    reasoning = AgentReasoning(
                        reasoning=data.get("reasoning", "Design principles derived from product analysis and industry standards."),
                        confidence=ConfidenceScore(
                            users=confidence_data.get("users", 0.8),
                            traits=confidence_data.get("traits", 0.8),
                            platforms=confidence_data.get("platforms", 0.8)
                        ),
                        overrides=data.get("overrides", [])
                    )
                
                # Create industry context object
                industry_context_obj = IndustryContext(
                    industry=industry,
                    **industry_context
                )
                
                # Override user inputs if they conflict with industry standards
                inferred_users = data.get("inferred_users", [])
                inferred_traits = data.get("inferred_traits", [])
                inferred_platforms = data.get("inferred_platforms", [])
                
                # If user provided values, validate them
                final_users = inferred_users
                if input_data.target_users:
                    # Check if user inputs make sense - if not, use inferred
                    user_provided = [u.value for u in input_data.target_users]
                    # For now, prefer inferred if they're more specific
                    if len(inferred_users) > 0:
                        final_users = inferred_users
                    else:
                        final_users = user_provided
                
                final_traits = inferred_traits
                if input_data.brand_traits:
                    user_provided_traits = [t.value for t in input_data.brand_traits]
                    # Override if conflicts detected
                    if trait_conflicts:
                        # Use inferred traits if user traits conflict
                        if len(inferred_traits) > 0:
                            final_traits = inferred_traits
                        else:
                            # Remove conflicting traits
                            final_traits = [t for t in user_provided_traits if not any(cf in t for cf in trait_conflicts)]
                    else:
                        final_traits = user_provided_traits if len(inferred_traits) == 0 else inferred_traits
                
                final_platforms = inferred_platforms
                if input_data.platforms:
                    user_provided_platforms = [p.value for p in input_data.platforms]
                    final_platforms = inferred_platforms if len(inferred_platforms) > 0 else user_provided_platforms
                
                return DesignPrinciples(
                    clarity=data.get("clarity", industry_context["clarity"]),
                    density=data.get("density", industry_context["density"]),
                    warmth=data.get("warmth", industry_context["warmth"]),
                    speed=data.get("speed", industry_context["speed"]),
                    philosophy=data.get("philosophy", industry_context["philosophy"]),
                    inferred_users=final_users,
                    inferred_traits=final_traits,
                    inferred_platforms=final_platforms,
                    reasoning=reasoning,
                    industry_context=industry_context_obj
                )
            except Exception as e:
                print(f"AI Strategy failed, falling back to rules: {e}")

        # Fallback to rule-based logic with industry context
        traits = [t.value for t in input_data.brand_traits] if input_data.brand_traits else []
        users = [u.value for u in input_data.target_users] if input_data.target_users else []
        
        # Use industry defaults if no user input
        if not users:
            # Infer from industry
            if industry == "healthcare" or industry == "finance":
                users = ["enterprise", "B2B"]
            elif industry == "ecommerce" or industry == "consumer":
                users = ["consumer", "B2C"]
            elif industry == "saas" or industry == "dashboard":
                users = ["B2B"]
            else:
                users = ["B2B"]
        
        if not traits:
            # Infer from industry
            if industry in ["healthcare", "finance", "enterprise"]:
                traits = ["professional", "minimal"]
            elif industry in ["ecommerce", "consumer", "marketing"]:
                traits = ["modern", "bold"]
            else:
                traits = ["modern", "professional"]
        
        # Override conflicting traits
        trait_conflicts = KnowledgeBase.check_trait_conflicts(traits)
        if trait_conflicts:
            # Remove conflicting traits, prefer industry-appropriate ones
            if industry in ["healthcare", "finance"]:
                traits = [t for t in traits if t not in ["playful", "bold"]]
                if "professional" not in traits:
                    traits.append("professional")
            elif industry in ["marketing", "consumer"]:
                traits = [t for t in traits if t not in ["clinical", "minimal"]]
        
        # Determine principles
        is_enterprise = "enterprise" in users or "B2B" in users
        is_playful = "playful" in traits
        is_bold = "bold" in traits
        
        # Use industry context as base, adjust based on user input
        philosophy = industry_context["philosophy"]
        density = industry_context["density"]
        clarity = industry_context["clarity"]
        warmth = industry_context["warmth"]
        speed = industry_context["speed"]
        
        # Override if user input strongly suggests different approach
        if is_playful and industry not in ["healthcare", "finance"]:
            philosophy = "brand-led"
            warmth = min(9, warmth + 2)
        elif is_bold and industry not in ["healthcare", "finance"]:
            philosophy = "brand-led"
            warmth = min(9, warmth + 1)
        
        # Create reasoning
        reasoning = AgentReasoning(
            reasoning=f"Design principles derived from industry analysis ({industry}) and product requirements. Industry standards applied with adjustments for user-provided preferences.",
            confidence=ConfidenceScore(
                users=0.7 if users else 0.5,
                traits=0.7 if traits else 0.5,
                platforms=0.6
            ),
            overrides=trait_conflicts if trait_conflicts else None
        )
        
        industry_context_obj = IndustryContext(
            industry=industry,
            **industry_context
        )
        
        return DesignPrinciples(
            clarity=clarity,
            density=density,
            warmth=warmth,
            speed=speed,
            philosophy=philosophy,
            inferred_users=users,
            inferred_traits=traits,
            inferred_platforms=[p.value for p in input_data.platforms] if input_data.platforms else ["web"],
            reasoning=reasoning,
            industry_context=industry_context_obj
        )
