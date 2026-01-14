"""Validation and quality assurance for agent outputs."""

import colorsys
from typing import Dict, List, Optional
from models import DesignTokens, DesignPrinciples, ComponentInventory, ValidationResult, ColorToken


class Validator:
    """Validates agent outputs for consistency, accessibility, and quality."""

    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple:
        """Convert hex color to RGB tuple (0-1 range)."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b)

    @staticmethod
    def get_luminance(rgb: tuple) -> float:
        """Calculate relative luminance (WCAG formula)."""
        r, g, b = rgb
        
        # Convert to linear RGB
        def to_linear(c):
            if c <= 0.03928:
                return c / 12.92
            return ((c + 0.055) / 1.055) ** 2.4
        
        r_linear = to_linear(r)
        g_linear = to_linear(g)
        b_linear = to_linear(b)
        
        # Calculate luminance
        return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear

    @staticmethod
    def get_contrast_ratio(color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors (WCAG)."""
        rgb1 = Validator.hex_to_rgb(color1)
        rgb2 = Validator.hex_to_rgb(color2)
        
        lum1 = Validator.get_luminance(rgb1)
        lum2 = Validator.get_luminance(rgb2)
        
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        
        if darker == 0:
            return 0
        
        return (lighter + 0.05) / (darker + 0.05)

    @staticmethod
    def validate_color_accessibility(tokens: DesignTokens) -> ValidationResult:
        """Validate color tokens for WCAG 2.1 AA accessibility."""
        issues = []
        warnings = []
        
        # Find primary-500 and neutral colors
        primary_500 = None
        neutral_50 = None
        neutral_700 = None
        white = "#FFFFFF"
        
        for color in tokens.colors:
            if color.name == "primary-500":
                primary_500 = color.value
            elif color.name == "neutral-50":
                neutral_50 = color.value
            elif color.name == "neutral-700":
                neutral_700 = color.value
        
        # Validate primary-500 on white (for buttons, links)
        if primary_500:
            contrast = Validator.get_contrast_ratio(primary_500, white)
            if contrast < 4.5:
                issues.append(f"Primary-500 ({primary_500}) on white has contrast ratio {contrast:.2f}, needs >= 4.5 for WCAG AA")
            elif contrast < 7.0:
                warnings.append(f"Primary-500 contrast is {contrast:.2f}, consider increasing to 7.0 for AAA")
        
        # Validate neutral-700 on white (for body text)
        if neutral_700:
            contrast = Validator.get_contrast_ratio(neutral_700, white)
            if contrast < 4.5:
                issues.append(f"Neutral-700 ({neutral_700}) on white has contrast ratio {contrast:.2f}, needs >= 4.5 for WCAG AA")
        
        # Validate primary-500 on neutral-50 (for primary buttons on light backgrounds)
        if primary_500 and neutral_50:
            contrast = Validator.get_contrast_ratio(primary_500, neutral_50)
            if contrast < 4.5:
                issues.append(f"Primary-500 on neutral-50 has contrast ratio {contrast:.2f}, needs >= 4.5")
        
        # Validate semantic colors
        semantic_colors = {
            "success": None,
            "error": None,
            "warning": None,
            "info": None
        }
        
        for color in tokens.colors:
            if color.name.startswith("success-"):
                semantic_colors["success"] = color.value
            elif color.name.startswith("error-"):
                semantic_colors["error"] = color.value
            elif color.name.startswith("warning-"):
                semantic_colors["warning"] = color.value
            elif color.name.startswith("info-"):
                semantic_colors["info"] = color.value
        
        for name, color_value in semantic_colors.items():
            if color_value:
                contrast = Validator.get_contrast_ratio(color_value, white)
                if contrast < 4.5:
                    issues.append(f"{name.capitalize()} color ({color_value}) on white has contrast ratio {contrast:.2f}, needs >= 4.5")
        
        # Calculate quality score
        score = 1.0
        if issues:
            score -= len(issues) * 0.2
        if warnings:
            score -= len(warnings) * 0.05
        score = max(0.0, score)
        
        return ValidationResult(
            valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            score=score
        )

    @staticmethod
    def validate_design_consistency(principles: DesignPrinciples, tokens: DesignTokens) -> ValidationResult:
        """Validate consistency between design principles and tokens."""
        issues = []
        warnings = []
        
        # Check if color warmth matches principles
        # This is a heuristic - warm colors have higher red/yellow components
        primary_colors = [c for c in tokens.colors if c.name == "primary-500"]
        if primary_colors:
            primary_hex = primary_colors[0].value
            rgb = Validator.hex_to_rgb(primary_hex)
            r, g, b = rgb
            
            # Calculate "warmth" of color (red+yellow components)
            color_warmth = (r + g) / 2
            
            # Expected warmth from principles (normalized to 0-1)
            expected_warmth = principles.warmth / 10.0
            
            # Check if they align (allow some variance)
            if abs(color_warmth - expected_warmth) > 0.3:
                if principles.warmth >= 7 and color_warmth < 0.4:
                    issues.append(f"Color system is too cool (warmth score: {color_warmth:.2f}) for principles.warmth={principles.warmth}")
                elif principles.warmth <= 3 and color_warmth > 0.6:
                    issues.append(f"Color system is too warm (warmth score: {color_warmth:.2f}) for principles.warmth={principles.warmth}")
        
        # Check if density matches spacing
        spacing_values = [int(s.value.replace('px', '')) for s in tokens.spacing]
        if spacing_values:
            base_spacing = min(spacing_values) if spacing_values else 4
            
            if principles.density == "dense" and base_spacing > 6:
                warnings.append(f"Spacing base unit ({base_spacing}px) seems large for dense UI")
            elif principles.density == "spacious" and base_spacing < 6:
                warnings.append(f"Spacing base unit ({base_spacing}px) seems small for spacious UI")
        
        # Check if clarity matches typography sizes
        if tokens.typography:
            body_sizes = [float(t.size.replace('px', '')) for t in tokens.typography if t.role == "body"]
            if body_sizes:
                min_body_size = min(body_sizes)
                if principles.clarity >= 9 and min_body_size < 14:
                    warnings.append(f"Body text size ({min_body_size}px) may be too small for high clarity requirement")
        
        score = 1.0
        if issues:
            score -= len(issues) * 0.3
        if warnings:
            score -= len(warnings) * 0.1
        score = max(0.0, score)
        
        return ValidationResult(
            valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            score=score
        )

    @staticmethod
    def validate_component_completeness(
        inventory: ComponentInventory,
        industry: str,
        product_context: str
    ) -> ValidationResult:
        """Validate component inventory for completeness."""
        issues = []
        warnings = []
        
        from agents.knowledge_base import KnowledgeBase
        
        # Get expected components for industry
        expected_components = KnowledgeBase.get_components_for_industry(industry)
        actual_components = [c.name for c in inventory.components]
        
        # Check for missing critical components
        missing_critical = []
        for expected in expected_components:
            if expected not in actual_components:
                # Some components are optional
                if expected in ["Button", "Input", "Select", "Modal", "Alert"]:
                    missing_critical.append(expected)
                else:
                    warnings.append(f"Consider adding {expected} component for {industry} products")
        
        if missing_critical:
            issues.append(f"Missing critical components: {', '.join(missing_critical)}")
        
        # Check component dependencies
        for component in inventory.components:
            dependencies = KnowledgeBase.get_component_dependencies(component.name)
            for dep in dependencies:
                if dep not in actual_components:
                    warnings.append(f"{component.name} typically requires {dep} component")
        
        # Check if component variants/states are appropriate
        for component in inventory.components:
            if component.name == "Button" and "primary" not in component.variants:
                issues.append("Button component should have 'primary' variant")
            if component.name == "Input" and "error" not in component.states:
                warnings.append("Input component should have 'error' state for form validation")
        
        score = 1.0
        if issues:
            score -= len(issues) * 0.3
        if warnings:
            score -= len(warnings) * 0.05
        score = max(0.0, score)
        
        return ValidationResult(
            valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            score=score
        )

    @staticmethod
    def validate_all(
        principles: DesignPrinciples,
        tokens: DesignTokens,
        inventory: ComponentInventory,
        industry: str,
        product_context: str
    ) -> Dict[str, ValidationResult]:
        """Run all validation checks."""
        return {
            "color_accessibility": Validator.validate_color_accessibility(tokens),
            "design_consistency": Validator.validate_design_consistency(principles, tokens),
            "component_completeness": Validator.validate_component_completeness(inventory, industry, product_context)
        }
