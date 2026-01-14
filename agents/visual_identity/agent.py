"""Visual Identity Agent - Generates design tokens and visual foundations with enhanced autonomy."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import DesignPrinciples, DesignTokens, ColorToken, TypographyToken, SpacingToken, ColorRationale
from typing import Optional, Tuple, List, Dict, Any
import colorsys
import json
import hashlib
from litellm import completion
from dotenv import load_dotenv
from agents.knowledge_base import KnowledgeBase
from agents.prompts import PromptTemplates
from agents.validator import Validator

load_dotenv()

class VisualIdentityAgent:
    """Agent that generates visual design tokens based on design principles."""

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

    def generate_color_system(self, principles: DesignPrinciples, product_idea: str = "") -> Tuple[List[ColorToken], Optional[ColorRationale], Optional[List[Dict[str, Any]]]]:
        """Generate a complete color system based on design principles with industry context."""
        industry = principles.industry_context.industry if principles.industry_context else "unknown"
        industry_colors = KnowledgeBase.get_industry_color_suggestions(industry)
        
        if self.api_key:
            try:
                prompt = PromptTemplates.visual_identity_color_prompt(principles, industry, industry_colors, product_idea)
                
                # Use higher temperature for more creative/diverse color generation
                response = completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.9  # Higher temperature for more variation
                )
                
                data = json.loads(response.choices[0].message.content)
                
                # Check for new format with recommendations
                recommendations_data = data.get('primary_recommendations')
                if recommendations_data and isinstance(recommendations_data, list) and len(recommendations_data) > 0:
                    # New format with multiple recommendations
                    primary_recommendations = []
                    for rec in recommendations_data[:3]:  # Take up to 3 recommendations
                        primary_hex = rec.get('primary')
                        secondary_hex = rec.get('secondary')
                        rationale = rec.get('rationale', '')
                        
                        if primary_hex and primary_hex.startswith('#') and secondary_hex and secondary_hex.startswith('#'):
                            primary_recommendations.append({
                                'primary': primary_hex,
                                'secondary': secondary_hex,
                                'rationale': rationale
                            })
                    
                    if not primary_recommendations:
                        raise ValueError("No valid recommendations found")
                    
                    # Use first recommendation as default
                    selected_rec = primary_recommendations[0]
                    primary_hex = selected_rec['primary']
                    secondary_hex = selected_rec['secondary']
                    neutral_hex = data.get('neutral')
                    accent_hex = data.get('accent', None)
                    overall_rationale = data.get('overall_rationale', '')
                    recommendation_rationales = [rec['rationale'] for rec in primary_recommendations]
                else:
                    # Legacy format - single primary (backward compatibility)
                    primary_hex = data.get('primary')
                    neutral_hex = data.get('neutral')
                    accent_hex = data.get('accent', None)
                    rationale_text = data.get('rationale', '')
                    secondary_hex = None
                    primary_recommendations = None
                    overall_rationale = rationale_text
                    recommendation_rationales = None
                
                # Validate hex format
                if not primary_hex or not primary_hex.startswith('#'):
                    raise ValueError("Invalid primary color format")
                if not neutral_hex or not neutral_hex.startswith('#'):
                    raise ValueError("Invalid neutral color format")
                
                # Add seed-based variation to AI-generated colors to ensure diversity
                if product_idea:
                    seed = int(hashlib.md5(product_idea.encode()).hexdigest()[:8], 16)
                    # Convert hex to HSL
                    r = int(primary_hex[1:3], 16) / 255
                    g = int(primary_hex[3:5], 16) / 255
                    b = int(primary_hex[5:7], 16) / 255
                    h, l, s = colorsys.rgb_to_hls(r, g, b)
                    
                    # Add seed-based variation to ensure different products get different colors
                    # Use different parts of the seed for different variations
                    hue_shift = ((seed % 30) + 10) / 360.0  # 10-40 degrees variation (more noticeable)
                    saturation_shift = ((seed % 11) - 5) / 100.0  # ±5% saturation variation
                    lightness_shift = ((seed % 7) - 3) / 100.0  # ±3% lightness variation
                    
                    varied_hue = (h + hue_shift) % 1.0
                    varied_saturation = max(0.3, min(0.9, s + saturation_shift))
                    varied_lightness = max(0.25, min(0.55, l + lightness_shift))
                    
                    primary_hex = self.hsl_to_hex(varied_hue, varied_saturation, varied_lightness)
                    print(f"🎨 Applied seed-based variation to AI color (seed: {seed % 1000})")
                
                # Check primary color contrast (AI should generate accessible colors from the start)
                contrast = Validator.get_contrast_ratio(primary_hex, "#FFFFFF")
                if contrast < 4.5:
                    # Only adjust if absolutely necessary (AI should have generated accessible color)
                    print(f"⚠️  WARNING: Primary color contrast {contrast:.2f} < 4.5. AI should generate accessible colors from the start.")
                    primary_hex = self.ensure_contrast(primary_hex, "#FFFFFF", min_contrast=4.5)
                    print(f"✅ Adjusted to {primary_hex} with contrast {Validator.get_contrast_ratio(primary_hex, '#FFFFFF'):.2f}")
                
                # Generate full color scales
                colors = self.generate_scale_from_hex(primary_hex, "primary")
                colors.extend(self.generate_scale_from_hex(neutral_hex, "neutral", saturation_mult=0.05))
                
                # Add secondary color scale if provided
                if secondary_hex and secondary_hex.startswith('#'):
                    # Ensure secondary color is accessible
                    contrast = Validator.get_contrast_ratio(secondary_hex, "#FFFFFF")
                    if contrast < 4.5:
                        secondary_hex = self.ensure_contrast(secondary_hex, "#FFFFFF", min_contrast=4.5)
                    colors.extend(self.generate_scale_from_hex(secondary_hex, "secondary"))
                
                # Add accent if provided
                if accent_hex and accent_hex.startswith('#'):
                    colors.extend(self.generate_scale_from_hex(accent_hex, "accent"))
                
                # Add semantic colors with accessibility in mind (WCAG AA compliant)
                colors.extend(self.generate_accessible_semantic_colors())
                
                # Create color rationale
                rationale = ColorRationale(
                    primary=overall_rationale or f"Primary color ({primary_hex}) selected to align with {industry} industry standards and design principles.",
                    neutral=overall_rationale or f"Neutral color ({neutral_hex}) chosen to complement primary and support {principles.density} density UI.",
                    accent=overall_rationale or f"Accent color ({accent_hex}) provides visual interest and supports brand identity." if accent_hex else "No accent color specified.",
                    secondary=f"Secondary color ({secondary_hex}) complements the primary color." if secondary_hex else None,
                    recommendations=recommendation_rationales,
                    overall=overall_rationale or f"Color system designed for {industry} with {principles.warmth}/10 warmth and {principles.philosophy} philosophy."
                )
                
                return colors, rationale, primary_recommendations
            except Exception as e:
                print(f"AI Color generation failed, falling back to rules: {e}")

        # Fallback to rule-based logic with industry context and seed-based variation
        if industry_colors:
            primary_hex = industry_colors.get('primary')
            neutral_hex = industry_colors.get('neutral')
            accent_hex = industry_colors.get('accent')
        else:
            # Generate seed from product_idea for deterministic variation
            seed = 0
            if product_idea:
                seed = int(hashlib.md5(product_idea.encode()).hexdigest()[:8], 16)
            
            # Base hue based on warmth, then add seed-based variation
            if principles.warmth <= 3:
                base_hue = 0.6  # Cool (blue)
            elif principles.warmth >= 7:
                base_hue = 0.1   # Warm (red/orange)
            else:
                base_hue = 0.5  # Balanced (teal/purple)
            
            # Add seed-based variation (0-120 degrees) to ensure different products get different colors
            # Use more of the seed to get better distribution
            hue_variation = (seed % 120) / 360.0  # 0-120 degrees (1/3 of color wheel)
            varied_hue = (base_hue + hue_variation) % 1.0
            
            # Vary saturation based on seed (0.5-0.85 range for more diversity)
            base_saturation = 0.7
            saturation_variation = 0.35 * ((seed % 20) / 20.0)  # More variation
            varied_saturation = base_saturation - 0.2 + saturation_variation
            varied_saturation = max(0.5, min(0.85, varied_saturation))
            
            # Vary lightness based on seed (0.3-0.5 range for accessibility)
            base_lightness = 0.4
            lightness_variation = 0.2 * ((seed % 10) / 10.0)  # More variation
            varied_lightness = base_lightness - 0.1 + lightness_variation
            varied_lightness = max(0.3, min(0.5, varied_lightness))
            
            print(f"🎨 Generated fallback color with seed-based variation (seed: {seed % 1000}, hue: {varied_hue:.3f})")
            
            primary_hex = self.hsl_to_hex(varied_hue, varied_saturation, varied_lightness)
            neutral_hex = "#64748b"
            accent_hex = None
        
        # Generate 3 recommendations for fallback
        primary_recommendations = []
        seed = int(hashlib.md5(product_idea.encode()).hexdigest()[:8], 16) if product_idea else 0
        
        # Generate 3 different primary colors with variations
        for i in range(3):
            # Use different parts of seed for each recommendation
            rec_seed = (seed + i * 1000) % 1000000
            
            if industry_colors and i == 0:
                # First recommendation uses industry color
                rec_primary = industry_colors.get('primary')
            else:
                # Generate variation based on warmth
                if principles.warmth <= 3:
                    base_hue = 0.6  # Cool (blue)
                elif principles.warmth >= 7:
                    base_hue = 0.1   # Warm (red/orange)
                else:
                    base_hue = 0.5  # Balanced (teal/purple)
                
                # Add variation for each recommendation
                hue_variation = ((rec_seed % 120) + i * 40) / 360.0
                varied_hue = (base_hue + hue_variation) % 1.0
                varied_saturation = 0.5 + ((rec_seed % 20) / 40.0)  # 0.5-1.0
                varied_lightness = 0.35 + ((rec_seed % 10) / 30.0)  # 0.35-0.65
                varied_lightness = max(0.3, min(0.5, varied_lightness))
                
                rec_primary = self.hsl_to_hex(varied_hue, varied_saturation, varied_lightness)
            
            # Generate complementary secondary color
            r = int(rec_primary[1:3], 16) / 255
            g = int(rec_primary[3:5], 16) / 255
            b = int(rec_primary[5:7], 16) / 255
            h, l, s = colorsys.rgb_to_hls(r, g, b)
            
            # Complementary color (opposite on color wheel)
            comp_hue = (h + 0.5) % 1.0
            comp_saturation = min(0.8, s + 0.1)
            comp_lightness = max(0.3, min(0.5, l))
            rec_secondary = self.hsl_to_hex(comp_hue, comp_saturation, comp_lightness)
            
            # Ensure accessibility
            if Validator.get_contrast_ratio(rec_primary, "#FFFFFF") < 4.5:
                rec_primary = self.ensure_contrast(rec_primary, "#FFFFFF", min_contrast=4.5)
            if Validator.get_contrast_ratio(rec_secondary, "#FFFFFF") < 4.5:
                rec_secondary = self.ensure_contrast(rec_secondary, "#FFFFFF", min_contrast=4.5)
            
            primary_recommendations.append({
                'primary': rec_primary,
                'secondary': rec_secondary,
                'rationale': f"Recommendation {i+1}: Primary {rec_primary} with complementary secondary {rec_secondary}."
            })
        
        # Use first recommendation as default
        selected_rec = primary_recommendations[0]
        primary_hex = selected_rec['primary']
        secondary_hex = selected_rec['secondary']
        
        # Check primary color contrast
        contrast = Validator.get_contrast_ratio(primary_hex, "#FFFFFF")
        if contrast < 4.5:
            print(f"⚠️  WARNING: Primary color contrast {contrast:.2f} < 4.5. Adjusting...")
            primary_hex = self.ensure_contrast(primary_hex, "#FFFFFF", min_contrast=4.5)
            print(f"✅ Adjusted to {primary_hex} with contrast {Validator.get_contrast_ratio(primary_hex, '#FFFFFF'):.2f}")
        
        colors = self.generate_scale_from_hex(primary_hex, "primary")
        colors.extend(self.generate_scale_from_hex(neutral_hex, "neutral", saturation_mult=0.05))
        
        # Add secondary color scale
        if secondary_hex:
            contrast = Validator.get_contrast_ratio(secondary_hex, "#FFFFFF")
            if contrast < 4.5:
                secondary_hex = self.ensure_contrast(secondary_hex, "#FFFFFF", min_contrast=4.5)
            colors.extend(self.generate_scale_from_hex(secondary_hex, "secondary"))
        
        if accent_hex:
            colors.extend(self.generate_scale_from_hex(accent_hex, "accent"))
        
        # Add semantic colors with accessibility in mind (WCAG AA compliant)
        colors.extend(self.generate_accessible_semantic_colors())
        
        rationale = ColorRationale(
            primary=f"Primary color ({primary_hex}) based on industry standards for {industry}.",
            neutral=f"Neutral color ({neutral_hex}) provides balanced base for UI elements.",
            accent=f"Accent color ({accent_hex}) adds visual interest." if accent_hex else "No accent color specified.",
            secondary=f"Secondary color ({secondary_hex}) complements the primary color." if secondary_hex else None,
            recommendations=[rec['rationale'] for rec in primary_recommendations],
            overall=f"Color system generated using industry patterns for {industry}."
        )
        
        return colors, rationale, primary_recommendations

    def generate_scale_from_hex(self, hex_color: str, name: str, saturation_mult: float = 1.0) -> list[ColorToken]:
        """Generate a 50-900 scale from a single hex color."""
        # Convert hex to HLS
        r = int(hex_color[1:3], 16) / 255
        g = int(hex_color[3:5], 16) / 255
        b = int(hex_color[5:7], 16) / 255
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        
        tokens = []
        # Inverted weights for lightness (50 is light, 900 is dark)
        lightness_map = {
            50: 0.97, 100: 0.9, 200: 0.8, 300: 0.7, 400: 0.6,
            500: l, 600: 0.4, 700: 0.3, 800: 0.2, 900: 0.1
        }
        
        white = "#FFFFFF"
        
        for weight, lightness in lightness_map.items():
            hex_val = self.hsl_to_hex(h, s * saturation_mult, lightness)
            
            # For neutral-700, verify it meets WCAG AA contrast on white (for body text)
            # AI should generate dark enough neutral-700 from the start
            if name == "neutral" and weight == 700:
                contrast = Validator.get_contrast_ratio(hex_val, white)
                if contrast < 4.5:
                    # Only adjust if absolutely necessary
                    hex_val = self.ensure_contrast(hex_val, white, min_contrast=4.5)
            
            tokens.append(ColorToken(name=f"{name}-{weight}", value=hex_val, role=name))
        return tokens

    def generate_typography_system(self, principles: DesignPrinciples) -> list[TypographyToken]:
        """Generate typography tokens based on design principles."""

        # Choose font families based on philosophy
        if principles.philosophy == "brand-led":
            heading_family = "Inter, system-ui, sans-serif"
            body_family = "Inter, system-ui, sans-serif"
        elif principles.philosophy == "utility-first":
            heading_family = "system-ui, sans-serif"
            body_family = "system-ui, sans-serif"
        else:  # component-first
            heading_family = "Inter, system-ui, sans-serif"
            body_family = "Inter, system-ui, sans-serif"

        # Adjust sizes based on density and clarity
        if principles.density == "dense":
            base_size = 14
            scale_factor = 1.2
        elif principles.density == "spacious":
            base_size = 16
            scale_factor = 1.25
        else:  # balanced
            base_size = 15
            scale_factor = 1.22
        
        # Ensure minimum size for high clarity requirements
        if principles.clarity >= 9:
            base_size = max(base_size, 15)

        typography = []

        # Body text sizes
        for i in range(-2, 4):
            size = base_size * (scale_factor ** i)
            typography.append(TypographyToken(
                name=f"body-{i+2}",
                family=body_family,
                size=f"{size:.1f}px",
                weight=400,
                line_height=1.5,
                role="body"
            ))

        # Heading sizes (larger scale)
        for i in range(1, 7):
            size = base_size * (scale_factor ** (i + 1))
            typography.append(TypographyToken(
                name=f"heading-{i}",
                family=heading_family,
                size=f"{size:.1f}px",
                weight=600 if i <= 3 else 500,
                line_height=1.2,
                role="heading"
            ))

        # UI text
        typography.append(TypographyToken(
            name="ui-small",
            family=body_family,
            size="12px",
            weight=400,
            line_height=1.4,
            role="ui"
        ))

        return typography

    def generate_spacing_system(self, principles: DesignPrinciples) -> list[SpacingToken]:
        """Generate spacing scale based on design principles."""

        # Base spacing unit
        if principles.density == "dense":
            base_unit = 4
        elif principles.density == "spacious":
            base_unit = 8
        else:  # balanced
            base_unit = 6

        spacing = []

        # Generate spacing scale (1-16)
        for i in range(1, 17):
            value = base_unit * i
            spacing.append(SpacingToken(
                name=f"space-{i}",
                value=f"{value}px",
                scale=i
            ))

        return spacing

    def hsl_to_hex(self, h: float, s: float, l: float) -> str:
        """Convert HSL to hex color."""
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    def ensure_contrast(self, color_hex: str, background_hex: str = "#FFFFFF", min_contrast: float = 4.5) -> str:
        """Adjust a color to meet minimum contrast ratio with background."""
        contrast = Validator.get_contrast_ratio(color_hex, background_hex)
        
        if contrast >= min_contrast:
            return color_hex
        
        # Convert to HSL
        r = int(color_hex[1:3], 16) / 255
        g = int(color_hex[3:5], 16) / 255
        b = int(color_hex[5:7], 16) / 255
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        
        # Darken the color until it meets contrast requirements
        # We'll reduce lightness while maintaining hue and saturation
        attempts = 0
        max_attempts = 50
        adjusted_hex = color_hex
        
        while contrast < min_contrast and attempts < max_attempts:
            l = max(0.15, l - 0.08)  # Darken by 8% each iteration, minimum lightness 0.15
            adjusted_hex = self.hsl_to_hex(h, s, l)
            contrast = Validator.get_contrast_ratio(adjusted_hex, background_hex)
            attempts += 1
        
        # If still not meeting contrast, try reducing saturation and darkening more
        if contrast < min_contrast:
            # More aggressive darkening
            l = 0.25  # Force darker
            s = max(0.3, s * 0.8)  # Slightly reduce saturation
            adjusted_hex = self.hsl_to_hex(h, s, l)
            contrast = Validator.get_contrast_ratio(adjusted_hex, background_hex)
        
        return adjusted_hex

    def generate_accessible_semantic_colors(self) -> list[ColorToken]:
        """Generate semantic colors that meet WCAG AA contrast requirements on white."""
        # Use darker base colors that naturally meet 4.5:1 contrast on white
        # These lightness values are chosen to ensure accessibility from the start
        semantic_base = {
            "success": {"h": 0.4, "s": 0.65, "l": 0.38},  # Darker green (was 0.45)
            "error": {"h": 0.0, "s": 0.70, "l": 0.45},   # Darker red (was 0.50)
            "warning": {"h": 0.12, "s": 0.80, "l": 0.40}, # Darker orange (was 0.50)
            "info": {"h": 0.58, "s": 0.70, "l": 0.45}     # Darker blue (was 0.50)
        }
        
        semantic_colors = []
        white = "#FFFFFF"
        
        for name, hsl in semantic_base.items():
            # Generate color with darker base (should meet contrast naturally)
            base_hex = self.hsl_to_hex(hsl["h"], hsl["s"], hsl["l"])
            
            # Verify contrast (should meet 4.5:1 naturally with darker base colors)
            contrast = Validator.get_contrast_ratio(base_hex, white)
            if contrast < 4.5:
                # Only adjust if absolutely necessary (should rarely happen with darker base)
                accessible_hex = self.ensure_contrast(base_hex, white, min_contrast=4.5)
            else:
                accessible_hex = base_hex
            
            semantic_colors.append(
                ColorToken(name=f"{name}-500", value=accessible_hex, role="semantic")
            )
        
        return semantic_colors

    def generate_design_tokens(self, principles: DesignPrinciples, product_idea: str = "") -> DesignTokens:
        """Generate complete design token system."""
        # Generate light mode colors with rationale and recommendations
        light_colors, color_rationale, primary_recommendations = self.generate_color_system(principles, product_idea)
        
        # Generate dark mode colors
        dark_colors = self.generate_dark_color_system(principles)

        # Border radius based on philosophy
        if principles.philosophy == "brand-led":
            border_radius = {"small": "4px", "medium": "8px", "large": "16px", "round": "9999px"}
        elif principles.philosophy == "utility-first":
            border_radius = {"small": "2px", "medium": "4px", "large": "6px", "round": "9999px"}
        else:
            border_radius = {"small": "6px", "medium": "12px", "large": "24px", "round": "9999px"}

        # Shadows based on density
        if principles.density == "dense":
            shadows = {
                "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
                "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)"
            }
        else:
            shadows = {
                "sm": "0 1px 3px 0 rgb(0 0 0 / 0.1)",
                "md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
                "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
            }

        return DesignTokens(
            colors=light_colors,
            dark_colors=dark_colors,
            typography=self.generate_typography_system(principles),
            spacing=self.generate_spacing_system(principles),
            border_radius=border_radius,
            shadows=shadows,
            color_rationale=color_rationale,
            primary_recommendations=primary_recommendations
        )

    def generate_dark_color_system(self, principles: DesignPrinciples) -> list[ColorToken]:
        """Generate a color system specifically for dark mode."""
        industry = principles.industry_context.industry if principles.industry_context else "unknown"
        
        # Use same hues but adjust for dark mode
        # For dark mode, we want darker backgrounds and lighter text
        if principles.warmth >= 7:
            base_hue = 0.1  # Warm colors
        elif principles.warmth <= 3:
            base_hue = 0.6  # Cool colors
        else:
            base_hue = 0.5  # Neutral

        saturation = 0.5  # Slightly desaturated for dark mode

        colors = []
        # Primary scale - adjusted for dark mode
        for i in range(50, 951, 100):
            # In dark mode, lighter shades (50-300) are used for text/accents
            # Darker shades (700-900) are used for backgrounds
            lightness = (1000 - i) / 1000
            # Adjust lightness for better dark mode contrast
            if i <= 300:
                lightness = 0.7 + (i / 1000) * 0.2  # Lighter for text
            else:
                lightness = 0.1 + ((1000 - i) / 1000) * 0.3  # Darker for backgrounds
            
            hex_color = self.hsl_to_hex(base_hue, saturation, lightness)
            colors.append(ColorToken(
                name=f"primary-{i}",
                value=hex_color,
                role="primary"
            ))

        # Neutral grays - inverted for dark mode backgrounds
        neutral_hue = 0.08 if principles.warmth >= 6 else 0.58
        for i in range(50, 951, 100):
            # Dark mode: 50 is dark background, 900 is light text
            lightness = 1.0 - (i / 1000)
            # Ensure we don't go to pure black/white
            lightness = max(0.05, min(0.95, lightness))
            hex_color = self.hsl_to_hex(neutral_hue, 0.05, lightness)
            colors.append(ColorToken(
                name=f"neutral-{i}",
                value=hex_color,
                role="neutral"
            ))

        # Semantic colors (slightly adjusted for dark mode contrast)
        # For dark mode, we still want good contrast but on dark backgrounds
        dark_semantic = self.generate_accessible_semantic_colors()
        colors.extend(dark_semantic)

        return colors
