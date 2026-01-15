"""Dashboard starter template generator."""

from pathlib import Path
from models import DesignSystemOutput
from integrations.templates.nextjs_template import NextJSTemplate


class DashboardTemplate(NextJSTemplate):
    """Generates a dashboard starter project with design system."""
    
    def generate(self, design_system: DesignSystemOutput, output_dir: Path):
        """Generate dashboard project structure."""
        # Use Next.js as base
        super().generate(design_system, output_dir)
        
        # Add dashboard-specific files
        self._generate_dashboard_layout(output_dir)
        self._generate_dashboard_page(output_dir)
        self._generate_dashboard_components(output_dir)
    
    def _generate_dashboard_layout(self, output_dir: Path):
        """Generate dashboard layout with sidebar."""
        layout_content = '''import type { Metadata } from 'next';
import '../styles/globals.css';
import { Sidebar } from '@/components/Sidebar';

export const metadata: Metadata = {
  title: 'Dashboard',
  description: 'Analytics dashboard with design system',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex">
        <Sidebar />
        <main className="flex-1">
          {children}
        </main>
      </body>
    </html>
  );
}
'''
        with open(output_dir / "app" / "layout.tsx", 'w') as f:
            f.write(layout_content)
    
    def _generate_dashboard_page(self, output_dir: Path):
        """Generate dashboard page with charts and metrics."""
        dashboard = '''export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Analytics Dashboard</h1>
        
        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500 mb-1">Total Revenue</h3>
            <p className="text-2xl font-bold">$45,231</p>
            <p className="text-sm text-green-600 mt-1">+20.1% from last month</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500 mb-1">Active Users</h3>
            <p className="text-2xl font-bold">2,350</p>
            <p className="text-sm text-green-600 mt-1">+15.3% from last month</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500 mb-1">Conversion Rate</h3>
            <p className="text-2xl font-bold">3.2%</p>
            <p className="text-sm text-red-600 mt-1">-2.4% from last month</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500 mb-1">Avg. Session</h3>
            <p className="text-2xl font-bold">4m 32s</p>
            <p className="text-sm text-green-600 mt-1">+12.5% from last month</p>
          </div>
        </div>
        
        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Revenue Overview</h2>
            <div className="h-64 flex items-center justify-center text-gray-400">
              Chart placeholder
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">User Activity</h2>
            <div className="h-64 flex items-center justify-center text-gray-400">
              Chart placeholder
            </div>
          </div>
        </div>
        
        {/* Recent Activity */}
        <div className="mt-6 bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between py-2 border-b">
              <div>
                <p className="font-medium">New user registered</p>
                <p className="text-sm text-gray-500">2 minutes ago</p>
              </div>
            </div>
            <div className="flex items-center justify-between py-2 border-b">
              <div>
                <p className="font-medium">Payment received</p>
                <p className="text-sm text-gray-500">15 minutes ago</p>
              </div>
            </div>
            <div className="flex items-center justify-between py-2">
              <div>
                <p className="font-medium">Report generated</p>
                <p className="text-sm text-gray-500">1 hour ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
'''
        with open(output_dir / "app" / "page.tsx", 'w') as f:
            f.write(dashboard)
    
    def _generate_dashboard_components(self, output_dir: Path):
        """Generate dashboard-specific components."""
        # Sidebar component
        sidebar = '''export function Sidebar() {
  const menuItems = [
    { label: 'Dashboard', href: '/' },
    { label: 'Analytics', href: '/analytics' },
    { label: 'Reports', href: '/reports' },
    { label: 'Settings', href: '/settings' },
  ];
  
  return (
    <aside className="w-64 bg-white border-r border-gray-200 min-h-screen">
      <div className="p-6">
        <h1 className="text-xl font-bold mb-8">Dashboard</h1>
        <nav className="space-y-2">
          {menuItems.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            >
              {item.label}
            </a>
          ))}
        </nav>
      </div>
    </aside>
  );
}
'''
        with open(output_dir / "components" / "Sidebar.tsx", 'w') as f:
            f.write(sidebar)
