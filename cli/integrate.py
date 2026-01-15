"""Project integration logic for auto-detecting and integrating design systems."""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
from models import DesignSystemOutput


class ProjectIntegrator:
    """Auto-detect and integrate design system into existing projects."""
    
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir).resolve()
        self.framework = None
        self.package_manager = None
        
    def detect_framework(self, explicit_framework: Optional[str] = None) -> Optional[str]:
        """Detect the framework used in the project.
        
        Args:
            explicit_framework: If provided, use this framework instead of auto-detecting
            
        Returns:
            Framework name or None if not detected
        """
        if explicit_framework:
            self.framework = explicit_framework
            return explicit_framework
            
        if not self.project_dir.exists():
            return None
        
        # Check package.json first for more accurate detection
        package_json = self.project_dir / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    pkg = json.load(f)
                    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                    
                    # Check for Next.js
                    if "next" in deps:
                        self.framework = "nextjs"
                        return "nextjs"
                    
                    # Check for Vite (but not Next.js which also uses Vite)
                    if "vite" in deps and "next" not in deps:
                        # Check if it's Vue or React
                        if "vue" in deps:
                            self.framework = "vue"
                            return "vue"
                        elif "react" in deps:
                            self.framework = "vite"
                            return "vite"
                    
                    # Check for Create React App
                    if "react-scripts" in deps:
                        self.framework = "cra"
                        return "cra"
                    
                    # Check for Vue (standalone)
                    if "vue" in deps and "@vue/cli-service" in deps:
                        self.framework = "vue"
                        return "vue"
            except (json.JSONDecodeError, IOError):
                pass  # Fall through to file-based detection
        
        # File-based detection as fallback
        # Check for Next.js
        if (self.project_dir / "next.config.js").exists() or \
           (self.project_dir / "next.config.ts").exists() or \
           (self.project_dir / "app").exists() or \
           (self.project_dir / "pages").exists():
            self.framework = "nextjs"
            return "nextjs"
        
        # Check for Vite
        if (self.project_dir / "vite.config.js").exists() or \
           (self.project_dir / "vite.config.ts").exists():
            # Check if it's Vue or React
            if (self.project_dir / "vue.config.js").exists() or \
               (package_json.exists() and self._check_package_for_vue(package_json)):
                self.framework = "vue"
                return "vue"
            self.framework = "vite"
            return "vite"
        
        # Check for Create React App
        if (self.project_dir / "src" / "index.js").exists() or \
           (self.project_dir / "src" / "index.tsx").exists():
            if package_json.exists() and self._check_package_for_cra(package_json):
                self.framework = "cra"
                return "cra"
        
        return None
    
    def _check_package_for_vue(self, package_json: Path) -> bool:
        """Check if package.json indicates Vue project."""
        try:
            with open(package_json) as f:
                pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                return "vue" in deps
        except (json.JSONDecodeError, IOError):
            return False
    
    def _check_package_for_cra(self, package_json: Path) -> bool:
        """Check if package.json indicates Create React App."""
        try:
            with open(package_json) as f:
                pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                return "react-scripts" in deps
        except (json.JSONDecodeError, IOError):
            return False
    
    def detect_package_manager(self) -> Optional[str]:
        """Detect package manager (npm, yarn, pnpm)."""
        if (self.project_dir / "package-lock.json").exists():
            self.package_manager = "npm"
            return "npm"
        elif (self.project_dir / "yarn.lock").exists():
            self.package_manager = "yarn"
            return "yarn"
        elif (self.project_dir / "pnpm-lock.yaml").exists():
            self.package_manager = "pnpm"
            return "pnpm"
        else:
            # Default to npm
            self.package_manager = "npm"
            return "npm"
    
    def integrate(self, design_system: DesignSystemOutput, 
                  auto_install: bool = False,
                  explicit_framework: Optional[str] = None) -> Dict[str, Any]:
        """Integrate design system into the project.
        
        Args:
            design_system: The design system to integrate
            auto_install: Whether to automatically install dependencies (default: False for safety)
            explicit_framework: Explicitly specify framework instead of auto-detecting
            
        Returns:
            Dictionary with integration results
        """
        results = {
            "framework": self.detect_framework(explicit_framework),
            "package_manager": self.detect_package_manager(),
            "files_created": [],
            "files_modified": [],
            "dependencies_added": [],
            "errors": [],
            "warnings": [],
            "instructions": []
        }
        
        # Validate project directory
        if not self.project_dir.exists():
            results["errors"].append(f"Project directory does not exist: {self.project_dir}")
            return results
        
        if not self.project_dir.is_dir():
            results["errors"].append(f"Path is not a directory: {self.project_dir}")
            return results
        
        # Check for package.json
        package_json = self.project_dir / "package.json"
        if not package_json.exists():
            results["warnings"].append("No package.json found. This may not be a valid project directory.")
        
        if not results["framework"]:
            results["errors"].append("Could not detect framework. Please specify with --framework option.")
            results["instructions"].append("Available frameworks: nextjs, vite, cra, vue")
            return results
        
        try:
            # Create necessary directories
            try:
                (self.project_dir / "src" / "styles").mkdir(parents=True, exist_ok=True)
                (self.project_dir / "src" / "components").mkdir(parents=True, exist_ok=True)
                (self.project_dir / "design-system").mkdir(exist_ok=True)
            except PermissionError as e:
                results["errors"].append(f"Permission denied creating directories: {str(e)}")
                return results
            except OSError as e:
                results["errors"].append(f"Error creating directories: {str(e)}")
                return results
            
            # Save design system JSON
            try:
                ds_file = self.project_dir / "design-system" / "design-system.json"
                with open(ds_file, 'w') as f:
                    json.dump(design_system.model_dump(), f, indent=2)
                results["files_created"].append(str(ds_file.relative_to(self.project_dir)))
            except (IOError, OSError) as e:
                results["errors"].append(f"Error saving design system file: {str(e)}")
                return results
            
            # Generate CSS variables
            try:
                from templates.components.generator import ComponentGenerator
                comp_gen = ComponentGenerator(design_system.tokens)
                css_vars = comp_gen.generate_css_variables()
                
                css_file = self.project_dir / "src" / "styles" / "tokens.css"
                with open(css_file, 'w') as f:
                    f.write(css_vars)
                results["files_created"].append(str(css_file.relative_to(self.project_dir)))
            except Exception as e:
                results["errors"].append(f"Error generating CSS variables: {str(e)}")
                return results
            
            # Framework-specific integration
            try:
                if results["framework"] == "nextjs":
                    self._integrate_nextjs(design_system, comp_gen, results)
                elif results["framework"] == "vite":
                    self._integrate_vite(design_system, comp_gen, results)
                elif results["framework"] == "cra":
                    self._integrate_cra(design_system, comp_gen, results)
                elif results["framework"] == "vue":
                    self._integrate_vue(design_system, comp_gen, results)
            except Exception as e:
                results["errors"].append(f"Error in framework-specific integration: {str(e)}")
            
            # Generate setup instructions
            self._generate_setup_instructions(results, auto_install)
            
            # Install dependencies if requested
            if auto_install and results["dependencies_added"]:
                self._install_dependencies(results)
            
        except Exception as e:
            results["errors"].append(f"Integration error: {str(e)}")
        
        return results
    
    def _generate_setup_instructions(self, results: Dict, auto_install: bool):
        """Generate manual setup instructions."""
        pm = results["package_manager"]
        deps = results["dependencies_added"]
        
        if deps:
            deps_str = " ".join(deps)
            if pm == "npm":
                install_cmd = f"npm install -D {deps_str}"
            elif pm == "yarn":
                install_cmd = f"yarn add -D {deps_str}"
            elif pm == "pnpm":
                install_cmd = f"pnpm add -D {deps_str}"
            else:
                install_cmd = f"npm install -D {deps_str}"
            
            if not auto_install:
                results["instructions"].append(f"Install dependencies: {install_cmd}")
        
        # Framework-specific instructions
        if results["framework"] == "nextjs":
            results["instructions"].append("Import tokens.css in your app/layout.tsx or pages/_app.tsx")
            results["instructions"].append("Example: import '@/src/styles/tokens.css'")
        elif results["framework"] == "vite":
            results["instructions"].append("Import tokens.css in your main.tsx or main.js")
            results["instructions"].append("Example: import './styles/tokens.css'")
        elif results["framework"] == "cra":
            results["instructions"].append("Import tokens.css in your src/index.tsx or src/index.js")
            results["instructions"].append("Example: import './styles/tokens.css'")
        
        results["instructions"].append("Start using your design system tokens in components!")
    
    def _integrate_nextjs(self, design_system: DesignSystemOutput, comp_gen: Any, results: Dict):
        """Integrate with Next.js project."""
        # Update or create tailwind.config.js
        tailwind_config = comp_gen.generate_tailwind_config()
        tailwind_file = self.project_dir / "tailwind.config.js"
        tailwind_ts_file = self.project_dir / "tailwind.config.ts"
        
        # Prefer TypeScript config if it exists
        config_file = tailwind_ts_file if tailwind_ts_file.exists() else tailwind_file
        
        if config_file.exists():
            # Create backup
            try:
                with open(config_file) as f:
                    existing = f.read()
                backup_file = config_file.with_suffix(config_file.suffix + '.bak')
                with open(backup_file, 'w') as f:
                    f.write(existing)
                results["warnings"].append(f"Backed up existing config to {backup_file.name}")
            except Exception as e:
                results["warnings"].append(f"Could not backup existing config: {str(e)}")
            
            results["files_modified"].append(str(config_file.relative_to(self.project_dir)))
        else:
            results["files_created"].append(str(config_file.relative_to(self.project_dir)))
        
        try:
            with open(config_file, 'w') as f:
                f.write(tailwind_config)
        except (IOError, OSError) as e:
            results["errors"].append(f"Error writing Tailwind config: {str(e)}")
            return
        
        # Update global CSS
        globals_css = self.project_dir / "app" / "globals.css"
        if not globals_css.exists():
            globals_css = self.project_dir / "styles" / "globals.css"
        
        if globals_css.exists():
            with open(globals_css) as f:
                content = f.read()
            if "@import" not in content and "tokens.css" not in content:
                with open(globals_css, 'a') as f:
                    f.write(f"\n@import '../src/styles/tokens.css';\n")
                results["files_modified"].append(str(globals_css.relative_to(self.project_dir)))
        else:
            # Create new globals.css
            globals_css.parent.mkdir(parents=True, exist_ok=True)
            with open(globals_css, 'w') as f:
                f.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\n")
                f.write("@import '../src/styles/tokens.css';\n")
            results["files_created"].append(str(globals_css.relative_to(self.project_dir)))
        
        # Add dependencies
        results["dependencies_added"].extend([
            "tailwindcss", "postcss", "autoprefixer"
        ])
    
    def _integrate_vite(self, design_system: DesignSystemOutput, comp_gen: Any, results: Dict):
        """Integrate with Vite project."""
        # Similar to Next.js but for Vite
        tailwind_config = comp_gen.generate_tailwind_config()
        tailwind_file = self.project_dir / "tailwind.config.js"
        
        if not tailwind_file.exists():
            with open(tailwind_file, 'w') as f:
                f.write(tailwind_config)
            results["files_created"].append(str(tailwind_file.relative_to(self.project_dir)))
        
        # Update main CSS
        main_css = self.project_dir / "src" / "main.css"
        if main_css.exists():
            with open(main_css) as f:
                content = f.read()
            if "tokens.css" not in content:
                with open(main_css, 'a') as f:
                    f.write(f"\n@import './styles/tokens.css';\n")
                results["files_modified"].append(str(main_css.relative_to(self.project_dir)))
        
        results["dependencies_added"].extend([
            "tailwindcss", "postcss", "autoprefixer"
        ])
    
    def _integrate_cra(self, design_system: DesignSystemOutput, comp_gen: Any, results: Dict):
        """Integrate with Create React App."""
        # Update index.css
        index_css = self.project_dir / "src" / "index.css"
        if index_css.exists():
            with open(index_css) as f:
                content = f.read()
            if "tokens.css" not in content:
                with open(index_css, 'a') as f:
                    f.write(f"\n@import './styles/tokens.css';\n")
                results["files_modified"].append(str(index_css.relative_to(self.project_dir)))
        
        results["dependencies_added"].extend([
            "tailwindcss", "postcss", "autoprefixer"
        ])
    
    def _integrate_vue(self, design_system: DesignSystemOutput, comp_gen: Any, results: Dict):
        """Integrate with Vue project."""
        # Update main.js or main.ts
        main_file = self.project_dir / "src" / "main.js"
        if not main_file.exists():
            main_file = self.project_dir / "src" / "main.ts"
        
        if main_file.exists():
            with open(main_file) as f:
                content = f.read()
            if "tokens.css" not in content:
                with open(main_file, 'a') as f:
                    f.write(f"\nimport './styles/tokens.css';\n")
                results["files_modified"].append(str(main_file.relative_to(self.project_dir)))
        
        results["dependencies_added"].extend([
            "tailwindcss", "postcss", "autoprefixer"
        ])
    
    def _install_dependencies(self, results: Dict):
        """Install required dependencies.
        
        Note: This is disabled by default for security. Users should install manually.
        """
        if not results["dependencies_added"]:
            return
        
        pm = results["package_manager"]
        deps = " ".join(results["dependencies_added"])
        
        # Check if package manager is available
        try:
            if pm == "npm":
                subprocess.run(["npm", "--version"], check=True, capture_output=True)
            elif pm == "yarn":
                subprocess.run(["yarn", "--version"], check=True, capture_output=True)
            elif pm == "pnpm":
                subprocess.run(["pnpm", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            results["warnings"].append(f"{pm} not found. Please install dependencies manually.")
            results["instructions"].append(f"Run: {pm} install -D {deps}")
            return
        
        try:
            if pm == "npm":
                result = subprocess.run(
                    ["npm", "install", "-D"] + results["dependencies_added"], 
                    cwd=self.project_dir, 
                    check=True,
                    capture_output=True,
                    text=True
                )
            elif pm == "yarn":
                result = subprocess.run(
                    ["yarn", "add", "-D"] + results["dependencies_added"],
                    cwd=self.project_dir, 
                    check=True,
                    capture_output=True,
                    text=True
                )
            elif pm == "pnpm":
                result = subprocess.run(
                    ["pnpm", "add", "-D"] + results["dependencies_added"],
                    cwd=self.project_dir, 
                    check=True,
                    capture_output=True,
                    text=True
                )
        except subprocess.CalledProcessError as e:
            results["errors"].append(f"Failed to install dependencies: {str(e)}")
            if e.stderr:
                results["errors"].append(f"Error output: {e.stderr}")
            results["instructions"].append(f"Please run manually: {pm} install -D {deps}")
        except Exception as e:
            results["errors"].append(f"Unexpected error installing dependencies: {str(e)}")
            results["instructions"].append(f"Please run manually: {pm} install -D {deps}")
