# 🔧 Troubleshooting Guide

Comprehensive troubleshooting guide for the Design System Generator.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Runtime Errors](#runtime-errors)
- [Generation Problems](#generation-problems)
- [Web Interface Issues](#web-interface-issues)
- [Component Library Issues](#component-library-issues)
- [Performance Issues](#performance-issues)
- [Testing Problems](#testing-problems)
- [Deployment Issues](#deployment-issues)
- [Common Error Messages](#common-error-messages)
- [Debug Tools](#debug-tools)

## Installation Issues

### Python Virtual Environment Problems

**Issue:** `python3 -m venv venv` fails

**Solutions:**
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Install venv if missing
sudo apt install python3-venv  # Ubuntu/Debian
brew install python  # macOS

# Alternative: use conda
conda create -n design-system python=3.11
conda activate design-system
```

**Issue:** Permission denied when creating venv

**Solutions:**
```bash
# Don't use system Python
which python3  # Should not be /usr/bin/python3

# Or use user directory
python3 -m venv ~/.venvs/design-system
source ~/.venvs/design-system/bin/activate
```

### Dependency Installation Failures

**Issue:** `pip install -r requirements.txt` fails

**Solutions:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install in stages
pip install fastapi uvicorn pydantic
pip install -r requirements.txt

# Use alternative mirror
pip install -r requirements.txt -i https://pypi.org/simple/

# Check for conflicting packages
pip check
```

**Issue:** tiktoken installation fails (Rust compiler needed)

**Solutions:**
```bash
# This is expected - tiktoken requires Rust
# The system works without it for basic functionality

# If you need tiktoken (for future AI features):
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
pip install tiktoken
```

### Node.js Issues

**Issue:** Node.js not found for component library testing

**Solutions:**
```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Or use nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
```

## Runtime Errors

### Import Errors

**Issue:** `ModuleNotFoundError: No module named 'agents'`

**Solutions:**
```python
# Check current directory
pwd  # Should be /path/to/design-system-agent

# Check Python path
python -c "import sys; print(sys.path)"

# Fix relative imports
export PYTHONPATH=$PWD:$PYTHONPATH

# Or run from correct directory
cd /path/to/design-system-agent
python main.py
```

**Issue:** `ImportError: cannot import name 'DesignSystemInput'`

**Solutions:**
```python
# Check models.py exists
ls models.py

# Check syntax errors
python -m py_compile models.py

# Reinstall in development mode
pip install -e .
```

### FastAPI Startup Issues

**Issue:** `uvicorn web.app:app` fails

**Solutions:**
```bash
# Check port availability
lsof -i :8000

# Use different port
uvicorn web.app:app --port 8001

# Check for syntax errors
python -c "from web.app import app; print('App loaded successfully')"

# Enable debug logging
uvicorn web.app:app --log-level debug
```

### Memory Errors

**Issue:** `MemoryError` during generation

**Solutions:**
```bash
# Increase system memory limits
echo 'vm.overcommit_memory=1' >> /etc/sysctl.conf
sysctl -p

# Use smaller batch processing
export BATCH_SIZE=5

# Add memory monitoring
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"
```

## Generation Problems

### Empty or Incomplete Generation

**Issue:** Component generation returns empty results

**Debug Steps:**
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test individual agents
from agents.design_strategist.agent import DesignStrategistAgent
strategist = DesignStrategistAgent()
principles = strategist.analyze_product_requirements(input_data)
print("Principles:", principles)

# Test visual identity
from agents.visual_identity.agent import VisualIdentityAgent
visual = VisualIdentityAgent()
tokens = visual.generate_design_tokens(principles)
print("Tokens generated:", len(tokens.colors))
```

**Common Causes:**
- Invalid input data (check Pydantic validation)
- Agent logic errors (check decision trees)
- Template rendering issues (check string formatting)

### Template Rendering Errors

**Issue:** `KeyError` or `TypeError` in template generation

**Solutions:**
```python
# Check template data structure
component_spec = {
    "name": "Button",
    "variants": ["primary", "secondary"],
    "states": ["default", "hover", "disabled"]
}

# Validate before passing to template
assert "name" in component_spec
assert isinstance(component_spec["variants"], list)

# Debug template rendering
try:
    code = generator.generate_button_component(component_spec)
except Exception as e:
    print(f"Template error: {e}")
    print(f"Component spec: {component_spec}")
```

### Color Generation Issues

**Issue:** Invalid color values generated

**Debug:**
```python
from templates.components.generator import ComponentGenerator

gen = ComponentGenerator(None)
colors = gen._generate_color_scale("#3b82f6", 9)
print("Generated colors:", colors)

# Validate hex format
import re
for color in colors:
    assert re.match(r'^#[0-9a-fA-F]{6}$', color), f"Invalid color: {color}"
```

## Web Interface Issues

### CORS Errors

**Issue:** Browser blocks API requests

**Solutions:**
```python
# Add CORS middleware to FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Static File Issues

**Issue:** CSS/JS files not loading

**Solutions:**
```python
# Check static file mounting
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Verify file paths
ls web/static/
ls web/templates/
```

### Form Submission Issues

**Issue:** Form data not processed correctly

**Debug:**
```javascript
// Add to browser console
const form = document.getElementById('designSystemForm');
const formData = new FormData(form);

for (let [key, value] of formData.entries()) {
    console.log(key, value);
}

// Check API endpoint
fetch('/generate', {
    method: 'POST',
    body: formData
}).then(r => r.json()).then(console.log);
```

## Component Library Issues

### Build Failures

**Issue:** Generated component library won't build

**Solutions:**
```bash
# Check generated package.json
cat generated/*/package.json

# Install dependencies
cd generated/component-library
npm install

# Check for syntax errors
npx tsc --noEmit

# Try building
npm run build
```

### Storybook Startup Issues

**Issue:** `npm run storybook` fails

**Solutions:**
```bash
# Clear cache
rm -rf node_modules/.cache

# Check Storybook config
cat .storybook/main.ts

# Install Storybook CLI
npx storybook@latest init --yes

# Start with verbose logging
npm run storybook -- --loglevel verbose
```

### Test Execution Problems

**Issue:** Jest tests fail

**Solutions:**
```bash
# Check test setup
cat src/setupTests.ts

# Run tests with verbose output
npm test -- --verbose

# Check for missing dependencies
npm ls @testing-library/react

# Debug specific test
npm test -- Button.test.tsx
```

## Performance Issues

### Slow Generation

**Issue:** Generation takes >30 seconds

**Optimization Steps:**
```python
# Enable caching
import functools
@functools.lru_cache(maxsize=100)
def generate_component_cached(self, spec_json: str):
    spec = ComponentSpec.parse_raw(spec_json)
    return self.generate_component(spec)

# Profile performance
import cProfile
cProfile.run('generator.generate_design_system(input_data)', 'profile.stats')

# Analyze bottlenecks
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative').print_stats(10)
```

### High Memory Usage

**Issue:** Memory usage >1GB during generation

**Solutions:**
```python
# Use streaming for large outputs
def generate_components_stream(self, specs):
    for spec in specs:
        yield self.generate_component(spec)

# Clear caches periodically
import gc
gc.collect()

# Monitor memory
import tracemalloc
tracemalloc.start()
# ... generation code ...
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
```

### Large Bundle Sizes

**Issue:** Generated component library is too large

**Optimization:**
```javascript
// Enable tree shaking
export { Button } from './Button';  // Named exports

// Code splitting
const Button = lazy(() => import('./Button'));
const Input = lazy(() => import('./Input'));

// Compression
// Add to build config
plugins: [
    terser({
        compress: { drop_console: true },
        mangle: true
    })
]
```

## Testing Problems

### Test Discovery Issues

**Issue:** Tests not found or not running

**Solutions:**
```bash
# Check Jest configuration
cat jest.config.js

# Run test discovery
npx jest --listTests

# Check test file patterns
find src -name "*.test.tsx" -o -name "*.spec.tsx"

# Run with different patterns
npx jest --testPathPattern=Button --verbose
```

### Async Test Issues

**Issue:** Async tests timing out

**Solutions:**
```typescript
// Use async/await properly
it('handles async operations', async () => {
    const user = userEvent.setup();
    render(<AsyncComponent />);

    await user.click(screen.getByRole('button'));
    await waitFor(() => {
        expect(screen.getByText('Loaded')).toBeInTheDocument();
    });
});

// Increase timeout
it('slow async operation', async () => {
    // ... test code ...
}, 10000); // 10 second timeout
```

### Coverage Issues

**Issue:** Coverage reports inaccurate or missing

**Solutions:**
```javascript
// Update Jest config
collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.stories.{ts,tsx}',
    '!src/**/*.d.ts',
],

// Run coverage
npm run test:coverage

// View HTML report
open coverage/lcov-report/index.html
```

## Deployment Issues

### Docker Build Failures

**Issue:** Docker build fails

**Debug:**
```bash
# Test Dockerfile locally
docker build -t test-build .

# Check build logs
docker build -t test-build . --progress=plain

# Test container
docker run -p 8000:8000 test-build
docker logs <container-id>
```

### Kubernetes Deployment Issues

**Issue:** Pods failing to start

**Debug:**
```bash
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name> --previous

# Check resource limits
kubectl describe node <node-name>

# Debug with temporary pod
kubectl run debug-pod --image=busybox --rm -it -- sh
```

### Load Balancer Issues

**Issue:** Traffic not reaching application

**Debug:**
```bash
# Check service endpoints
kubectl get endpoints

# Test service directly
kubectl port-forward service/design-system-service 8080:80

# Check ingress configuration
kubectl get ingress
kubectl describe ingress <ingress-name>
```

## Common Error Messages

### Python Errors

**`TypeError: 'NoneType' object is not subscriptable`**
```python
# Check for None values before accessing
if data is not None and 'key' in data:
    value = data['key']
```

**`AttributeError: module 'xyz' has no attribute 'abc'`**
```python
# Check import statements
from models import DesignSystemInput  # Correct
# vs
import models  # Incorrect usage
```

**`ValidationError: 1 validation error for DesignSystemInput`**
```python
# Check Pydantic model requirements
input_data = DesignSystemInput(
    product_idea="Test",  # Required field
    target_users=["B2B"],  # Must be list
    brand_traits=["modern"],  # Must be list
    platforms=["web"]  # Must be list
)
```

### JavaScript/TypeScript Errors

**`Cannot find module 'xyz'`**
```typescript
// Check import paths
import { Button } from '../components/Button';  // Correct
// vs
import { Button } from 'components/Button';  // Wrong base path
```

**`Property 'xyz' does not exist on type`**
```typescript
// Check interface definitions
interface ButtonProps {
    variant?: 'primary' | 'secondary';  // Must include all variants
    onClick?: () => void;
}
```

### API Errors

**`422 Unprocessable Entity`**
```json
{
  "detail": [
    {
      "loc": ["body", "product_idea"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```
**Fix:** Ensure all required fields are provided in request.

**`500 Internal Server Error`**
- Check application logs
- Verify input data format
- Test with minimal input
- Check for None values in processing

## Debug Tools

### Python Debugging

```python
# PDB debugger
import pdb; pdb.set_trace()

# IPython for interactive debugging
from IPython import embed; embed()

# Logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Web Interface Debugging

```javascript
// Console logging
console.log('Debug info:', data);

// Network inspection
fetch('/generate', { /* request */ })
    .then(r => r.json())
    .then(data => console.log('Response:', data))
    .catch(e => console.error('Error:', e));

// React DevTools
// Install from Chrome extensions
// Inspect component state and props
```

### Performance Profiling

```python
# Time execution
import time
start = time.time()
result = generator.generate_design_system(input_data)
elapsed = time.time() - start
print(f"Generation took {elapsed:.2f} seconds")

# Memory profiling
from memory_profiler import profile

@profile
def generate_with_memory_tracking():
    return generator.generate_design_system(input_data)
```

### Network Debugging

```bash
# Test API endpoints
curl -X GET http://localhost:8000/health

curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"product_idea":"test","target_users":["B2B"],"brand_traits":["modern"],"platforms":["web"]}' \
  | jq .

# Check response headers
curl -I http://localhost:8000/

# Monitor network traffic
tcpdump -i lo0 port 8000
```

This troubleshooting guide covers the most common issues and provides systematic approaches to diagnosing and resolving problems with the Design System Generator.

