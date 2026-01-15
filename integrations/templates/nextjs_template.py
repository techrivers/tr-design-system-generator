"""Next.js starter template generator."""

from pathlib import Path
from typing import Dict, Any
from models import DesignSystemOutput


class NextJSTemplate:
    """Generates a complete Next.js starter project with design system."""
    
    def generate(self, design_system: DesignSystemOutput, output_dir: Path):
        """Generate Next.js project structure."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create directory structure
        (output_dir / "app").mkdir(exist_ok=True)
        (output_dir / "components").mkdir(exist_ok=True)
        (output_dir / "styles").mkdir(exist_ok=True)
        (output_dir / "public").mkdir(exist_ok=True)
        
        # Generate package.json
        package_json = self._generate_package_json()
        with open(output_dir / "package.json", 'w') as f:
            f.write(package_json)
        
        # Generate next.config.js
        next_config = self._generate_next_config()
        with open(output_dir / "next.config.js", 'w') as f:
            f.write(next_config)
        
        # Generate tsconfig.json
        tsconfig = self._generate_tsconfig()
        with open(output_dir / "tsconfig.json", 'w') as f:
            f.write(tsconfig)
        
        # Generate app layout
        layout = self._generate_layout()
        with open(output_dir / "app" / "layout.tsx", 'w') as f:
            f.write(layout)
        
        # Generate app page
        page = self._generate_page()
        with open(output_dir / "app" / "page.tsx", 'w') as f:
            f.write(page)
        
        # Generate global styles
        from templates.components.generator import ComponentGenerator
        comp_gen = ComponentGenerator(design_system.tokens)
        css_vars = comp_gen.generate_css_variables()
        with open(output_dir / "styles" / "globals.css", 'w') as f:
            f.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\n")
            f.write(css_vars)
        
        # Generate tailwind config
        tailwind_config = comp_gen.generate_tailwind_config()
        with open(output_dir / "tailwind.config.js", 'w') as f:
            f.write(tailwind_config)
        
        # Generate README
        readme = self._generate_readme(design_system)
        with open(output_dir / "README.md", 'w') as f:
            f.write(readme)
    
    def _generate_package_json(self) -> str:
        return '''{
  "name": "nextjs-design-system-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "next": "^14.0.0",
    "framer-motion": "^10.16.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0"
  }
}
'''
    
    def _generate_next_config(self) -> str:
        return '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
'''
    
    def _generate_tsconfig(self) -> str:
        return '''{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
'''
    
    def _generate_layout(self) -> str:
        return '''import type { Metadata } from 'next';
import '../styles/globals.css';

export const metadata: Metadata = {
  title: 'Design System App',
  description: 'Next.js app with generated design system',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
'''
    
    def _generate_page(self) -> str:
        return '''import { Button } from '@/components/Button';

export default function Home() {
  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white p-8 rounded-lg shadow-sm">
          <h1 className="text-4xl font-bold mb-4">Welcome to Your Design System</h1>
          <p className="text-lg text-gray-600 mb-8">
            This Next.js app was generated with your design system. Start building amazing experiences!
          </p>
          <div className="flex gap-4">
            <Button variant="primary" onClick={() => alert('Hello!')}>
              Get Started
            </Button>
            <Button variant="secondary">
              Learn More
            </Button>
          </div>
        </div>
        
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-lg font-semibold mb-2">Components</h2>
            <p className="text-gray-600 text-sm">Pre-built React components ready to use</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-lg font-semibold mb-2">Tokens</h2>
            <p className="text-gray-600 text-sm">Design tokens for consistent styling</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-lg font-semibold mb-2">Documentation</h2>
            <p className="text-gray-600 text-sm">Complete documentation and examples</p>
          </div>
        </div>
      </div>
    </main>
  );
}
'''
    
    def _generate_readme(self, design_system: DesignSystemOutput) -> str:
        return f'''# Next.js Design System App

This Next.js application was generated with your design system.

## Getting Started

\`\`\`bash
npm install
npm run dev
\`\`\`

Open [http://localhost:3000](http://localhost:3000) to see your app.

## Design System

- **Product**: {design_system.input.product_idea}
- **Philosophy**: {design_system.principles.philosophy}
- **Components**: {len(design_system.components.components)} components included

## Project Structure

- \`app/\` - Next.js App Router pages
- \`components/\` - React components
- \`styles/\` - Global styles and design tokens
- \`public/\` - Static assets

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Design System Documentation](./docs)
'''