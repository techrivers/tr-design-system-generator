# 🛠️ Development Guide

Complete guide for developing and contributing to the Design System Generator.

## Table of Contents

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Adding New Components](#adding-new-components)
- [Testing](#testing)
- [Code Style](#code-style)
- [Performance Optimization](#performance-optimization)
- [Debugging](#debugging)
- [Contributing](#contributing)

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+ (for component library testing)
- Git
- Virtual environment tool (venv, conda, etc.)

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd design-system-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from main import DesignSystemGenerator; print('✅ Setup complete')"
```

### First Run

```bash
# Start development server
uvicorn web.app:app --reload --host 0.0.0.0 --port 8000

# Open browser to http://localhost:8000

# Test with a simple generation
python -c "
from main import DesignSystemGenerator
from models import DesignSystemInput, TargetUser, BrandTrait, Platform

gen = DesignSystemGenerator()
result = gen.generate_design_system(DesignSystemInput(
    product_idea='Test app',
    target_users=[TargetUser.B2B],
    brand_traits=[BrandTrait.MODERN],
    platforms=[Platform.WEB]
))
print(f'Generated {len(result.component_library.components)} components')
"
```

## Project Structure

```
design-system-agent/
├── main.py                 # Main application entry point
├── models.py               # Pydantic data models
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── docs/                  # Documentation files
│   ├── API_REFERENCE.md   # API documentation
│   ├── ARCHITECTURE.md    # Architecture overview
│   ├── COMPONENTS.md      # Component documentation
│   ├── DEPLOYMENT.md      # Deployment guide
│   ├── DEVELOPMENT.md     # This file
│   └── TROUBLESHOOTING.md # Troubleshooting guide
├── agents/                 # AI agent implementations
│   ├── __init__.py
│   ├── design_strategist/
│   │   ├── __init__.py
│   │   └── agent.py       # Design strategy agent
│   ├── visual_identity/
│   │   ├── __init__.py
│   │   └── agent.py       # Visual identity agent
│   └── component_architect/
│       ├── __init__.py
│       └── agent.py       # Component architect agent
├── templates/             # Code generation templates
│   └── components/
│       ├── __init__.py
│       └── generator.py   # Component code generator
├── web/                   # Web interface
│   ├── __init__.py
│   ├── app.py            # FastAPI application
│   └── templates/
│       └── index.html    # Web interface template
└── tests/                 # Test suite (if exists)
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/new-component-type
```

### 2. Make Changes

Follow the patterns established in the codebase:
- Use type hints for all Python functions
- Follow Pydantic model conventions
- Maintain consistent naming conventions
- Add comprehensive error handling

### 3. Test Changes

```bash
# Run existing tests
python -m pytest tests/ -v

# Test your changes manually
python -c "
# Test your new functionality
from main import DesignSystemGenerator
# ... test code ...
"

# Test web interface
uvicorn web.app:app --reload
# Visit http://localhost:8000 and test manually
```

### 4. Update Documentation

```bash
# Update relevant docs in docs/ directory
# Update README.md if needed
# Add code examples and API documentation
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add new component type

- Add ComponentName component with variants
- Update component architect to include new component
- Add Storybook stories and Jest tests
- Update documentation

Closes #123"
```

### 6. Create Pull Request

```bash
git push origin feature/new-component-type
# Create PR on GitHub/GitLab
```

## Adding New Components

### Step 1: Define Component Specification

Add to `agents/component_architect/agent.py`:

```python
ComponentSpec(
    name="NewComponent",
    category="input",  # or "feedback", "navigation", "data", "layout"
    variants=["default", "variant1", "variant2"],
    states=["default", "hover", "disabled", "loading"],
    description="Description of the component's purpose",
    accessibility_notes="Specific accessibility requirements"
)
```

### Step 2: Implement Component Generator

Add to `templates/components/generator.py`:

```python
def generate_new_component(self, spec: ComponentSpec) -> str:
    """Generate a NewComponent."""
    return '''import React from 'react';

interface NewComponentProps {
  variant?: 'default' | 'variant1' | 'variant2';
  // ... other props
}

export const NewComponent: React.FC<NewComponentProps> = ({
  variant = 'default',
  // ... props
}) => {
  // Component implementation
  return (
    <div className="new-component">
      {/* Component JSX */}
    </div>
  );
};

export default NewComponent;
'''
```

### Step 3: Add Generation Logic

Update `main.py` in the component generation section:

```python
elif component_name == 'newcomponent':
    code = component_gen.generate_new_component(component_spec)
    file_path = f"src/components/NewComponent.tsx"
```

### Step 4: Add Storybook Stories

Add to `templates/components/generator.py`:

```python
def generate_new_component_stories(self) -> str:
    """Generate Storybook stories for NewComponent."""
    return '''import type { Meta, StoryObj } from '@storybook/react';
import { NewComponent } from './NewComponent';

const meta: Meta<typeof NewComponent> = {
  title: 'Components/NewComponent',
  component: NewComponent,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Description of NewComponent.',
      },
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    // default props
  },
};

// Add more story variants...
'''
```

### Step 5: Add Test Generation

Add to `templates/components/generator.py`:

```python
def generate_new_component_tests(self) -> str:
    """Generate Jest tests for NewComponent."""
    return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { NewComponent } from './NewComponent';

describe('NewComponent', () => {
  it('renders correctly', () => {
    render(<NewComponent />);
    expect(screen.getByRole('generic')).toBeInTheDocument();
  });

  // Add more tests...
});
'''
```

### Step 6: Update Documentation

- Add to `docs/COMPONENTS.md` with props reference and examples
- Update `README.md` component count
- Add to API documentation if new endpoints

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html

# Run specific test
python -m pytest tests/test_component_generation.py::test_button_component -v

# Run tests in watch mode
python -m pytest tests/ -v --watch
```

### Writing Tests

#### Unit Tests

```python
import pytest
from main import DesignSystemGenerator
from models import DesignSystemInput

def test_design_system_generation():
    generator = DesignSystemGenerator()
    input_data = DesignSystemInput(
        product_idea="Test product",
        target_users=["B2B"],
        brand_traits=["modern"],
        platforms=["web"]
    )

    result = generator.generate_design_system(input_data)

    assert len(result.component_library.components) > 0
    assert result.principles.philosophy in ["utility-first", "component-first", "brand-led"]
    assert len(result.tokens.colors) > 0
```

#### Integration Tests

```python
def test_full_generation_pipeline():
    # Test complete generation with file output
    generator = DesignSystemGenerator()
    # ... setup test data ...

    result = generator.generate_design_system(input_data)

    # Verify all components have code
    for component in result.component_library.components:
        assert len(component.code) > 0
        assert component.file_path.startswith("src/components/")

    # Verify Storybook files
    assert len(result.component_library.storybook_files) > 0
    assert any(f.name == "main.ts" for f in result.component_library.storybook_files)
```

#### Component Tests

Generated component libraries include Jest tests:

```typescript
// Button.test.tsx
describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('handles click events', async () => {
    const handleClick = jest.fn();
    const user = userEvent.setup();

    render(<Button onClick={handleClick}>Click me</Button>);
    await user.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Test Coverage

Aim for 80%+ coverage across:
- Branches (if/else logic)
- Functions (method calls)
- Lines (code execution)
- Statements (all code paths)

## Code Style

### Python Code Style

Follow PEP 8 with these additions:

```python
# Type hints required
def generate_component(self, spec: ComponentSpec) -> str:
    pass

# Docstrings required
def generate_component(self, spec: ComponentSpec) -> str:
    """Generate a React component from specification.

    Args:
        spec: Component specification with variants and states

    Returns:
        Generated React component as TypeScript string
    """
    pass

# Consistent naming
class DesignSystemGenerator:  # PascalCase for classes
    def generate_design_system(self, input_data):  # snake_case for methods
        pass

# Error handling
try:
    result = self.generate_component(spec)
except Exception as e:
    logger.error(f"Component generation failed: {e}")
    raise GenerationError(f"Failed to generate component: {spec.name}") from e
```

### TypeScript/React Code Style

Generated components follow these patterns:

```typescript
// Interface definitions
interface ComponentProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

// Functional components with hooks
export const Component: React.FC<ComponentProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  children
}) => {
  // Hooks at top
  const [state, setState] = useState(initialState);

  // Event handlers
  const handleClick = () => {
    if (disabled) return;
    onClick?.();
  };

  // Class name logic
  const classes = `base-classes ${variantClasses[variant]} ${sizeClasses[size]}`;

  return (
    <button className={classes} onClick={handleClick} disabled={disabled}>
      {children}
    </button>
  );
};
```

### File Organization

- One component per file
- Related files grouped (Component.tsx, Component.stories.tsx, Component.test.tsx)
- Clear import/export structure
- Consistent file naming

## Performance Optimization

### Generation Performance

```python
# Cache expensive operations
@lru_cache(maxsize=100)
def generate_color_scale(base_color: str, shades: int) -> List[str]:
    # Expensive color calculation
    pass

# Use async where possible
async def generate_large_component_library(self, specs: List[ComponentSpec]):
    # Parallel component generation
    tasks = [self.generate_component_async(spec) for spec in specs]
    return await asyncio.gather(*tasks)
```

### Memory Optimization

```python
# Stream large outputs
def generate_components_stream(self, specs: List[ComponentSpec]):
    for spec in specs:
        component_code = self.generate_component(spec)
        yield component_code  # Don't accumulate in memory

# Clean up large objects
def __del__(self):
    # Clean up caches and large data structures
    self.cache.clear()
    self.large_data = None
```

### Bundle Optimization

Generated component libraries are optimized:

```javascript
// Tree shaking friendly exports
export { Button } from './components/Button';
export { Input } from './components/Input';
// Named exports allow tree shaking
```

## Debugging

### Debug Logging

Enable detailed logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def generate_component(self, spec: ComponentSpec) -> str:
    logger.debug(f"Generating component: {spec.name}")
    logger.debug(f"Variants: {spec.variants}")
    logger.debug(f"States: {spec.states}")

    try:
        code = self._generate_component_code(spec)
        logger.debug(f"Generated {len(code)} characters")
        return code
    except Exception as e:
        logger.error(f"Component generation failed: {e}")
        raise
```

### Debug Mode

```bash
# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG

# Start with verbose logging
uvicorn web.app:app --log-level debug
```

### Breakpoint Debugging

```python
# Add debug breakpoints
import pdb; pdb.set_trace()

def debug_component_generation(self, spec: ComponentSpec):
    print(f"Debug: Generating {spec.name}")
    print(f"Debug: Variants = {spec.variants}")
    # Add breakpoint here
    breakpoint()
    return self.generate_component(spec)
```

### Visual Debugging

For web interface debugging:

```javascript
// Add to web interface
console.log('Generated components:', result.component_library.components.length);
console.log('Design tokens:', result.tokens);

// Inspect generated code
console.log('Button component code:', result.component_library.components[0].code);
```

## Contributing

### Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Add tests** for new functionality
5. **Update documentation**
6. **Ensure** all tests pass
7. **Submit** pull request

### Commit Message Convention

```bash
# Format: type(scope): description

feat(components): add DatePicker component with calendar interface
fix(api): resolve CORS issue in web interface
docs(readme): update component count and examples
test(button): add loading state tests
refactor(generator): optimize component generation performance
```

### Code Review Checklist

- [ ] Type hints added for all Python functions
- [ ] Pydantic models validated
- [ ] Error handling implemented
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Code style consistent
- [ ] Performance considerations addressed
- [ ] Security implications reviewed

### Issue Reporting

Use GitHub issues for:
- Bug reports with reproduction steps
- Feature requests with use cases
- Documentation improvements
- Performance issues

**Bug Report Template:**
```markdown
## Bug Description
Clear description of the issue

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., macOS 12.0]
- Python: [e.g., 3.9]
- Browser: [e.g., Chrome 91]

## Additional Context
Any other information
```

This development guide provides everything needed to contribute effectively to the Design System Generator project.

