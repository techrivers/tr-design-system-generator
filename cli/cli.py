#!/usr/bin/env python3
"""Command-line interface for Design System Generator."""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import DesignSystemGenerator
from models import DesignSystemInput, TargetUser, BrandTrait, Platform


def generate_command(args):
    """Generate a design system from product idea."""
    print("🎨 Technology Rivers Design System Generator\n")
    
    # Parse optional parameters
    target_users = None
    if args.users:
        try:
            target_users = [TargetUser(u.strip()) for u in args.users.split(',')]
        except ValueError as e:
            print(f"❌ Error: Invalid target user. Valid options: B2B, B2C, enterprise, consumer")
            sys.exit(1)
    
    brand_traits = None
    if args.traits:
        try:
            brand_traits = [BrandTrait(t.strip()) for t in args.traits.split(',')]
        except ValueError as e:
            print(f"❌ Error: Invalid brand trait. Valid options: modern, clinical, playful, premium, bold, minimal, warm, professional")
            sys.exit(1)
    
    platforms = None
    if args.platforms:
        try:
            platforms = [Platform(p.strip()) for p in args.platforms.split(',')]
        except ValueError as e:
            print(f"❌ Error: Invalid platform. Valid options: web, mobile, dashboard, marketing")
            sys.exit(1)
    
    # Create input
    input_data = DesignSystemInput(
        product_idea=args.product_idea,
        target_users=target_users,
        brand_traits=brand_traits,
        platforms=platforms
    )
    
    # Generate
    generator = DesignSystemGenerator()
    result = generator.generate_design_system(input_data)
    
    # Save output
    output_dir = Path(args.output or "generated")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = result.generated_at.replace(':', '-').replace(' ', '-')
    output_file = output_dir / f"design-system-{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(result.model_dump(), f, indent=2)
    
    print(f"\n✅ Design system generated successfully!")
    print(f"📁 Output: {output_file}")
    print(f"🎨 Colors: {len(result.tokens.colors)}")
    print(f"🧩 Components: {len(result.components.components)}")
    
    return result


def init_command(args):
    """Initialize a project with generated design system."""
    print("🚀 Initializing project with design system...\n")
    
    # Check if output directory exists
    output_dir = Path(args.directory or ".")
    if output_dir.exists() and any(output_dir.iterdir()):
        if not args.force:
            print(f"❌ Error: Directory '{output_dir}' is not empty. Use --force to overwrite.")
            sys.exit(1)
    
    # Generate design system first
    print("📋 Generating design system...")
    product_idea = args.product_idea or input("Enter your product idea: ")
    
    input_data = DesignSystemInput(product_idea=product_idea)
    generator = DesignSystemGenerator()
    result = generator.generate_design_system(input_data)
    
    # Create project structure
    output_dir.mkdir(exist_ok=True)
    
    # Save design system JSON
    with open(output_dir / "design-system.json", 'w') as f:
        json.dump(result.model_dump(), f, indent=2)
    
    # Generate component library files
    from templates.components.generator import ComponentGenerator
    comp_gen = ComponentGenerator(result.tokens)
    
    # Create directories
    (output_dir / "src" / "components").mkdir(parents=True, exist_ok=True)
    (output_dir / "src" / "styles").mkdir(parents=True, exist_ok=True)
    (output_dir / ".storybook").mkdir(exist_ok=True)
    
    # Generate CSS variables
    css_vars = comp_gen.generate_css_variables()
    with open(output_dir / "src" / "styles" / "tokens.css", 'w') as f:
        f.write(css_vars)
    
    # Generate components
    for component_spec in result.components.components:
        component_name = component_spec.name.lower()
        method_name = f"generate_{component_name}_component"
        if hasattr(comp_gen, method_name):
            method = getattr(comp_gen, method_name)
            try:
                code = method(component_spec)
                file_path = output_dir / "src" / "components" / f"{component_spec.name}.tsx"
                with open(file_path, 'w') as f:
                    f.write(code)
            except Exception as e:
                print(f"   ⚠️  Warning: Could not generate {component_spec.name}: {e}")
    
    # Generate package.json
    package_json = comp_gen.generate_package_json()
    with open(output_dir / "package.json", 'w') as f:
        f.write(package_json)
    
    # Generate README
    readme = comp_gen.generate_readme(
        [ComponentCode(name=c.name, code="", file_path=f"src/components/{c.name}.tsx") 
         for c in result.components.components],
        result.principles.model_dump(),
        product_idea
    )
    with open(output_dir / "README.md", 'w') as f:
        f.write(readme)
    
    print(f"\n✅ Project initialized in '{output_dir}'")
    print(f"📦 Next steps:")
    print(f"   cd {output_dir}")
    print(f"   npm install")
    print(f"   npm run storybook")


