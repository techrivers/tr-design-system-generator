# 📋 API Reference

Complete API documentation for the Design System Generator.

## Table of Contents

- [Core Classes](#core-classes)
- [Data Models](#data-models)
- [Enums](#enums)
- [Agent Interfaces](#agent-interfaces)
- [Component Generators](#component-generators)
- [Utility Functions](#utility-functions)

## Core Classes

### DesignSystemGenerator

Main orchestrator for the design system generation process.

#### Constructor

```python
DesignSystemGenerator()
```

#### Methods

##### `generate_design_system(input_data: DesignSystemInput) -> DesignSystemOutput`

Generates a complete design system from product requirements.

**Parameters:**
- `input_data` (DesignSystemInput): Product specification and requirements

**Returns:**
- `DesignSystemOutput`: Complete generated design system

**Example:**
```python
from main import DesignSystemGenerator
from models import DesignSystemInput, TargetUser, BrandTrait, Platform

generator = DesignSystemGenerator()
input_data = DesignSystemInput(
    product_idea="A modern analytics dashboard",
    target_users=[TargetUser.B2B, TargetUser.ENTERPRISE],
    brand_traits=[BrandTrait.MODERN, BrandTrait.PROFESSIONAL],
    platforms=[Platform.WEB, Platform.DASHBOARD]
)

result = generator.generate_design_system(input_data)
```

## Data Models

### DesignSystemInput

Input specification for design system generation.

```python
class DesignSystemInput(BaseModel):
    product_idea: str
    target_users: List[TargetUser]
    brand_traits: List[BrandTrait]
    platforms: List[Platform]
```

**Fields:**
- `product_idea` (str): Description of the product and its domain
- `target_users` (List[TargetUser]): Target user types
- `brand_traits` (List[BrandTrait]): Brand personality traits
- `platforms` (List[Platform]): Target platforms

### DesignSystemOutput

Complete generated design system output.

```python
class DesignSystemOutput(BaseModel):
    input: DesignSystemInput
    principles: DesignPrinciples
    tokens: DesignTokens
    components: ComponentInventory
    component_library: ComponentLibrary
    guidelines: Dict[str, str]
    generated_at: str
```

**Fields:**
- `input` (DesignSystemInput): Original input specification
- `principles` (DesignPrinciples): Design philosophy and rules
- `tokens` (DesignTokens): Visual design tokens
- `components` (ComponentInventory): Component specifications
- `component_library` (ComponentLibrary): Generated code and files
- `guidelines` (Dict[str, str]): Usage guidelines
- `generated_at` (str): ISO timestamp of generation

### DesignPrinciples

Core design principles and philosophy.

```python
class DesignPrinciples(BaseModel):
    clarity: int  # 1-10 scale
    density: Literal["dense", "spacious", "balanced"]
    warmth: int   # 1-10 scale
    speed: int    # 1-10 scale
    philosophy: Literal["utility-first", "component-first", "brand-led"]
```

### DesignTokens

Complete visual design token system.

```python
class DesignTokens(BaseModel):
    colors: List[ColorToken]
    typography: List[TypographyToken]
    spacing: List[SpacingToken]
    border_radius: Dict[str, str]
    shadows: Dict[str, str]
```

### ComponentInventory

Complete component specifications.

```python
class ComponentInventory(BaseModel):
    components: List[ComponentSpec]
    reusable_components: List[str]
    contextual_components: List[str]
```

### ComponentLibrary

Generated component library files.

```python
class ComponentLibrary(BaseModel):
    css_variables: str
    tailwind_config: str
    package_json: str
    components: List[ComponentCode]
    index_file: str
    readme: str
    storybook_files: List[StorybookFile]
    test_files: List[TestFile]
```

## Enums

### TargetUser

Target user types for design system adaptation.

```python
class TargetUser(str, Enum):
    B2B = "B2B"              # Business-to-business
    B2C = "B2C"              # Business-to-consumer
    ENTERPRISE = "enterprise" # Large enterprise organizations
    CONSUMER = "consumer"    # Individual consumers
```

### BrandTrait

Brand personality traits for design adaptation.

```python
class BrandTrait(str, Enum):
    MODERN = "modern"         # Contemporary, current
    CLINICAL = "clinical"     # Clean, sterile, medical
    PLAYFUL = "playful"       # Fun, energetic, youthful
    PREMIUM = "premium"       # Luxury, high-end, sophisticated
    BOLD = "bold"            # Strong, confident, impactful
    MINIMAL = "minimal"      # Simple, clean, understated
    WARM = "warm"            # Friendly, approachable, human
    PROFESSIONAL = "professional" # Corporate, trustworthy, serious
```

### Platform

Target platforms for component adaptation.

```python
class Platform(str, Enum):
    WEB = "web"              # Desktop web applications
    MOBILE = "mobile"        # Mobile applications
    DASHBOARD = "dashboard"  # Analytics and data dashboards
    MARKETING = "marketing"  # Marketing websites and landing pages
```

## Agent Interfaces

### DesignStrategistAgent

Agent responsible for defining design principles and philosophy.

#### Methods

##### `analyze_product_requirements(input_data: DesignSystemInput) -> DesignPrinciples`

Analyzes product requirements and generates design principles.

**Parameters:**
- `input_data` (DesignSystemInput): Product specification

**Returns:**
- `DesignPrinciples`: Design philosophy and rules

### VisualIdentityAgent

Agent responsible for generating visual design tokens.

#### Methods

##### `generate_design_tokens(principles: DesignPrinciples) -> DesignTokens`

Creates comprehensive visual design tokens.

**Parameters:**
- `principles` (DesignPrinciples): Design principles

**Returns:**
- `DesignTokens`: Complete token system

### ComponentArchitectAgent

Agent responsible for defining component inventories.

#### Methods

##### `generate_component_inventory(principles: DesignPrinciples, product_context: str) -> ComponentInventory`

Creates component specifications based on requirements.

**Parameters:**
- `principles` (DesignPrinciples): Design principles
- `product_context` (str): Product description

**Returns:**
- `ComponentInventory`: Component specifications

## Component Generators

### ComponentGenerator

Generates React components and supporting files.

#### Methods

##### `generate_button_component(spec: ComponentSpec) -> str`

Generates Button component code.

##### `generate_input_component(spec: ComponentSpec) -> str`

Generates Input component code.

##### `generate_modal_component(spec: ComponentSpec) -> str`

Generates Modal component code.

##### `generate_css_variables() -> str`

Generates CSS custom properties from design tokens.

##### `generate_tailwind_config() -> str`

Generates Tailwind CSS configuration.

##### `generate_package_json() -> str`

Generates package.json for the component library.

##### `generate_storybook_main_config() -> str`

Generates Storybook main configuration.

##### `generate_storybook_preview_config() -> str`

Generates Storybook preview configuration.

## Utility Functions

### Color Utilities

#### `hsl_to_hex(h: float, s: float, l: float) -> str`

Converts HSL color values to hex format.

**Parameters:**
- `h` (float): Hue (0-1)
- `s` (float): Saturation (0-1)
- `l` (float): Lightness (0-1)

**Returns:**
- `str`: Hex color code

### File Operations

#### Generated File Structure

```
component-library/
├── src/
│   ├── components/          # React components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── ...
│   ├── styles/
│   │   └── variables.css    # Design tokens
│   └── index.ts             # Component exports
├── .storybook/
│   ├── main.ts             # Storybook config
│   └── preview.ts          # Preview settings
├── jest.config.js          # Test configuration
├── src/setupTests.ts       # Test setup
├── tailwind.config.js      # Tailwind config
├── package.json            # Package config
└── README.md               # Documentation
```

## Error Handling

### Exception Types

#### `ValidationError`
Raised when input data fails validation.

#### `GenerationError`
Raised when component generation fails.

#### `FileSystemError`
Raised when file operations fail.

## Examples

### Complete Design System Generation

```python
from main import DesignSystemGenerator
from models import DesignSystemInput, TargetUser, BrandTrait, Platform

# Create generator
generator = DesignSystemGenerator()

# Define product
input_data = DesignSystemInput(
    product_idea="A comprehensive project management tool for remote teams",
    target_users=[TargetUser.B2B, TargetUser.CONSUMER],
    brand_traits=[BrandTrait.MODERN, BrandTrait.PROFESSIONAL, BrandTrait.WARM],
    platforms=[Platform.WEB, Platform.MOBILE]
)

# Generate design system
result = generator.generate_design_system(input_data)

# Access generated components
for component in result.component_library.components:
    print(f"Generated: {component.name}")
    print(f"Code length: {len(component.code)} characters")

# Access design tokens
print(f"Colors: {len(result.tokens.colors)}")
print(f"Typography: {len(result.tokens.typography)}")
```

### Custom Component Generation

```python
from templates.components.generator import ComponentGenerator
from models import DesignTokens, ComponentSpec

# Create generator with tokens
tokens = DesignTokens(...)  # Your design tokens
generator = ComponentGenerator(tokens)

# Generate specific component
spec = ComponentSpec(
    name="CustomButton",
    category="button",
    variants=["primary", "secondary"],
    states=["default", "hover", "disabled"],
    description="Custom button component"
)

button_code = generator.generate_button_component(spec)
print(button_code)
```

