"""SaaS starter template generator."""

from pathlib import Path
from models import DesignSystemOutput
from integrations.templates.nextjs_template import NextJSTemplate


class SaaSTemplate(NextJSTemplate):
    """Generates a SaaS starter project with design system."""
    
    def generate(self, design_system: DesignSystemOutput, output_dir: Path):
        """Generate SaaS project structure."""
        # Use Next.js as base
        super().generate(design_system, output_dir)
        
        # Add SaaS-specific files
        self._generate_saas_layout(output_dir)
        self._generate_saas_pages(output_dir)
        self._generate_saas_components(output_dir)
    
    def _generate_saas_layout(self, output_dir: Path):
        """Generate SaaS layout with navigation."""
        layout_content = '''import type { Metadata } from 'next';
import '../styles/globals.css';
import { Navigation } from '@/components/Navigation';

export const metadata: Metadata = {
  title: 'SaaS App',
  description: 'SaaS application with design system',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Navigation />
        {children}
      </body>
    </html>
  );
}
'''
        with open(output_dir / "app" / "layout.tsx", 'w') as f:
            f.write(layout_content)
    
    def _generate_saas_pages(self, output_dir: Path):
        """Generate SaaS pages (dashboard, settings, etc.)."""
        # Dashboard page
        dashboard = '''export default function Dashboard() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-lg font-semibold mb-2">Total Users</h2>
            <p className="text-3xl font-bold">1,234</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-lg font-semibold mb-2">Revenue</h2>
            <p className="text-3xl font-bold">$12,345</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-lg font-semibold mb-2">Active</h2>
            <p className="text-3xl font-bold">89%</p>
          </div>
        </div>
      </div>
    </main>
  );
}
'''
        (output_dir / "app" / "dashboard").mkdir(exist_ok=True)
        with open(output_dir / "app" / "dashboard" / "page.tsx", 'w') as f:
            f.write(dashboard)
        
        # Settings page
        settings = '''export default function Settings() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold mb-6">Settings</h1>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Account Settings</h2>
          <p className="text-gray-600">Configure your account preferences here.</p>
        </div>
      </div>
    </main>
  );
}
'''
        (output_dir / "app" / "settings").mkdir(exist_ok=True)
        with open(output_dir / "app" / "settings" / "page.tsx", 'w') as f:
            f.write(settings)
    
    def _generate_saas_components(self, output_dir: Path):
        """Generate SaaS-specific components."""
        # Navigation component
        nav = '''export function Navigation() {
  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold">SaaS App</h1>
          </div>
          <div className="flex items-center gap-4">
            <a href="/dashboard" className="text-gray-600 hover:text-gray-900">Dashboard</a>
            <a href="/settings" className="text-gray-600 hover:text-gray-900">Settings</a>
          </div>
        </div>
      </div>
    </nav>
  );
}
'''
        with open(output_dir / "components" / "Navigation.tsx", 'w') as f:
            f.write(nav)
