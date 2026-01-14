"""Sophisticated prompts for agent reasoning with few-shot examples and chain-of-thought."""

from typing import Dict, Optional
from models import DesignSystemInput, DesignPrinciples


class PromptTemplates:
    """Centralized prompt templates with few-shot examples."""

    @staticmethod
    def design_strategist_prompt(input_data: DesignSystemInput, industry: str, industry_context: Dict) -> str:
        """Generate sophisticated prompt for Design Strategist with chain-of-thought reasoning."""
        
        users_provided = [u.value for u in input_data.target_users] if input_data.target_users else []
        traits_provided = [t.value for t in input_data.brand_traits] if input_data.brand_traits else []
        platforms_provided = [p.value for p in input_data.platforms] if input_data.platforms else []
        
        return f"""You are a senior Design Strategist with 15+ years of experience creating design systems for Fortune 500 companies and startups.

TASK: Analyze the product requirements and define core design principles that will guide the entire design system.

PRODUCT DESCRIPTION: {input_data.product_idea}
DETECTED INDUSTRY: {industry}
PROVIDED TARGET USERS: {users_provided if users_provided else "Not provided - you must infer"}
PROVIDED BRAND TRAITS: {traits_provided if traits_provided else "Not provided - you must infer"}
PROVIDED PLATFORMS: {platforms_provided if platforms_provided else "Not provided - you must infer"}

INDUSTRY CONTEXT:
- Typical philosophy: {industry_context.get('philosophy', 'component-first')}
- Typical density: {industry_context.get('density', 'balanced')}
- Typical warmth: {industry_context.get('warmth', 5)}/10
- Typical clarity: {industry_context.get('clarity', 8)}/10
- Typical speed: {industry_context.get('speed', 7)}/10

REASONING PROCESS:
1. First, analyze the product description to understand:
   - What problem does it solve?
   - Who are the primary users? (infer if not provided)
   - What is the primary use case? (data-heavy, transactional, informational, etc.)
   - What emotional tone should it convey?

2. Evaluate provided inputs against industry standards:
   - If user provided traits that conflict with industry norms (e.g., "playful" for healthcare), you should override them
   - If user provided users/platforms, validate they make sense for the product
   - Infer missing values based on product description and industry patterns

3. Determine design principles:
   - clarity (1-10): How critical is legibility? Healthcare/finance = 10, marketing = 7
   - density ("dense", "balanced", "spacious"): Data-heavy = dense, consumer = balanced, healthcare = spacious
   - warmth (1-10): Clinical = 3, consumer = 7, marketing = 8
   - speed (1-10): Dashboard = 9, marketing = 6, healthcare = 9
   - philosophy: Utility-first for data/enterprise, brand-led for consumer/marketing, component-first for SaaS

4. Generate confidence scores (0-1) for your inferences:
   - How confident are you in the inferred users?
   - How confident are you in the inferred traits?
   - How confident are you in the inferred platforms?

OUTPUT FORMAT (JSON only):
{{
  "clarity": <1-10>,
  "density": "<dense|balanced|spacious>",
  "warmth": <1-10>,
  "speed": <1-10>,
  "philosophy": "<utility-first|component-first|brand-led>",
  "inferred_users": ["<user_type>", ...],
  "inferred_traits": ["<trait>", ...],
  "inferred_platforms": ["<platform>", ...],
  "reasoning": "<2-3 sentence explanation of your decisions>",
  "confidence": {{
    "users": <0.0-1.0>,
    "traits": <0.0-1.0>,
    "platforms": <0.0-1.0>
  }},
  "overrides": ["<any user inputs you overrode and why>"]
}}

IMPORTANT:
- If user provided values conflict with industry best practices, override them and explain why
- Be specific in your reasoning - explain the "why" behind each decision
- Confidence scores should reflect how certain you are based on the product description
- Return ONLY valid JSON, no markdown, no explanations outside JSON"""

    @staticmethod
    def visual_identity_color_prompt(principles: DesignPrinciples, industry: str, industry_colors: Optional[Dict]) -> str:
        """Generate sophisticated prompt for color generation."""
        
        color_suggestion = ""
        if industry_colors:
            color_suggestion = f"""
INDUSTRY COLOR GUIDANCE:
- Suggested primary: {industry_colors.get('primary')}
- Suggested accent: {industry_colors.get('accent')}
- Rationale: {industry_colors.get('rationale')}

You may use these as inspiration but create a unique palette that fits the specific product context."""
        
        return f"""You are a senior UI/UX Designer specializing in color systems for digital products.

TASK: Generate a professional, accessible color palette that aligns with the design principles and product context.

DESIGN PRINCIPLES:
- Philosophy: {principles.philosophy}
- Warmth: {principles.warmth}/10 ({'warm' if principles.warmth >= 7 else 'cool' if principles.warmth <= 3 else 'neutral'})
- Density: {principles.density}
- Clarity: {principles.warmth}/10 (high clarity requires high contrast)

INDUSTRY: {industry}
{color_suggestion}

REASONING PROCESS:
1. Consider the warmth score:
   - Warmth 1-3: Cool colors (blues, grays) - professional, clinical
   - Warmth 4-6: Balanced colors (teals, purples) - modern, approachable
   - Warmth 7-10: Warm colors (oranges, reds, yellows) - energetic, friendly

2. Select primary color:
   - MUST be accessible from the start (WCAG AA contrast on white >= 4.5:1)
   - For 4.5:1 contrast on white, choose a DARKER shade (lightness typically 0.3-0.5)
   - Should align with industry standards but be unique
   - Consider the product's emotional goals
   - IMPORTANT: Choose a darker shade that naturally meets contrast, don't rely on post-processing adjustments

3. Select neutral/base color:
   - Should complement primary
   - Warm or cool based on warmth score
   - Must work for text, backgrounds, borders
   - Neutral-700 MUST be dark enough for body text (lightness ~0.25-0.35 for 4.5:1 on white)

4. Ensure accessibility (CRITICAL - Generate accessible colors from the start):
   - Primary-500: Choose a color with lightness between 0.3-0.5 to ensure 4.5:1+ contrast on white
   - Semantic colors: 
     * Success: Use darker green (lightness ~0.35-0.45)
     * Error: Use darker red (lightness ~0.40-0.50)
     * Warning: Use darker orange (lightness ~0.35-0.45)
     * Info: Use darker blue (lightness ~0.40-0.50)
   - Neutral-700: Use lightness ~0.25-0.35 for body text on white
   - Consider color blindness (avoid red-green only combinations)
   - Generate colors that are naturally accessible, not colors that need adjustment

OUTPUT FORMAT (JSON only):
{{
  "primary": "<hex_code>",
  "neutral": "<hex_code>",
  "accent": "<hex_code>",
  "rationale": "<2-3 sentence explanation of color choices and how they support the design principles>"
}}

IMPORTANT:
- Generate unique colors for this specific product (not generic palettes)
- Ensure all colors are accessible
- Explain how colors support the design principles
- Return ONLY valid JSON"""

    @staticmethod
    def component_architect_prompt(principles: DesignPrinciples, product_context: str, industry: str, base_components: list) -> str:
        """Generate sophisticated prompt for component selection."""
        
        return f"""You are a Design Systems Architect with expertise in component design and information architecture.

TASK: Determine the complete component inventory needed for this product, including specialized components beyond the base set.

PRODUCT CONTEXT: {product_context}
INDUSTRY: {industry}
DESIGN PHILOSOPHY: {principles.philosophy}
BASE COMPONENTS (already included): {', '.join([c.name for c in base_components])}

REASONING PROCESS:
1. Analyze the product context:
   - What are the primary user flows?
   - What data needs to be displayed? (tables, charts, cards)
   - What interactions are needed? (forms, navigation, modals)
   - What specialized features exist? (pricing, testimonials, dashboards)

2. Consider component dependencies:
   - If Table is needed, also include Pagination and Search
   - If Navigation exists, consider Header/Footer
   - If Dashboard context, include DataTable, DashboardStat, Skeleton
   - If Marketing context, include Hero, PricingTable, Testimonial

3. Select specialized components (3-7 additional):
   Available: Hero, PricingTable, Sidebar, Header, Footer, Testimonial, DataTable, DashboardStat, Breadcrumb, Tabs, Accordion, Progress, Skeleton, Avatar, DatePicker, Switch, Badge, Tooltip

4. For each component, determine:
   - Appropriate variants (e.g., Button: primary, secondary, tertiary, danger)
   - Necessary states (default, hover, focus, disabled, loading, error)
   - Accessibility requirements

OUTPUT FORMAT (JSON only):
{{
  "additional_components": ["<ComponentName>", ...],
  "component_variants": {{
    "<ComponentName>": ["<variant1>", "<variant2>", ...]
  }},
  "component_states": {{
    "<ComponentName>": ["<state1>", "<state2>", ...]
  }},
  "reasoning": "<2-3 sentence explanation of component choices>"
}}

IMPORTANT:
- Select components that match the product's actual needs
- Consider component dependencies
- Ensure completeness for the product type
- Return ONLY valid JSON"""

    @staticmethod
    def validation_prompt(agent_output: str, validation_type: str, context: Dict) -> str:
        """Generate prompt for validation."""
        
        if validation_type == "color_accessibility":
            return f"""Validate these colors for WCAG 2.1 AA accessibility:

PRIMARY COLOR: {context.get('primary')}
NEUTRAL COLOR: {context.get('neutral')}

Check:
1. Primary-500 on white background: contrast ratio >= 4.5:1
2. Primary-500 on neutral-50: contrast ratio >= 4.5:1
3. Neutral-700 on white: contrast ratio >= 4.5:1
4. All semantic colors (success, error, warning) meet contrast requirements

Return JSON with validation results and any issues found."""
        
        elif validation_type == "component_completeness":
            return f"""Validate component inventory for completeness:

PRODUCT TYPE: {context.get('product_type')}
INDUSTRY: {context.get('industry')}
COMPONENTS: {context.get('components')}

Check:
1. Are all necessary components for this product type included?
2. Are component dependencies satisfied?
3. Are there any missing critical components?

Return JSON with validation results."""
        
        return ""
