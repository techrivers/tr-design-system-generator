"""Visual Identity Agent - Generates design tokens and visual foundations with enhanced autonomy."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import DesignPrinciples, DesignTokens, ColorToken, TypographyToken, SpacingToken, ColorRationale
from typing import Optional, Tuple
import colorsys
import json
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
        self.model = os.getenv("MODEL_NAME", "gemini/gemini-1.5-pro-latest")

    def generate_color_system(self, principles: DesignPrinciples) -> Tuple[list[ColorToken], Optional[ColorRationale]]:
        """Generate a complete color system based on design principles with industry context."""
        industry = principles.industry_context.industry if principles.industry_context else "unknown"
        industry_colors = KnowledgeBase.get_industry_color_suggestions(industry)
        
        if self.api_key:
            try:
                prompt = PromptTemplates.visual_identity_color_prompt(principles, industry, industry_colors)
                
                response = completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                
                data = json.loads(response.choices[0].message.content)
                primary_hex = data.get('primary')
                neutral_hex = data.get('neutral')
                accent_hex = data.get('accent', None)
                rationale_text = data.get('rationale', '')
                
                # Validate hex format
                if not primary_hex or not primary_hex.startswith('#'):
                    raise ValueError("Invalid primary color format")
                if not neutral_hex or not neutral_hex.startswith('#'):
                    raise ValueError("Invalid neutral color format")
                
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
                
                # Add accent if provided
                if accent_hex and accent_hex.startswith('#'):
                    colors.extend(self.generate_scale_from_hex(accent_hex, "accent"))
                
                # Add semantic colors with accessibility in mind (WCAG AA compliant)
                colors.extend(self.generate_accessible_semantic_colors())
                
                # Create color rationale
                rationale = ColorRationale(
                    primary=rationale_text or f"Primary color ({primary_hex}) selected to align with {industry} industry standards and design principles.",
                    neutral=rationale_text or f"Neutral color ({neutral_hex}) chosen to complement primary and support {principles.density} density UI.",
                    accent=rationale_text or f"Accent color ({accent_hex}) provides visual interest and supports brand identity." if accent_hex else "No accent color specified.",
                    overall=rationale_text or f"Color system designed for {industry} with {principles.warmth}/10 warmth and {principles.philosophy} philosophy."
                )
                
                return colors, rationale
            except Exception as e:
                print(f"AI Color generation failed, falling back to rules: {e}")

        # Fallback to rule-based logic with industry context
        if industry_colors:
            primary_hex = industry_colors.get('primary')
            neutral_hex = industry_colors.get('neutral')
            accent_hex = industry_colors.get('accent')
        else:
            # Generate based on warmth
            base_hue = 0.6 if principles.warmth <= 3 else (0.1 if principles.warmth >= 7 else 0.5)
            primary_hex = self.hsl_to_hex(base_hue, 0.7, 0.5)
            neutral_hex = "#64748b"
            accent_hex = None
        
        # Check primary color contrast (AI should generate accessible colors from the start)
        contrast = Validator.get_contrast_ratio(primary_hex, "#FFFFFF")
        if contrast < 4.5:
            # Only adjust if absolutely necessary (AI should have generated accessible color)
            print(f"⚠️  WARNING: Primary color contrast {contrast:.2f} < 4.5. AI should generate accessible colors from the start.")
            primary_hex = self.ensure_contrast(primary_hex, "#FFFFFF", min_contrast=4.5)
            print(f"✅ Adjusted to {primary_hex} with contrast {Validator.get_contrast_ratio(primary_hex, '#FFFFFF'):.2f}")
        
        colors = self.generate_scale_from_hex(primary_hex, "primary")
        colors.extend(self.generate_scale_from_hex(neutral_hex, "neutral", saturation_mult=0.05))
        
        if accent_hex:
            colors.extend(self.generate_scale_from_hex(accent_hex, "accent"))
        
        # Add semantic colors with accessibility in mind (WCAG AA compliant)
        colors.extend(self.generate_accessible_semantic_colors())
        
        rationale = ColorRationale(
            primary=f"Primary color ({primary_hex}) based on industry standards for {industry}.",
            neutral=f"Neutral color ({neutral_hex}) provides balanced base for UI elements.",
            accent=f"Accent color ({accent_hex}) adds visual interest." if accent_hex else "No accent color specified.",
            overall=f"Color system generated using industry patterns for {industry}."
        )
        
        return colors, rationale

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

    def generate_design_tokens(self, principles: DesignPrinciples) -> DesignTokens:
        """Generate complete design token system."""
        # Generate light mode colors with rationale
        light_colors, color_rationale = self.generate_color_system(principles)
        
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
            color_rationale=color_rationale
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
