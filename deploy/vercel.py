"""Vercel deployment automation."""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional


class VercelDeployer:
    """Handles Vercel deployment setup and execution."""
    
    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir).resolve()
    
    def setup_vercel(self, framework: str = "nextjs") -> Dict[str, Any]:
        """Set up Vercel configuration."""
        vercel_json = {
            "version": 2,
            "builds": [],
            "routes": [],
            "framework": framework
        }
        
        if framework == "nextjs":
            vercel_json["builds"] = [
                {
                    "src": "package.json",
                    "use": "@vercel/next"
                }
            ]
        elif framework == "vite":
            vercel_json["builds"] = [
                {
                    "src": "package.json",
                    "use": "@vercel/static-build",
                    "config": {
                        "distDir": "dist"
                    }
                }
            ]
            vercel_json["routes"] = [
                {
                    "src": "/(.*)",
                    "dest": "/index.html"
                }
            ]
        
        vercel_file = self.project_dir / "vercel.json"
        try:
            with open(vercel_file, 'w') as f:
                json.dump(vercel_json, f, indent=2)
            return {"success": True, "file": str(vercel_file.relative_to(self.project_dir))}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def deploy(self, production: bool = False) -> Dict[str, Any]:
        """Deploy to Vercel."""
        try:
            # Check if Vercel CLI is installed
            result = subprocess.run(
                ["vercel", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                "success": False,
                "error": "Vercel CLI not found. Install it with: npm i -g vercel",
                "instructions": [
                    "Install Vercel CLI: npm i -g vercel",
                    "Login to Vercel: vercel login",
                    f"Deploy: vercel {'--prod' if production else ''}"
                ]
            }
        
        try:
            cmd = ["vercel", "--prod"] if production else ["vercel"]
            result = subprocess.run(
                cmd,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Try to extract URL from output
            url = None
            for line in result.stdout.split('\n'):
                if 'https://' in line and 'vercel.app' in line:
                    url = line.strip()
                    break
            
            return {
                "success": True,
                "url": url,
                "output": result.stdout
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": str(e),
                "output": e.stderr or e.stdout,
                "instructions": [
                    "Make sure you're logged in: vercel login",
                    "Check your project configuration",
                    f"Try deploying manually: vercel {'--prod' if production else ''}"
                ]
            }
