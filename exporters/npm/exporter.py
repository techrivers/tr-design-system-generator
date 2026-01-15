"""NPM package exporter for design systems."""

import json
from pathlib import Path
from typing import Dict, Any
from models import DesignSystemOutput


class NPMExporter:
    """Exports design system as publishable NPM package."""
    
    def export(self, design_system: DesignSystemOutput, output_dir: Path):
        """Export design system as NPM package."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create package structure
        (output_dir / "src" / "components").mkdir(parents=True, exist_ok=True)
        (output_dir / "src" / "styles").mkdir(parents=True, exist_ok=True)
        (output_dir / "dist").mkdir(exist_ok=True)
        (output_dir / "types").mkdir(exist_ok=True)
        
        # Generate package.json
        package_json = self._generate_package_json(design_system)
        with open(output_dir / "package.json", 'w') as f:
            f.write(json.dumps(package_json, indent=2))
        
        # Generate TypeScript config
        tsconfig = self._generate_tsconfig()
        with open(output_dir / "tsconfig.json", 'w') as f:
            f.write(json.dumps(tsconfig, indent=2))
        
        # Generate components
        from templates.components.generator import ComponentGenerator
        comp_gen = ComponentGenerator(design_system.tokens)
        
        components_export = []
        for component_spec in design_system.components.components:
            component_name = component_spec.name.lower()
            if hasattr(comp_gen, f"generate_{component_name}_component"):
                method = getattr(comp_gen, f"generate_{component_name}_component")
                code = method(component_spec)
                
                # Write component file
                file_path = output_dir / "src" / "components" / f"{component_spec.name}.tsx"
                with open(file_path, 'w') as f:
                    f.write(code)
                
                components_export.append(component_spec.name)
        
        # Generate index.ts barrel export
        index_content = self._generate_index(components_export)
        with open(output_dir / "src" / "index.ts", 'w') as f:
            f.write(index_content)
        
        # Generate CSS variables
        css_vars = comp_gen.generate_css_variables()
        with open(output_dir / "src" / "styles" / "tokens.css", 'w') as f:
            f.write(css_vars)
        
        # Generate README
        readme = self._generate_readme(design_system, components_export)
        with open(output_dir / "README.md", 'w') as f:
            f.write(readme)
    
    def _generate_package_json(self, design_system: DesignSystemOutput) -> Dict[str, Any]:
        """Generate package.json for NPM package."""
        return {
            "name": f"@{design_system.principles.philosophy}-design-system",
            "version": "1.0.0",
            "description": f"Design system for {design_system.input.product_idea[:50]}...",
            "main": "dist/index.js",
            "module": "dist/index.esm.js",
            "types": "dist/index.d.ts",
            "files": [
                "dist",
                "src",
                "types"
            ],
            "scripts": {
                "build": "tsc && rollup -c",
                "dev": "rollup -c -w",
                "test": "jest",
                "storybook": "start-storybook -p 6006",
                "build-storybook": "build-storybook"
            },
            "keywords": [
                "design-system",
                "components",
                "react",
                "typescript",
                "tailwind"
            ],
            "author": "",
            "license": "MIT",
            "peerDependencies": {
                "react": ">=18.0.0",
                "react-dom": ">=18.0.0"
            },
            "dependencies": {
                "framer-motion": "^10.16.0"
            },
            "devDependencies": {
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "typescript": "^5.0.0",
                "rollup": "^3.0.0",
                "@rollup/plugin-typescript": "^11.0.0",
                "jest": "^29.0.0",
                "@testing-library/react": "^14.0.0",
                "@storybook/react": "^7.0.0"
            }
        }
    
    def _generate_tsconfig(self) -> Dict[str, Any]:
        """Generate TypeScript configuration."""
        return {
            "compilerOptions": {
                "target": "ES2020",
                "module": "ESNext",
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "jsx": "react-jsx",
                "declaration": True,
                "declarationMap": True,
                "outDir": "./dist",
                "rootDir": "./src",
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True,
                "moduleResolution": "node",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": False
            },
            "include": ["src/**/*"],
            "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.test.tsx"]
        }
    
    def _generate_index(self, components: list) -> str:
        """Generate barrel export index file."""
        lines = ["// Design System Components", ""]
        for component in components:
            lines.append(f"export {{ {component} }} from './components/{component}';")
        lines.append("")
        lines.append("// Styles")
        lines.append("export * from './styles/tokens.css';")
        return "\n".join(lines)
    
    def _generate_readme(self, design_system: DesignSystemOutput, components: list) -> str:
        """Generate README for NPM package."""
        return f"""# Design System Package

Generated design system for: {design_system.input.product_idea}

## Installation

\`\`\`bash
npm install @{design_system.principles.philosophy}-design-system
\`\`\`

## Usage

\`\`\`tsx
import {{ Button }} from '@{design_system.principles.philosophy}-design-system';
import '@{design_system.principles.philosophy}-design-system/styles/tokens.css';

function App() {{
  return <Button variant="primary">Click me</Button>;
}}
\`\`\`

## Components

{chr(10).join(f"- {c}" for c in components)}

## Design Tokens

- Colors: {len(design_system.tokens.colors)} tokens
- Typography: {len(design_system.tokens.typography)} scales
- Spacing: {len(design_system.tokens.spacing)} values

## Philosophy

- **Philosophy**: {design_system.principles.philosophy}
- **Density**: {design_system.principles.density}
- **Clarity**: {design_system.principles.clarity}/10
- **Warmth**: {design_system.principles.warmth}/10
"""