def export_command(args):
    """Export design system in various formats."""
    print(f"📦 Exporting design system as {args.format}...\n")
    
    # Load design system
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"❌ Error: File '{input_file}' not found.")
        sys.exit(1)
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    from models import DesignSystemOutput
    result = DesignSystemOutput(**data)
    
    output_dir = Path(args.output or "export")
    output_dir.mkdir(exist_ok=True)
    
    if args.format == "npm":
        # Export as NPM package
        from exporters.npm.exporter import NPMExporter
        exporter = NPMExporter()
        exporter.export(result, output_dir)
        print(f"✅ NPM package exported to '{output_dir}'")
    
    elif args.format == "figma-tokens":
        # Export as Figma Tokens
        from exporters.figma.tokens import FigmaTokensExporter
        exporter = FigmaTokensExporter()
        exporter.export(result, output_dir)
        print(f"✅ Figma Tokens exported to '{output_dir}'")
    
    elif args.format == "css":
        # Export CSS variables
        from templates.components.generator import ComponentGenerator
        comp_gen = ComponentGenerator(result.tokens)
        css_vars = comp_gen.generate_css_variables()
        with open(output_dir / "tokens.css", 'w') as f:
            f.write(css_vars)
        print(f"✅ CSS variables exported to '{output_dir}/tokens.css'")
    
    elif args.format == "typescript":
        # Export TypeScript types
        from generators.typescript.generator import TypeScriptGenerator
        ts_gen = TypeScriptGenerator()
        types = ts_gen.generate_all(result)
        
        (output_dir / "types").mkdir(exist_ok=True)
        for filename, content in types.items():
            with open(output_dir / "types" / filename, 'w') as f:
                f.write(content)
        print(f"✅ TypeScript types exported to '{output_dir}/types/'")
    
    elif args.format == "guidelines":
        # Export component guidelines
        from templates.guidelines.generator import GuidelinesGenerator
        guide_gen = GuidelinesGenerator()
        guidelines = guide_gen.generate_all_guidelines(result.components.components)
        
        (output_dir / "guidelines").mkdir(exist_ok=True)
        for comp in result.components.components:
            markdown = guide_gen.generate_markdown(comp)
            with open(output_dir / "guidelines" / f"{comp.name}.md", 'w') as f:
                f.write(markdown)
        print(f"✅ Component guidelines exported to '{output_dir}/guidelines/'")
    
    else:
        print(f"❌ Error: Unsupported format '{args.format}'. Supported: npm, figma-tokens, css, typescript, guidelines")
        sys.exit(1)


def preview_command(args):
    """Start local preview server."""
    import subprocess
    
    print("🚀 Starting preview server...\n")
    print("📝 Starting web interface on http://localhost:8000")
    print("   Press Ctrl+C to stop\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "web.app:app",
            "--host", "0.0.0.0",
            "--port", str(args.port),
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Preview server stopped.")


def docs_command(args):
    """Generate documentation site."""
    from ui.docs.generator import DocsSiteGenerator
    
    print("📚 Generating documentation site...\n")
    
    # Load design system
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"❌ Error: File '{input_file}' not found.")
        sys.exit(1)
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    from models import DesignSystemOutput
    design_system = DesignSystemOutput(**data)
    
    # Generate docs
    output_dir = Path(args.output or "docs-site")
    generator = DocsSiteGenerator()
    generator.generate(design_system, output_dir)
    
    print(f"✅ Documentation site generated in '{output_dir}'")
    print(f"📁 Open '{output_dir}/index.html' in your browser to view")
    
    if args.deploy:
        print("\n🚀 Deploying to GitHub Pages...")
        # Would add GitHub Pages deployment logic here
        print("   (Deployment feature coming soon)")


