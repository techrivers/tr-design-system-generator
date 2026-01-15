"""Figma Tokens Studio format exporter."""

import json
from pathlib import Path
from typing import Dict, Any
from models import DesignSystemOutput


class FigmaTokensExporter:
    """Exports design tokens in Figma Tokens Studio format."""
    
    def export(self, design_system: DesignSystemOutput, output_dir: Path):
        """Export design tokens as Figma Tokens JSON."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        tokens = self._build_tokens_structure(design_system)
        
        output_file = output_dir / "tokens.json"
        with open(output_file, 'w') as f:
            json.dump(tokens, f, indent=2)
        
        # Also create a tokens directory structure for Figma Tokens Studio
        tokens_dir = output_dir / "tokens"
        tokens_dir.mkdir(exist_ok=True)
        
        # Split into separate files
        if "color" in tokens:
            with open(tokens_dir / "color.json", 'w') as f:
                json.dump({"color": tokens["color"]}, f, indent=2)
        
        if "typography" in tokens:
            with open(tokens_dir / "typography.json", 'w') as f:
                json.dump({"typography": tokens["typography"]}, f, indent=2)
        
        if "spacing" in tokens:
            with open(tokens_dir / "spacing.json", 'w') as f:
                json.dump({"spacing": tokens["spacing"]}, f, indent=2)
        
        if "shadow" in tokens:
            with open(tokens_dir / "shadow.json", 'w') as f:
                json.dump({"shadow": tokens["shadow"]}, f, indent=2)
    
    def _build_tokens_structure(self, design_system: DesignSystemOutput) -> Dict[str, Any]:
        """Build Figma Tokens Studio format structure."""
        tokens = {}
        
        # Colors
        colors = {}
        for color in design_system.tokens.colors:
            # Convert to Figma format: {color.primary.500: {value: "#hex"}}
            parts = color.name.split('-')
            if len(parts) >= 2:
                category = parts[0]
                shade = parts[1] if len(parts) > 1 else "base"
                
                if category not in colors:
                    colors[category] = {}
                colors[category][shade] = {
                    "value": color.value,
                    "type": "color"
                }
        if colors:
            tokens["color"] = colors
        
        # Typography
        typography = {}
        for typo in design_system.tokens.typography:
            typography[typo.name] = {
                "fontFamily": {"value": typo.family, "type": "fontFamily"},
                "fontSize": {"value": typo.size, "type": "fontSize"},
                "fontWeight": {"value": str(typo.weight), "type": "fontWeight"},
                "lineHeight": {"value": str(typo.line_height), "type": "lineHeight"}
            }
        if typography:
            tokens["typography"] = typography
        
        # Spacing
        spacing = {}
        for space in design_system.tokens.spacing:
            spacing[space.name] = {
                "value": space.value,
                "type": "spacing"
            }
        if spacing:
            tokens["spacing"] = spacing
        
        # Shadows
        shadows = {}
        for key, value in design_system.tokens.shadows.items():
            shadows[key] = {
                "value": value,
                "type": "boxShadow"
            }
        if shadows:
            tokens["shadow"] = shadows
        
        # Border radius
        radius = {}
        for key, value in design_system.tokens.border_radius.items():
            radius[key] = {
                "value": value,
                "type": "borderRadius"
            }
        if radius:
            tokens["borderRadius"] = radius
        
        return tokens
