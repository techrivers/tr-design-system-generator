"""TypeScript type definitions generator for design systems."""

from typing import Dict, Any, List
from models import DesignSystemOutput, DesignTokens


class TypeScriptGenerator:
    """Generates TypeScript type definitions for design systems."""
    
    def generate_token_types(self, tokens: DesignTokens) -> str:
        """Generate TypeScript types for design tokens."""
        return f'''/**
 * Design Token Types
 * Auto-generated from design system
 */

export type ColorToken = {{
  name: string;
  value: string;
  role: 'primary' | 'secondary' | 'neutral' | 'semantic' | 'accent';
}};

export type TypographyToken = {{
  name: string;
  family: string;
  size: string;
  weight: number;
  line_height: number | string;
  role: 'heading' | 'body' | 'ui';
}};

export type SpacingToken = {{
  name: string;
  value: string;
  scale: number;
}};

export type DesignTokens = {{
  colors: ColorToken[];
  typography: TypographyToken[];
  spacing: SpacingToken[];
  border_radius: {{
    small: string;
    medium: string;
    large: string;
    round: string;
  }};
  shadows: {{
    sm: string;
    md: string;
    lg: string;
  }};
}};

// Color token names
export type ColorName = {self._generate_color_names(tokens)};

// Typography token names
export type TypographyName = {self._generate_typography_names(tokens)};

// Spacing token names
export type SpacingName = {self._generate_spacing_names(tokens)};

// Theme type
export interface Theme {{
  colors: Record<ColorName, string>;
  typography: Record<TypographyName, TypographyToken>;
  spacing: Record<SpacingName, string>;
  borderRadius: DesignTokens['border_radius'];
  shadows: DesignTokens['shadows'];
}}

/**
 * Theme provider props
 */
export interface ThemeProviderProps {{
  theme?: Theme;
  mode?: 'light' | 'dark' | 'auto';
  children: React.ReactNode;
}}

/**
 * Token value getter function type
 */
export type TokenGetter<T> = (token: T) => string;

/**
 * Color token getter
 */
export const getColorToken: TokenGetter<ColorToken> = (token) => token.value;

/**
 * Typography token getter
 */
export const getTypographyToken: TokenGetter<TypographyToken> = (token) => token.family;
'''
    
    def generate_component_types(self, components: list) -> str:
        """Generate TypeScript types for components."""
        component_props = []
        
        for comp in components:
            props = self._generate_component_props(comp)
            variant_type = f'{comp.name}Variant' if comp.variants else 'never'
            component_props.append(f'''
/**
 * {comp.name} Component Props
 * {comp.description or "Component props interface"}
 */
export interface {comp.name}Props {{
{props}
}}

/**
 * {comp.name} Variant Type
 */
export type {comp.name}Variant = {self._generate_variant_union(comp.variants)};

/**
 * {comp.name} Component with Generic Support
 */
export interface {comp.name}Component<T extends {variant_type} = {variant_type}> extends React.FC<{comp.name}Props & {{ variant?: T }}> {{}}
''')
        
        return f'''/**
 * Component Props Types
 * Auto-generated from design system
 */

import React from 'react';

{''.join(component_props)}

/**
 * Generic Component Props Base
 */
export interface BaseComponentProps {{
  className?: string;
  'data-testid'?: string;
  'aria-label'?: string;
  'aria-labelledby'?: string;
}}

/**
 * Interactive Component Props
 */
export interface InteractiveComponentProps extends BaseComponentProps {{
  onClick?: (event: React.MouseEvent<HTMLElement>) => void;
  onFocus?: (event: React.FocusEvent<HTMLElement>) => void;
  onBlur?: (event: React.FocusEvent<HTMLElement>) => void;
  disabled?: boolean;
  'aria-disabled'?: boolean;
}}

/**
 * Form Component Props
 */
export interface FormComponentProps extends InteractiveComponentProps {{
  name?: string;
  value?: string | number | boolean;
  defaultValue?: string | number | boolean;
  required?: boolean;
  'aria-required'?: boolean;
  'aria-invalid'?: boolean;
}}
'''
    
    def generate_theme_types(self, design_system: DesignSystemOutput) -> str:
        """Generate complete theme type definitions."""
        tokens = design_system.tokens
        
        return f'''/**
 * Complete Theme Type Definitions
 * Auto-generated from design system
 */

import {{ ColorToken, TypographyToken, SpacingToken, DesignTokens }} from './tokens';

export interface DesignSystemTheme {{
  tokens: DesignTokens;
  principles: {{
    philosophy: '{design_system.principles.philosophy}';
    density: '{design_system.principles.density}';
    clarity: {design_system.principles.clarity};
    warmth: {design_system.principles.warmth};
    speed: {design_system.principles.speed};
  }};
  components: Array<{{
    name: string;
    role: string;
    variants: string[];
    states: string[];
  }}>;
}}

// Utility types
export type ThemeColor = DesignTokens['colors'][number]['name'];
export type ThemeTypography = DesignTokens['typography'][number]['name'];
export type ThemeSpacing = DesignTokens['spacing'][number]['name'];

// Component variant types
{self._generate_variant_types(design_system)}
'''
    
    def _generate_color_names(self, tokens: DesignTokens) -> str:
        names = [f'"{c.name}"' for c in tokens.colors]
        return ' | '.join(names) if names else 'never'
    
    def _generate_typography_names(self, tokens: DesignTokens) -> str:
        names = [f'"{t.name}"' for t in tokens.typography]
        return ' | '.join(names) if names else 'never'
    
    def _generate_spacing_names(self, tokens: DesignTokens) -> str:
        names = [f'"{s.name}"' for s in tokens.spacing]
        return ' | '.join(names) if names else 'never'
    
    def _generate_component_props(self, component: Any) -> str:
        """Generate props interface for a component."""
        props = []
        
        # Base props
        props.append('  children?: React.ReactNode;')
        
        # Variant prop with JSDoc
        if component.variants:
            variant_doc = f'  /** Variant of the {component.name} component */'
            props.append(variant_doc)
            variant_type = ' | '.join([f'"{v}"' for v in component.variants])
            props.append(f'  variant?: {variant_type};')
        
        # Size prop if applicable
        if any('size' in str(s).lower() or 'small' in str(s).lower() or 'large' in str(s).lower() 
               for s in (component.states or [])):
            props.append('  /** Size of the component */')
            props.append('  size?: "sm" | "md" | "lg";')
        
        # State-based props
        if component.states:
            if 'disabled' in component.states:
                props.append('  /** Whether the component is disabled */')
                props.append('  disabled?: boolean;')
            if 'loading' in component.states:
                props.append('  /** Whether the component is in loading state */')
                props.append('  loading?: boolean;')
            if 'error' in component.states:
                props.append('  /** Whether the component has an error state */')
                props.append('  error?: boolean;')
            if 'checked' in component.states:
                props.append('  /** Whether the component is checked */')
                props.append('  checked?: boolean;')
        
        # Common interactive props
        props.extend([
            '  /** Additional CSS class names */',
            '  className?: string;',
            '  /** Click event handler */',
            '  onClick?: (event: React.MouseEvent<HTMLElement>) => void;',
            '  /** Focus event handler */',
            '  onFocus?: (event: React.FocusEvent<HTMLElement>) => void;',
            '  /** Blur event handler */',
            '  onBlur?: (event: React.FocusEvent<HTMLElement>) => void;',
        ])
        
        # Accessibility props
        props.extend([
            '  /** ARIA label for accessibility */',
            '  "aria-label"?: string;',
            '  /** ARIA labelled by element ID */',
            '  "aria-labelledby"?: string;',
        ])
        
        return '\n'.join(props)
    
    def _generate_variant_union(self, variants: list) -> str:
        """Generate variant union type."""
        if not variants:
            return 'never'
        return ' | '.join([f'"{v}"' for v in variants])
    
    def _generate_variant_types(self, design_system: DesignSystemOutput) -> str:
        """Generate variant type definitions for components."""
        variant_types = []
        
        for comp in design_system.components.components:
            if comp.variants:
                variant_type = f'''export type {comp.name}Variant = {' | '.join([f'"{v}"' for v in comp.variants])};'''
                variant_types.append(variant_type)
        
        return '\n'.join(variant_types) if variant_types else '// No variant types'
    
    def generate_all(self, design_system: DesignSystemOutput) -> Dict[str, str]:
        """Generate all TypeScript type files."""
        return {
            'tokens.d.ts': self.generate_token_types(design_system.tokens),
            'components.d.ts': self.generate_component_types(design_system.components.components),
            'theme.d.ts': self.generate_theme_types(design_system),
            'utils.d.ts': self.generate_utility_types(design_system),
        }
    
    def generate_utility_types(self, design_system: DesignSystemOutput) -> str:
        """Generate utility types for common patterns."""
        return f'''/**
 * Utility Types
 * Auto-generated from design system
 */

/**
 * Extract component props type
 */
export type ComponentProps<T> = T extends React.ComponentType<infer P> ? P : never;

/**
 * Extract variant type from component
 */
export type ExtractVariant<T> = T extends {{ variant?: infer V }} ? V : never;

/**
 * Make all properties optional recursively
 */
export type DeepPartial<T> = {{
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
}};

/**
 * Make all properties required recursively
 */
export type DeepRequired<T> = {{
  [P in keyof T]-?: T[P] extends object ? DeepRequired<T[P]> : T[P];
}};

/**
 * Omit properties from type
 */
export type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;

/**
 * Pick properties from type
 */
export type Pick<T, K extends keyof T> = {{
  [P in K]: T[P];
}};

/**
 * Component size type
 */
export type ComponentSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

/**
 * Component state type
 */
export type ComponentState = 'default' | 'hover' | 'focus' | 'active' | 'disabled' | 'loading' | 'error';

/**
 * Color role type
 */
export type ColorRole = 'primary' | 'secondary' | 'neutral' | 'semantic' | 'accent';

/**
 * Typography role type
 */
export type TypographyRole = 'heading' | 'body' | 'ui' | 'display';

/**
 * Responsive value type
 */
export type ResponsiveValue<T> = T | {{
  sm?: T;
  md?: T;
  lg?: T;
  xl?: T;
}};

/**
 * Theme mode type
 */
export type ThemeMode = 'light' | 'dark' | 'auto';

/**
 * Design system configuration
 */
export interface DesignSystemConfig {{
  theme: ThemeMode;
  density: 'dense' | 'spacious' | 'balanced';
  philosophy: 'utility-first' | 'component-first' | 'brand-led';
}}
'''