def playground_command(args):
    """Start component playground server."""
    import subprocess
    
    print("🎮 Starting component playground...\n")
    print("📝 Playground available at http://localhost:8000/playground")
    print("   Press Ctrl+C to stop\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "web.app:app",
            "--host", "0.0.0.0",
            "--port", str(args.port),
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Playground server stopped.")


def deploy_command(args):
    """Deploy project to hosting platform."""
    from deploy.vercel import VercelDeployer
    
    print(f"🚀 Deploying to {args.platform}...\n")
    
    project_dir = Path(args.directory or ".")
    if not project_dir.exists():
        print(f"❌ Error: Directory '{project_dir}' does not exist.")
        sys.exit(1)
    
    if args.platform == "vercel":
        deployer = VercelDeployer(project_dir)
        
        # Setup
        if args.setup:
            print("⚙️  Setting up Vercel configuration...")
            result = deployer.setup_vercel(framework=args.framework)
            if result["success"]:
                print(f"✅ Vercel config created: {result['file']}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
                sys.exit(1)
        
        # Deploy
        print("📤 Deploying to Vercel...")
        result = deployer.deploy(production=args.production)
        
        if result["success"]:
            print(f"\n✅ Deployment successful!")
            if result.get("url"):
                print(f"🌐 URL: {result['url']}")
        else:
            print(f"\n❌ Deployment failed: {result.get('error', 'Unknown error')}")
            if args.setup:
                print("\n💡 Tip: Run with --setup first to configure Vercel")
            sys.exit(1)
    else:
        print(f"❌ Error: Platform '{args.platform}' not supported yet.")
        print("   Supported platforms: vercel")
        sys.exit(1)


def integrate_command(args):
    """Integrate design system into existing project."""
    from cli.integrate import ProjectIntegrator
    
    print("🔧 Integrating design system into project...\n")
    
    project_dir = Path(args.directory or ".").resolve()
    
    if not project_dir.exists():
        print(f"❌ Error: Directory '{project_dir}' does not exist.")
        sys.exit(1)
    
    # Load design system
    if args.input:
        input_file = Path(args.input)
        if not input_file.exists():
            print(f"❌ Error: Design system file '{input_file}' not found.")
            sys.exit(1)
        
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        from models import DesignSystemOutput
        design_system = DesignSystemOutput(**data)
    else:
        # Generate new design system
        print("📋 Generating design system...")
        product_idea = args.product_idea or input("Enter your product idea: ")
        
        input_data = DesignSystemInput(product_idea=product_idea)
        generator = DesignSystemGenerator()
        design_system = generator.generate_design_system(input_data)
    
    # Integrate
    integrator = ProjectIntegrator(project_dir)
    results = integrator.integrate(
        design_system, 
        auto_install=args.auto_install,
        explicit_framework=args.framework
    )
    
    # Print results
    if results['errors']:
        print(f"\n❌ Integration completed with errors:")
        for error in results['errors']:
            print(f"   ❌ {error}")
    else:
        print(f"\n✅ Integration complete!")
    
    print(f"📦 Framework: {results['framework'] or 'Not detected'}")
    print(f"📦 Package Manager: {results['package_manager']}")
    
    if results.get('warnings'):
        print(f"\n⚠️  Warnings:")
        for warning in results['warnings']:
            print(f"   ⚠️  {warning}")
    
    if results['files_created']:
        print(f"\n📄 Files created ({len(results['files_created'])}):")
        for file in results['files_created']:
            print(f"   ✓ {file}")
    
    if results['files_modified']:
        print(f"\n📝 Files modified ({len(results['files_modified'])}):")
        for file in results['files_modified']:
            print(f"   ✏️  {file}")
    
    if results['dependencies_added']:
        deps = " ".join(results['dependencies_added'])
        pm = results['package_manager']
        if args.auto_install and not results['errors']:
            print(f"\n📦 Dependencies installed automatically:")
            print(f"   ✅ {pm} install -D {deps}")
        else:
            print(f"\n📦 Dependencies to install:")
            print(f"   {pm} install -D {deps}")
    
    if results.get('instructions'):
        print(f"\n📋 Next steps:")
        for instruction in results['instructions']:
            print(f"   • {instruction}")
    
    if not results['errors']:
        print(f"\n🎉 Design system integrated! Start using it in your project.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="tr-ds",
        description="Technology Rivers Design System Generator CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tr-ds generate "A modern e-commerce platform"
  tr-ds generate "Healthcare app" --users B2B,enterprise --traits modern,professional
  tr-ds init --directory my-project
  tr-ds integrate --auto
  tr-ds integrate --input design-system.json --directory ./my-app
  tr-ds docs --input design-system.json --deploy
  tr-ds playground
  tr-ds deploy --platform vercel --setup
  tr-ds deploy --platform vercel --production
  tr-ds export --input design-system.json --format npm
  tr-ds preview
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a design system")
    gen_parser.add_argument("product_idea", help="Product idea or description")
    gen_parser.add_argument("--users", help="Target users (comma-separated: B2B,B2C,enterprise,consumer)")
    gen_parser.add_argument("--traits", help="Brand traits (comma-separated: modern,professional,playful,etc)")
    gen_parser.add_argument("--platforms", help="Platforms (comma-separated: web,mobile,dashboard,marketing)")
    gen_parser.add_argument("--output", "-o", help="Output directory (default: generated/)")
    gen_parser.set_defaults(func=generate_command)
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize project with design system")
    init_parser.add_argument("--directory", "-d", help="Project directory (default: current directory)")
    init_parser.add_argument("--product-idea", help="Product idea (or will prompt)")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing directory")
    init_parser.set_defaults(func=init_command)
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export design system in various formats")
    export_parser.add_argument("--input", "-i", required=True, help="Input design system JSON file")
    export_parser.add_argument("--format", "-f", required=True, 
                              choices=["npm", "figma-tokens", "css", "typescript", "guidelines"], 
                              help="Export format")
    export_parser.add_argument("--output", "-o", help="Output directory (default: export/)")
    export_parser.set_defaults(func=export_command)
    
    # Preview command
    preview_parser = subparsers.add_parser("preview", help="Start local preview server")
    preview_parser.add_argument("--port", "-p", type=int, default=8000, help="Port number (default: 8000)")
    preview_parser.set_defaults(func=preview_command)
    
    # Integrate command
    integrate_parser = subparsers.add_parser("integrate", help="Integrate design system into existing project")
    integrate_parser.add_argument("--directory", "-d", help="Project directory (default: current directory)")
    integrate_parser.add_argument("--input", "-i", help="Design system JSON file (or will generate new)")
    integrate_parser.add_argument("--product-idea", help="Product idea (if generating new design system)")
    integrate_parser.add_argument("--framework", "-f", 
                                 choices=["nextjs", "vite", "cra", "vue"],
                                 help="Explicitly specify framework (nextjs, vite, cra, vue)")
    integrate_parser.add_argument("--auto-install", action="store_true", default=False,
                                 help="Automatically install dependencies (default: False for safety)")
    integrate_parser.add_argument("--no-auto-install", dest="auto_install", action="store_false",
                                 help="Don't automatically install dependencies")
    integrate_parser.set_defaults(func=integrate_command)
    
    # Docs command
    docs_parser = subparsers.add_parser("docs", help="Generate documentation site")
    docs_parser.add_argument("--input", "-i", required=True, help="Design system JSON file")
    docs_parser.add_argument("--output", "-o", help="Output directory (default: docs-site/)")
    docs_parser.add_argument("--deploy", action="store_true", help="Deploy to GitHub Pages")
    docs_parser.set_defaults(func=docs_command)
    
    # Playground command
    playground_parser = subparsers.add_parser("playground", help="Start component playground server")
    playground_parser.add_argument("--port", "-p", type=int, default=8000, help="Port number (default: 8000)")
    playground_parser.set_defaults(func=playground_command)
    
    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy project to hosting platform")
    deploy_parser.add_argument("--platform", "-p", choices=["vercel", "netlify"], default="vercel", help="Deployment platform")
    deploy_parser.add_argument("--directory", "-d", help="Project directory (default: current directory)")
    deploy_parser.add_argument("--framework", "-f", default="nextjs", help="Framework type (default: nextjs)")
    deploy_parser.add_argument("--setup", action="store_true", help="Set up deployment configuration")
    deploy_parser.add_argument("--production", action="store_true", help="Deploy to production (default: preview)")
    deploy_parser.set_defaults(func=deploy_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
