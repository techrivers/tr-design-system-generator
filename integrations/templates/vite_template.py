"""Vite + React starter template generator."""

from pathlib import Path
from models import DesignSystemOutput


class ViteTemplate:
    """Generates a Vite + React starter project with design system."""
    
    def generate(self, design_system: DesignSystemOutput, output_dir: Path):
        """Generate Vite project structure."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create directory structure
        (output_dir / "src" / "components").mkdir(parents=True, exist_ok=True)
        (output_dir / "src" / "styles").mkdir(parents=True, exist_ok=True)
        (output_dir / "public").mkdir(exist_ok=True)
        
        # Generate package.json
        package_json = self._generate_package_json()
        with open(output_dir / "package.json", 'w') as f:
            f.write(package_json)
        
        # Generate vite.config.ts
        vite_config = self._generate_vite_config()
        with open(output_dir / "vite.config.ts", 'w') as f:
            f.write(vite_config)
        
        # Generate tsconfig.json
        tsconfig = self._generate_tsconfig()
        with open(output_dir / "tsconfig.json", 'w') as f:
            f.write(tsconfig)
        
        # Generate index.html
        index_html = self._generate_index_html()
        with open(output_dir / "index.html", 'w') as f:
            f.write(index_html)
        
        # Generate main.tsx
        main_tsx = self._generate_main_tsx()
        with open(output_dir / "src" / "main.tsx", 'w') as f:
            f.write(main_tsx)
        
        # Generate App.tsx
        app_tsx = self._generate_app_tsx()
        with open(output_dir / "src" / "App.tsx", 'w') as f:
            f.write(app_tsx)
        
        # Generate global styles
        from templates.components.generator import ComponentGenerator
        comp_gen = ComponentGenerator(design_system.tokens)
        css_vars = comp_gen.generate_css_variables()
        with open(output_dir / "src" / "styles" / "globals.css", 'w') as f:
            f.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\n")
            f.write(css_vars)
        
        # Generate tailwind config
        tailwind_config = comp_gen.generate_tailwind_config()
        with open(output_dir / "tailwind.config.js", 'w') as f:
            f.write(tailwind_config)
    
    def _generate_package_json(self) -> str:
        return '''{
  "name": "vite-design-system-app",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "framer-motion": "^10.16.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.0.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
'''
    
    def _generate_vite_config(self) -> str:
        return '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
'''
    
    def _generate_tsconfig(self) -> str:
        return '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
'''
    
    def _generate_index_html(self) -> str:
        return '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Design System App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''
    
    def _generate_main_tsx(self) -> str:
        return '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './styles/globals.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
'''
    
    def _generate_app_tsx(self) -> str:
        return '''import { Button } from './components/Button';

function App() {
  return (
    <div className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-4">Welcome to Your Design System</h1>
        <p className="text-lg text-gray-600 mb-8">
          This Vite + React app was generated with your design system.
        </p>
        <Button variant="primary" onClick={() => alert('Hello!')}>
          Get Started
        </Button>
      </div>
    </div>
  );
}

export default App;
'''