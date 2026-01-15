"""Next.js component generator with App Router and Pages Router support."""

from typing import List
from models import DesignTokens, ComponentSpec


class NextJSGenerator:
    """Generates Next.js components with App Router support."""
    
    def __init__(self, tokens: DesignTokens):
        self.tokens = tokens
    
    def generate_button_component(self, spec: ComponentSpec) -> str:
        """Generate Next.js Button component with 'use client' directive."""
        variants_union = ' | '.join(f'"{v}"' for v in spec.variants)
        default_variant = spec.variants[0]
        
        return f'''"use client";

import React from 'react';
import {{ motion }} from 'framer-motion';

/**
 * Button component for Next.js applications.
 * 
 * @example
 * ```tsx
 * <Button variant="primary" onClick={{() => console.log('clicked')}}>
 *   Click me
 * </Button>
 * ```
 */
export interface ButtonProps {{
  /** Button variant style */
  variant?: {variants_union};
  /** Button size */
  size?: 'sm' | 'md' | 'lg';
  /** Whether button is disabled */
  disabled?: boolean;
  /** Whether button is in loading state */
  loading?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Button content */
  children: React.ReactNode;
  /** Additional CSS classes */
  className?: string;
  /** HTML button type */
  type?: 'button' | 'submit' | 'reset';
  /** ARIA label for accessibility */
  'aria-label'?: string;
}}

/**
 * Button component with multiple variants and states.
 * 
 * Features:
 * - Multiple variants: primary, secondary, tertiary, danger
 * - Three sizes: sm, md, lg
 * - Loading and disabled states
 * - Full keyboard navigation support
 * - WCAG 2.1 AA compliant
 */
export const Button: React.FC<ButtonProps> = ({{
  variant = '{default_variant}',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  children,
  className = '',
  type = 'button',
  'aria-label': ariaLabel,
}}) => {{
  const baseClasses = 'inline-flex items-center justify-center font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';
  
  const variantClasses = {{
    primary: 'bg-primary-500 hover:bg-primary-600 text-white focus:ring-primary-500',
    secondary: 'bg-neutral-100 hover:bg-neutral-200 text-neutral-900 focus:ring-neutral-500',
    tertiary: 'border border-neutral-300 hover:bg-neutral-50 text-neutral-900 focus:ring-neutral-500',
    danger: 'bg-error-500 hover:bg-error-600 text-white focus:ring-error-500'
  }};
  
  const sizeClasses = {{
    sm: 'px-3 py-1.5 text-sm rounded-md',
    md: 'px-4 py-2 text-base rounded-md',
    lg: 'px-6 py-3 text-lg rounded-lg'
  }};
  
  const classes = `${{baseClasses}} ${{variantClasses[variant]}} ${{sizeClasses[size]}} ${{className}}`;
  
  return (
    <motion.button
      type={{type}}
      className={{classes}}
      onClick={{onClick}}
      disabled={{disabled || loading}}
      aria-label={{ariaLabel}}
      aria-busy={{loading}}
      whileHover={{disabled || loading ? {{}} : {{ scale: 1.02 }}}}
      whileTap={{disabled || loading ? {{}} : {{ scale: 0.98 }}}}
    >
      {{loading ? (
        <span className="mr-2">
          <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </span>
      ) : null}}
      {{children}}
    </motion.button>
  );
}};
'''
    
    def generate_input_component(self, spec: ComponentSpec) -> str:
        """Generate Next.js Input component."""
        return '''"use client";

import React from 'react';

/**
 * Input component for Next.js applications.
 * 
 * @example
 * ```tsx
 * <Input 
 *   type="email" 
 *   placeholder="Enter email"
 *   onChange={(value) => console.log(value)}
 * />
 * ```
 */
export interface InputProps {
  /** Input type */
  type?: 'text' | 'email' | 'password' | 'search' | 'number';
  /** Placeholder text */
  placeholder?: string;
  /** Input value */
  value?: string;
  /** Change handler */
  onChange?: (value: string) => void;
  /** Whether input has error */
  error?: boolean;
  /** Whether input is disabled */
  disabled?: boolean;
  /** Whether input is required */
  required?: boolean;
  /** Additional CSS classes */
  className?: string;
  /** Input name attribute */
  name?: string;
  /** Input id attribute */
  id?: string;
  /** ARIA label for accessibility */
  'aria-label'?: string;
  /** ARIA described by */
  'aria-describedby'?: string;
}

/**
 * Input component with validation states and accessibility.
 */
export const Input: React.FC<InputProps> = ({
  type = 'text',
  placeholder,
  value,
  onChange,
  error = false,
  disabled = false,
  required = false,
  className = '',
  name,
  id,
  'aria-label': ariaLabel,
  'aria-describedby': ariaDescribedBy,
}) => {
  const baseClasses = 'w-full px-4 py-2 border rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1';
  const stateClasses = error 
    ? 'border-error-300 focus:ring-error-500 focus:border-error-500' 
    : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500';
  const disabledClasses = disabled ? 'bg-neutral-100 cursor-not-allowed opacity-60' : 'bg-white';
  
  const classes = `${baseClasses} ${stateClasses} ${disabledClasses} ${className}`;
  
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
      disabled={disabled}
      required={required}
      className={classes}
      name={name}
      id={id}
      aria-label={ariaLabel}
      aria-describedby={ariaDescribedBy}
      aria-invalid={error}
      aria-required={required}
    />
  );
};
'''
    
    def generate_app_router_layout(self) -> str:
        """Generate Next.js App Router layout with design tokens."""
        return '''import type { Metadata } from 'next';
import '../styles/tokens.css';

export const metadata: Metadata = {
  title: 'Design System App',
  description: 'Application built with generated design system',
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
    
    def generate_pages_router_document(self) -> str:
        """Generate Next.js Pages Router _document.tsx."""
        return '''import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <link rel="stylesheet" href="/styles/tokens.css" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
'''
