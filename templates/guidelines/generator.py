"""Component usage guidelines generator."""

from typing import List
from models import ComponentSpec


class GuidelinesGenerator:
    """Generates component usage guidelines from component specifications."""
    
    def generate_all_guidelines(self, components: List[ComponentSpec]) -> dict:
        """Generate guidelines for all components."""
        return {
            comp.name: self.generate_markdown(comp)
            for comp in components
        }
    
    def generate_markdown(self, component: ComponentSpec) -> str:
        """Generate markdown guidelines for a component."""
        return f'''# {component.name} Component Guidelines

## Overview

{component.description or f"The {component.name} component is a versatile element for your design system."}

## When to Use

{self._generate_when_to_use(component)}

## Variants

{self._generate_variants_guide(component)}

## States

{self._generate_states_guide(component)}

## Accessibility

{component.accessibility_notes or self._generate_default_accessibility(component)}

## Do's and Don'ts

{self._generate_dos_donts(component)}

## Code Examples

{self._generate_code_examples(component)}

## Responsive Behavior

{self._generate_responsive_guide(component)}

## Best Practices

{self._generate_best_practices(component)}
'''
    
    def _generate_when_to_use(self, component: ComponentSpec) -> str:
        """Generate when to use section."""
        category_hints = {
            'button': f"Use {component.name} for primary actions, form submissions, and user interactions that trigger important operations.",
            'input': f"Use {component.name} for collecting user input, form data entry, and text-based information gathering.",
            'navigation': f"Use {component.name} for helping users navigate through your application, access different sections, and understand their current location.",
            'feedback': f"Use {component.name} for providing feedback, status updates, notifications, and important information to users.",
            'layout': f"Use {component.name} for organizing content, creating visual structure, and grouping related information.",
            'data': f"Use {component.name} for displaying data, information tables, lists, and structured content.",
            'contextual': f"Use {component.name} for contextual actions, menus, and situation-specific interactions."
        }
        
        hint = category_hints.get(component.category, f"Use {component.name} when you need to {component.description or 'display this component'}.")
        
        return f'''### Primary Use Cases

- {hint}
- When you need consistent styling across your application
- When accessibility and keyboard navigation are important

### When NOT to Use

- Don't use {component.name} for decorative purposes only
- Avoid using multiple variants of {component.name} in the same context without clear hierarchy
- Don't override the component's core functionality with custom implementations
'''
    
    def _generate_variants_guide(self, component: ComponentSpec) -> str:
        """Generate variants guide."""
        if not component.variants:
            return "This component has a single default variant."
        
        variants_list = '\n'.join([
            f"- **{variant}**: {self._get_variant_description(component.name, variant)}"
            for variant in component.variants
        ])
        
        return f'''The {component.name} component supports the following variants:

{variants_list}

### Choosing the Right Variant

{self._generate_variant_choosing_guide(component)}
'''
    
    def _generate_states_guide(self, component: ComponentSpec) -> str:
        """Generate states guide."""
        if not component.states:
            return "This component supports standard interactive states (default, hover, focus)."
        
        states_list = '\n'.join([
            f"- **{state}**: {self._get_state_description(state)}"
            for state in component.states
        ])
        
        return f'''The {component.name} component supports the following states:

{states_list}

### State Transitions

{self._generate_state_transitions(component)}
'''
    
    def _generate_default_accessibility(self, component: ComponentSpec) -> str:
        """Generate default accessibility guidelines."""
        return f'''### WCAG 2.1 AA Compliance

- Ensure proper ARIA labels and roles
- Support keyboard navigation
- Maintain sufficient color contrast (4.5:1 for normal text, 3:1 for large text)
- Provide focus indicators
- Support screen readers

### Keyboard Navigation

- **Tab**: Navigate to the component
- **Enter/Space**: Activate the component (if interactive)
- **Arrow keys**: Navigate within component groups (if applicable)
- **Escape**: Close or cancel (if applicable)

### Screen Reader Support

Always provide:
- Descriptive labels via `aria-label` or `aria-labelledby`
- Current state information via `aria-disabled`, `aria-checked`, etc.
- Role attributes when default HTML semantics are insufficient
'''
    
    def _generate_dos_donts(self, component: ComponentSpec) -> str:
        """Generate do's and don'ts."""
        return f'''### ✅ Do's

- Use {component.name} consistently across your application
- Choose the appropriate variant based on importance and context
- Provide clear labels and descriptions
- Test with keyboard navigation
- Ensure sufficient color contrast
- Use semantic HTML when possible
- Provide loading states for async operations
- Handle error states gracefully

### ❌ Don'ts

- Don't use {component.name} for decorative purposes only
- Avoid mixing too many variants in the same view
- Don't skip accessibility attributes
- Avoid custom styling that breaks the design system
- Don't use {component.name} for critical actions without confirmation
- Avoid nesting {component.name} components unnecessarily
- Don't override core functionality without careful consideration
'''
    
    def _generate_code_examples(self, component: ComponentSpec) -> str:
        """Generate code examples."""
        examples = []
        
        # Basic example
        if component.variants:
            basic_variant = component.variants[0]
            examples.append(f'''### Basic Usage

\`\`\`tsx
<{component.name} variant="{basic_variant}">
  {self._get_example_content(component.name)}
</{component.name}>
\`\`\`
''')
        
        # With props example
        props_example = f'''### With Props

\`\`\`tsx
<{component.name}
  variant="{component.variants[0] if component.variants else 'default'}"
  {self._get_props_example(component)}
  onClick={{() => handleAction()}}
>
  {self._get_example_content(component.name)}
</{component.name}>
\`\`\`
'''
        examples.append(props_example)
        
        # Multiple variants example
        if len(component.variants) > 1:
            variants_example = f'''### Variant Examples

\`\`\`tsx
<div className="space-x-4">
{chr(10).join([f'  <{component.name} variant="{v}">{self._get_example_content(component.name, v)}</{component.name}>' for v in component.variants[:3]])}
</div>
\`\`\`
'''
            examples.append(variants_example)
        
        return '\n'.join(examples)
    
    def _generate_responsive_guide(self, component: ComponentSpec) -> str:
        """Generate responsive behavior guide."""
        return f'''### Mobile (< 640px)

- {component.name} should be full-width or appropriately sized for touch targets (minimum 44x44px)
- Text should remain readable without zooming
- Spacing should be optimized for smaller screens

### Tablet (640px - 1024px)

- {component.name} can use medium spacing and sizing
- Layout can adapt to available space

### Desktop (> 1024px)

- {component.name} can use larger spacing and sizing
- Consider hover states and interactions
- Optimize for mouse and keyboard input
'''
    
    def _generate_best_practices(self, component: ComponentSpec) -> str:
        """Generate best practices."""
        return f'''### Performance

- Use {component.name} efficiently - avoid creating unnecessary instances
- Consider lazy loading for components below the fold
- Optimize re-renders with React.memo when appropriate

### Testing

- Test {component.name} with different screen sizes
- Verify keyboard navigation works correctly
- Test with screen readers
- Validate color contrast ratios
- Test all variants and states

### Maintenance

- Keep {component.name} updated with design system changes
- Document any customizations or overrides
- Follow semantic versioning for breaking changes
- Provide migration guides when updating
'''
    
    def _get_variant_description(self, component_name: str, variant: str) -> str:
        """Get description for a variant."""
        descriptions = {
            'primary': 'Use for the most important actions',
            'secondary': 'Use for secondary actions',
            'tertiary': 'Use for less prominent actions',
            'danger': 'Use for destructive or dangerous actions',
            'success': 'Use for successful operations',
            'warning': 'Use for warnings or cautions',
            'info': 'Use for informational messages',
            'default': 'Default variant for general use',
        }
        return descriptions.get(variant.lower(), f'Use for {variant} scenarios')
    
    def _get_state_description(self, state: str) -> str:
        """Get description for a state."""
        descriptions = {
            'default': 'The normal, unmodified state of the component',
            'hover': 'When the user hovers over the component',
            'focus': 'When the component receives keyboard focus',
            'active': 'When the component is being activated',
            'disabled': 'When the component is disabled and cannot be interacted with',
            'loading': 'When the component is in a loading state',
            'error': 'When the component has an error state',
            'checked': 'When the component is checked or selected',
        }
        return descriptions.get(state.lower(), f'The {state} state of the component')
    
    def _generate_variant_choosing_guide(self, component: ComponentSpec) -> str:
        """Generate guide for choosing variants."""
        if 'primary' in component.variants and 'secondary' in component.variants:
            return '''- **Primary**: Use for the main action on a page or in a section
- **Secondary**: Use for supporting actions or less important operations
- Choose based on visual hierarchy and user flow'''
        return "Choose variants based on the importance and context of the action."
    
    def _generate_state_transitions(self, component: ComponentSpec) -> str:
        """Generate state transition guide."""
        return f'''State transitions should be smooth and provide visual feedback:

- **Default → Hover**: Subtle visual change (e.g., color darkening, shadow increase)
- **Hover → Active**: More pronounced change to indicate activation
- **Active → Default**: Return to default state with appropriate timing
- **Default → Disabled**: Visual indication that interaction is not possible
- **Default → Loading**: Show loading indicator while maintaining component structure
- **Default → Error**: Clear visual indication of error state

All transitions should respect user preferences for reduced motion.'''
    
    def _get_example_content(self, component_name: str, variant: str = None) -> str:
        """Get example content for component."""
        content_map = {
            'Button': 'Click me',
            'Input': 'Enter text...',
            'Card': 'Card content',
            'Badge': 'New',
            'Alert': 'This is an alert',
            'Modal': 'Modal content',
        }
        return content_map.get(component_name, 'Content')
    
    def _get_props_example(self, component: ComponentSpec) -> str:
        """Get props example string."""
        props = []
        if component.variants:
            props.append(f'variant="{component.variants[0]}"')
        if 'disabled' in (component.states or []):
            props.append('disabled={false}')
        if 'loading' in (component.states or []):
            props.append('loading={false}')
        return '\n  '.join(props) if props else ''
