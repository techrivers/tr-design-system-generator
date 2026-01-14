import sys
import os
from models import DesignSystemInput, TargetUser, BrandTrait, Platform

# Mock DesignStrategistAgent
from agents.design_strategist.agent import DesignStrategistAgent
from agents.visual_identity.agent import VisualIdentityAgent
from agents.component_architect.agent import ComponentArchitectAgent

def test_agents():
    print("Testing Phase 3 AI Agents (with fallbacks)...")
    
    input_data = DesignSystemInput(
        product_idea="A premium dashboard for professional crypto traders.",
        target_users=[TargetUser.ENTERPRISE],
        brand_traits=[BrandTrait.MODERN, BrandTrait.PREMIUM],
        platforms=[Platform.DASHBOARD]
    )
    
    # 1. Test Strategist
    strategist = DesignStrategistAgent()
    print(f"Strategist Model: {strategist.model}")
    print(f"Strategist API Key Set: {bool(strategist.api_key)}")
    
    principles = strategist.analyze_product_requirements(input_data)
    print(f"Principles: {principles}")
    
    # 2. Test Visual Identity
    visual = VisualIdentityAgent()
    tokens = visual.generate_design_tokens(principles)
    print(f"Tokens Generated: {len(tokens.colors)} colors")
    
    # 3. Test Architect
    architect = ComponentArchitectAgent()
    inventory = architect.generate_component_inventory(principles, input_data.product_idea)
    print(f"Inventory: {[c.name for c in inventory.components]}")
    
    print("Verification Successful!")

if __name__ == "__main__":
    test_agents()
