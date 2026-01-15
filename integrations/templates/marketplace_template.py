"""Marketplace starter template generator."""

from pathlib import Path
from models import DesignSystemOutput


class MarketplaceTemplate:
    """Generates a marketplace starter project with design system."""
    
    def generate(self, design_system: DesignSystemOutput, output_dir: Path):
        """Generate marketplace project structure."""
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
        
        # Generate app layout
        layout = self._generate_layout()
        with open(output_dir / "app" / "layout.tsx", 'w') as f:
            f.write(layout)
        
        # Generate home page with product listing
        home = self._generate_home()
        with open(output_dir / "app" / "page.tsx", 'w') as f:
            f.write(home)
        
        # Generate product page
        product = self._generate_product()
        (output_dir / "app" / "products").mkdir(exist_ok=True)
        with open(output_dir / "app" / "products" / "[id]" / "page.tsx", 'w') as f:
            f.write(product)
        
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
    
    def _generate_package_json(self) -> str:
        return '''{
  "name": "marketplace-starter",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "next": "^14.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
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
    
    def _generate_layout(self) -> str:
        return '''import type { Metadata } from 'next';
import '../styles/globals.css';

export const metadata: Metadata = {
  title: 'Marketplace',
  description: 'Marketplace application',
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
    
    def _generate_home(self) -> str:
        return '''export default function Home() {
  return (
    <main className="min-h-screen">
      <div className="max-w-7xl mx-auto py-8 px-4">
        <h1 className="text-4xl font-bold mb-8">Marketplace</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="bg-white rounded-lg shadow p-6">
              <div className="h-48 bg-gray-200 rounded mb-4"></div>
              <h2 className="text-lg font-semibold mb-2">Product {i}</h2>
              <p className="text-gray-600 mb-4">Product description</p>
              <div className="flex justify-between items-center">
                <span className="text-xl font-bold">$99.99</span>
                <button className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
                  Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
'''
    
    def _generate_product(self) -> str:
        return '''export default function ProductPage({ params }: { params: { id: string } }) {
  return (
    <main className="min-h-screen">
      <div className="max-w-4xl mx-auto py-8 px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-gray-200 rounded-lg h-96"></div>
          <div>
            <h1 className="text-3xl font-bold mb-4">Product Name</h1>
            <p className="text-2xl font-bold mb-4">$99.99</p>
            <p className="text-gray-600 mb-6">Product description goes here.</p>
            <button className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700">
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
'''
