"""Static documentation site generator for design systems."""

from pathlib import Path
from typing import Dict, Any
from models import DesignSystemOutput


class DocsSiteGenerator:
    """Generates a static documentation site for the design system."""
    
    def generate(self, design_system: DesignSystemOutput, output_dir: Path):
        """Generate static documentation site."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create directory structure
        (output_dir / "assets" / "css").mkdir(parents=True, exist_ok=True)
        (output_dir / "assets" / "js").mkdir(parents=True, exist_ok=True)
        
        # Generate index.html
        index_html = self._generate_index(design_system)
        with open(output_dir / "index.html", 'w') as f:
            f.write(index_html)
        
        # Generate tokens page
        tokens_html = self._generate_tokens_page(design_system)
        with open(output_dir / "tokens.html", 'w') as f:
            f.write(tokens_html)
        
        # Generate components page
        components_html = self._generate_components_page(design_system)
        with open(output_dir / "components.html", 'w') as f:
            f.write(components_html)
        
        # Generate guidelines page
        guidelines_html = self._generate_guidelines_page(design_system)
        with open(output_dir / "guidelines.html", 'w') as f:
            f.write(guidelines_html)
        
        # Generate deploy instructions page
        deploy_html = self._generate_deploy_page(design_system)
        with open(output_dir / "deploy.html", 'w') as f:
            f.write(deploy_html)
        
        # Generate CSS
        css = self._generate_css()
        with open(output_dir / "assets" / "css" / "style.css", 'w') as f:
            f.write(css)
        
        # Generate JavaScript
        js = self._generate_js()
        with open(output_dir / "assets" / "js" / "main.js", 'w') as f:
            f.write(js)
    
    def _generate_index(self, design_system: DesignSystemOutput) -> str:
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Design System Documentation - {design_system.input.product_idea[:50]}</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>Design System</h1>
            <ul>
                <li><a href="index.html">Overview</a></li>
                <li><a href="tokens.html">Tokens</a></li>
                <li><a href="components.html">Components</a></li>
                <li><a href="guidelines.html">Guidelines</a></li>
                <li><a href="deploy.html">Deploy</a></li>
            </ul>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search components..." class="search-input">
            </div>
        </div>
    </nav>
    
    <main class="container">
        <section class="hero">
            <h1>Design System Documentation</h1>
            <p class="lead">{design_system.input.product_idea}</p>
        </section>
        
        <section class="principles">
            <h2>Design Principles</h2>
            <div class="grid">
                <div class="card">
                    <h3>Philosophy</h3>
                    <p>{design_system.principles.philosophy}</p>
                </div>
                <div class="card">
                    <h3>Density</h3>
                    <p>{design_system.principles.density}</p>
                </div>
                <div class="card">
                    <h3>Clarity</h3>
                    <p>{design_system.principles.clarity}/10</p>
                </div>
                <div class="card">
                    <h3>Warmth</h3>
                    <p>{design_system.principles.warmth}/10</p>
                </div>
            </div>
        </section>
        
        <section class="stats">
            <h2>System Overview</h2>
            <div class="stats-grid">
                <div class="stat">
                    <div class="stat-value">{len(design_system.tokens.colors)}</div>
                    <div class="stat-label">Color Tokens</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{len(design_system.tokens.typography)}</div>
                    <div class="stat-label">Typography Scales</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{len(design_system.components.components)}</div>
                    <div class="stat-label">Components</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{len(design_system.tokens.spacing)}</div>
                    <div class="stat-label">Spacing Values</div>
                </div>
            </div>
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p>Generated by Technology Rivers Design System Generator</p>
        </div>
    </footer>
    
    <script src="assets/js/main.js"></script>
</body>
</html>
'''
    
    def _generate_tokens_page(self, design_system: DesignSystemOutput) -> str:
        colors_html = ''.join([
            f'<div class="color-swatch"><div class="color-box" style="background: {c.value}"></div><div class="color-name">{c.name}</div><div class="color-value">{c.value}</div></div>'
            for c in design_system.tokens.colors[:20]  # Limit for display
        ])
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Design Tokens - Design System Documentation</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>Design System</h1>
            <ul>
                <li><a href="index.html">Overview</a></li>
                <li><a href="tokens.html">Tokens</a></li>
                <li><a href="components.html">Components</a></li>
                <li><a href="guidelines.html">Guidelines</a></li>
                <li><a href="deploy.html">Deploy</a></li>
            </ul>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search components..." class="search-input">
            </div>
        </div>
    </nav>
    
    <main class="container">
        <h1>Design Tokens</h1>
        
        <section>
            <h2>Colors</h2>
            <div class="color-grid">
                {colors_html}
            </div>
        </section>
        
        <section>
            <h2>Typography</h2>
            <table class="token-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Family</th>
                        <th>Size</th>
                        <th>Weight</th>
                        <th>Line Height</th>
                    </tr>
                </thead>
                <tbody>
                    {' '.join([f'<tr><td>{t.name}</td><td>{t.family}</td><td>{t.size}</td><td>{t.weight}</td><td>{t.line_height}</td></tr>' for t in design_system.tokens.typography])}
                </tbody>
            </table>
        </section>
        
        <section>
            <h2>Spacing</h2>
            <div class="spacing-grid">
                {' '.join([f'<div class="spacing-item"><div class="spacing-box" style="width: {s.value}"></div><div class="spacing-name">{s.name}</div><div class="spacing-value">{s.value}</div></div>' for s in design_system.tokens.spacing])}
            </div>
        </section>
    </main>
    
    <footer>
        <div class="container">
            <p>Generated by Technology Rivers Design System Generator</p>
        </div>
    </footer>
</body>
</html>
'''
    
    def _generate_components_page(self, design_system: DesignSystemOutput) -> str:
        components_list = ''.join([
            f'''<div class="component-card" data-component-name="{c.name.lower()}" data-component-category="{c.category}">
                <div class="component-header">
                    <h3>{c.name}</h3>
                    <span class="component-badge">{c.category or 'general'}</span>
                </div>
                <p class="component-description">{c.description or "A versatile component for your design system."}</p>
                <div class="component-details">
                    <div class="detail-item">
                        <strong>Variants:</strong> {", ".join(c.variants[:5]) if c.variants else "default"}
                        {f"<span class='text-xs text-gray-500'>+{len(c.variants) - 5} more</span>" if c.variants and len(c.variants) > 5 else ""}
                    </div>
                    <div class="detail-item">
                        <strong>States:</strong> {", ".join(c.states) if c.states else "default, hover, focus"}
                    </div>
                </div>
                <div class="component-usage">
                    <h4>Usage Example</h4>
                    <pre class="usage-code"><code>&lt;{c.name} variant="{c.variants[0] if c.variants else 'default'}" /&gt;</code></pre>
                </div>
                <div class="component-guidelines">
                    <h4>When to Use</h4>
                    <ul>
                        <li>Use {c.name.lower()} for {self._get_usage_hint(c.category, c.name)}</li>
                        <li>Choose appropriate variant based on importance</li>
                        <li>Ensure proper accessibility attributes</li>
                    </ul>
                </div>
                {f'<div class="component-accessibility"><h4>Accessibility</h4><p class="text-sm text-gray-600">{c.accessibility_notes or "Follow WCAG 2.1 AA guidelines"}</p></div>' if c.accessibility_notes else ''}
            </div>'''
            for c in design_system.components.components
        ])
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Components - Design System Documentation</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>Design System</h1>
            <ul>
                <li><a href="index.html">Overview</a></li>
                <li><a href="tokens.html">Tokens</a></li>
                <li><a href="components.html">Components</a></li>
                <li><a href="guidelines.html">Guidelines</a></li>
                <li><a href="deploy.html">Deploy</a></li>
            </ul>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search components..." class="search-input">
            </div>
        </div>
    </nav>
    
    <main class="container">
        <div class="page-header">
            <h1>Component Gallery</h1>
            <p class="lead">A comprehensive library of {len(design_system.components.components)} production-ready components with usage guidelines.</p>
            <div class="filter-tabs">
                <button class="filter-tab active" data-filter="all">All</button>
                <button class="filter-tab" data-filter="button">Buttons</button>
                <button class="filter-tab" data-filter="input">Inputs</button>
                <button class="filter-tab" data-filter="navigation">Navigation</button>
                <button class="filter-tab" data-filter="feedback">Feedback</button>
                <button class="filter-tab" data-filter="layout">Layout</button>
            </div>
        </div>
        
        <div class="components-grid" id="componentsGrid">
            {components_list}
        </div>
        <div id="noResults" class="no-results" style="display: none;">
            <p>No components found matching your search.</p>
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p>Generated by Technology Rivers Design System Generator</p>
        </div>
    </footer>
</body>
</html>
'''
    
    def _generate_guidelines_page(self, design_system: DesignSystemOutput) -> str:
        guidelines_html = ''.join([
            f'<div class="guideline-card"><h3>{key}</h3><p>{value}</p></div>'
            for key, value in design_system.guidelines.items()
        ])
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guidelines - Design System Documentation</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>Design System</h1>
            <ul>
                <li><a href="index.html">Overview</a></li>
                <li><a href="tokens.html">Tokens</a></li>
                <li><a href="components.html">Components</a></li>
                <li><a href="guidelines.html">Guidelines</a></li>
                <li><a href="deploy.html">Deploy</a></li>
            </ul>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search components..." class="search-input">
            </div>
        </div>
    </nav>
    
    <main class="container">
        <h1>Design Guidelines</h1>
        <p class="lead">Best practices and usage guidelines for the design system.</p>
        
        <div class="guidelines-grid">
            {guidelines_html}
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p>Generated by Technology Rivers Design System Generator</p>
        </div>
    </footer>
</body>
</html>
'''
    
    def _generate_css(self) -> str:
        return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f9fafb;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.navbar {
    background: white;
    border-bottom: 1px solid #e5e7eb;
    padding: 1rem 0;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar ul {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.navbar a {
    text-decoration: none;
    color: #6366f1;
}

.hero {
    text-align: center;
    padding: 4rem 0;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.lead {
    font-size: 1.25rem;
    color: #6b7280;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.stat {
    text-align: center;
    background: white;
    padding: 2rem;
    border-radius: 8px;
}

.stat-value {
    font-size: 3rem;
    font-weight: bold;
    color: #6366f1;
}

.stat-label {
    color: #6b7280;
    margin-top: 0.5rem;
}

.color-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
    margin-top: 2rem;
}

.color-swatch {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.color-box {
    width: 100%;
    height: 80px;
    border-radius: 4px;
    margin-bottom: 0.5rem;
}

.color-name {
    font-weight: 600;
    margin-bottom: 0.25rem;
}

.color-value {
    font-size: 0.875rem;
    color: #6b7280;
}

.token-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    margin-top: 2rem;
}

.token-table th,
.token-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}

.token-table th {
    background: #f9fafb;
    font-weight: 600;
}

.components-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.component-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.component-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.component-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.component-badge {
    background: #6366f1;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}

.component-description {
    color: #6b7280;
    margin-bottom: 1rem;
}

.component-details {
    margin: 1rem 0;
    padding: 1rem;
    background: #f9fafb;
    border-radius: 4px;
}

.detail-item {
    margin: 0.5rem 0;
    font-size: 0.875rem;
}

.component-usage {
    margin: 1rem 0;
    padding: 1rem;
    background: #1f2937;
    border-radius: 4px;
}

.component-usage h4 {
    color: white;
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
}

.usage-code {
    color: #10b981;
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: 0.875rem;
}

.component-guidelines {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
}

.component-guidelines h4 {
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
    color: #374151;
}

.component-guidelines ul {
    list-style: disc;
    padding-left: 1.5rem;
    color: #6b7280;
    font-size: 0.875rem;
}

.component-guidelines li {
    margin: 0.25rem 0;
}

footer {
    background: white;
    border-top: 1px solid #e5e7eb;
    padding: 2rem 0;
    margin-top: 4rem;
    text-align: center;
    color: #6b7280;
}

.search-box {
    margin-left: 2rem;
}

.search-input {
    padding: 0.5rem 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    font-size: 0.875rem;
    width: 200px;
}

.search-input:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.page-header {
    margin-bottom: 2rem;
}

.filter-tabs {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}

.filter-tab {
    padding: 0.5rem 1rem;
    border: 1px solid #e5e7eb;
    background: white;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.875rem;
    transition: all 0.2s;
}

.filter-tab:hover {
    background: #f9fafb;
}

.filter-tab.active {
    background: #6366f1;
    color: white;
    border-color: #6366f1;
}

.no-results {
    text-align: center;
    padding: 3rem;
    color: #6b7280;
}

.component-accessibility {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
}

.deploy-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.deploy-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.deploy-steps {
    margin: 1rem 0;
    padding-left: 1.5rem;
}

.deploy-steps li {
    margin: 0.5rem 0;
}

.deploy-command {
    background: #f9fafb;
    padding: 1rem;
    border-radius: 6px;
    margin-top: 1rem;
}

.deploy-command code {
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: 0.875rem;
}

.deploy-note {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 2rem;
}

.deploy-note pre {
    background: white;
    padding: 1rem;
    border-radius: 6px;
    margin-top: 0.5rem;
    overflow-x: auto;
}

.usage-code {
    background: #f9fafb;
    padding: 1rem;
    border-radius: 6px;
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: 0.875rem;
    overflow-x: auto;
    border: 1px solid #e5e7eb;
}

.usage-code code {
    color: #1f2937;
}
'''
    
    def _generate_js(self) -> str:
        return '''// Documentation site JavaScript
(function() {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const componentsGrid = document.getElementById('componentsGrid');
    const noResults = document.getElementById('noResults');
    
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const cards = componentsGrid.querySelectorAll('.component-card');
            let visibleCount = 0;
            
            cards.forEach(card => {
                const name = card.getAttribute('data-component-name');
                const category = card.getAttribute('data-component-category');
                const description = card.querySelector('.component-description')?.textContent.toLowerCase() || '';
                
                if (name.includes(query) || category.includes(query) || description.includes(query)) {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
        });
    }
    
    // Filter tabs
    const filterTabs = document.querySelectorAll('.filter-tab');
    filterTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            filterTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            const filter = tab.getAttribute('data-filter');
            const cards = componentsGrid.querySelectorAll('.component-card');
            
            cards.forEach(card => {
                if (filter === 'all') {
                    card.style.display = 'block';
                } else {
                    const category = card.getAttribute('data-component-category');
                    card.style.display = category === filter ? 'block' : 'none';
                }
            });
        });
    });
    
    // Copy code functionality
    document.querySelectorAll('.usage-code').forEach(codeBlock => {
        codeBlock.addEventListener('click', () => {
            const code = codeBlock.textContent;
            navigator.clipboard.writeText(code).then(() => {
                const original = codeBlock.textContent;
                codeBlock.textContent = 'Copied!';
                setTimeout(() => {
                    codeBlock.textContent = original;
                }, 2000);
            });
        });
        codeBlock.style.cursor = 'pointer';
        codeBlock.title = 'Click to copy';
    });
})();
'''
    
    def _get_usage_hint(self, category: str, name: str) -> str:
        """Get usage hint based on category and name."""
        hints = {
            'button': 'primary actions and user interactions',
            'input': 'collecting user input and data entry',
            'navigation': 'helping users navigate through the application',
            'feedback': 'providing feedback and status updates',
            'layout': 'organizing and structuring content',
            'data': 'displaying data and information',
            'contextual': 'contextual actions and menus'
        }
        return hints.get(category, 'various use cases')
    
    def _generate_deploy_page(self, design_system: DesignSystemOutput) -> str:
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deployment - Design System Documentation</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>Design System</h1>
            <ul>
                <li><a href="index.html">Overview</a></li>
                <li><a href="tokens.html">Tokens</a></li>
                <li><a href="components.html">Components</a></li>
                <li><a href="guidelines.html">Guidelines</a></li>
                <li><a href="deploy.html">Deploy</a></li>
            </ul>
        </div>
    </nav>
    
    <main class="container">
        <h1>Deployment Instructions</h1>
        <p class="lead">Deploy your design system documentation to various platforms.</p>
        
        <div class="deploy-options">
            <div class="deploy-card">
                <h2>GitHub Pages</h2>
                <ol class="deploy-steps">
                    <li>Push your documentation to a GitHub repository</li>
                    <li>Go to Settings → Pages</li>
                    <li>Select the branch containing your docs (usually <code>main</code> or <code>gh-pages</code>)</li>
                    <li>Select the folder (usually <code>/docs</code> or <code>/</code>)</li>
                    <li>Your site will be available at <code>https://username.github.io/repository</code></li>
                </ol>
                <div class="deploy-command">
                    <code>git push origin main</code>
                </div>
            </div>
            
            <div class="deploy-card">
                <h2>Vercel</h2>
                <ol class="deploy-steps">
                    <li>Install Vercel CLI: <code>npm i -g vercel</code></li>
                    <li>Navigate to your docs directory</li>
                    <li>Run <code>vercel</code> and follow the prompts</li>
                    <li>Your site will be deployed automatically</li>
                </ol>
                <div class="deploy-command">
                    <code>vercel --prod</code>
                </div>
            </div>
            
            <div class="deploy-card">
                <h2>Netlify</h2>
                <ol class="deploy-steps">
                    <li>Install Netlify CLI: <code>npm i -g netlify-cli</code></li>
                    <li>Navigate to your docs directory</li>
                    <li>Run <code>netlify deploy --prod</code></li>
                    <li>Follow the prompts to complete deployment</li>
                </ol>
                <div class="deploy-command">
                    <code>netlify deploy --prod --dir=.</code>
                </div>
            </div>
        </div>
        
        <div class="deploy-note">
            <h3>💡 Quick Deploy</h3>
            <p>Use the CLI command to generate and deploy:</p>
            <pre><code>tr-ds docs --input design-system.json --deploy</code></pre>
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p>Generated by Technology Rivers Design System Generator</p>
        </div>
    </footer>
    
    <script src="assets/js/main.js"></script>
</body>
</html>
'''
