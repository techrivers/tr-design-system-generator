"""Component Generator - Generates React components from design system specifications."""

import sys
import os
from typing import Dict, List
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from models import DesignTokens, ComponentSpec, ComponentCode


class ComponentGenerator:
    """Generates React components with Tailwind CSS based on design tokens and specs."""

    def __init__(self, tokens: DesignTokens):
        self.tokens = tokens
        self.templates_dir = os.path.dirname(os.path.abspath(__file__))

    def generate_css_variables(self) -> str:
        """Generate CSS custom properties from design tokens with light and dark mode support."""
        css_vars = [":root {"]

        # Light Mode Palette
        for color in self.tokens.colors:
            css_vars.append(f"  --color-{color.name}: {color.value};")

        # Typography variables
        for typo in self.tokens.typography:
            css_vars.append(f"  --font-{typo.name}: {typo.family};")
            css_vars.append(f"  --text-{typo.name}: {typo.size} {typo.weight} {typo.line_height};")

        # Spacing variables
        for space in self.tokens.spacing:
            css_vars.append(f"  --space-{space.name}: {space.value};")

        # Border radius
        for key, value in self.tokens.border_radius.items():
            css_vars.append(f"  --radius-{key}: {value};")

        # Shadows
        for key, value in self.tokens.shadows.items():
            css_vars.append(f"  --shadow-{key}: {value};")

        # Semantic tokens (Light Mode)
        css_vars.append("\n  /* Semantic tokens */")
        css_vars.append("  --bg-base: var(--color-neutral-50);")
        css_vars.append("  --bg-surface: var(--color-neutral-100);")
        css_vars.append("  --text-base: var(--color-neutral-900);")
        css_vars.append("  --text-muted: var(--color-neutral-600);")
        css_vars.append("  --border-base: var(--color-neutral-300);")
        
        css_vars.append("}")

        # Dark Mode Palette & Semantic overrides
        if self.tokens.dark_colors:
            css_vars.append("\n[data-theme='dark'] {")
            for color in self.tokens.dark_colors:
                css_vars.append(f"  --color-{color.name}: {color.value};")
            
            css_vars.append("\n  /* Semantic overrides */")
            css_vars.append("  --bg-base: var(--color-neutral-900);")
            css_vars.append("  --bg-surface: var(--color-neutral-800);")
            css_vars.append("  --text-base: var(--color-neutral-50);")
            css_vars.append("  --text-muted: var(--color-neutral-400);")
            css_vars.append("  --border-base: var(--color-neutral-700);")
            css_vars.append("}")

        return "\n".join(css_vars)

    def generate_button_component(self, spec: ComponentSpec) -> str:
        """Generate a Button component with enhanced TypeScript, JSDoc, and accessibility."""
        variants_union = ' | '.join(f'"{v}"' for v in spec.variants)
        default_variant = spec.variants[0]

        button_code = '''import React from 'react';
import { motion } from 'framer-motion';

/**
 * Button component variants.
 * 
 * @public
 */
export type ButtonVariant = ''' + variants_union + ''';

/**
 * Button size options.
 * 
 * @public
 */
export type ButtonSize = 'sm' | 'md' | 'lg';

/**
 * Props for the Button component.
 * 
 * @public
 * 
 * @example
 * ```tsx
 * <Button variant="primary" size="md" onClick={() => console.log('clicked')}>
 *   Click me
 * </Button>
 * ```
 */
export interface ButtonProps {
  /**
   * Visual style variant of the button.
   * 
   * @defaultValue "primary"
   */
  variant?: ButtonVariant;
  
  /**
   * Size of the button.
   * 
   * @defaultValue "md"
   */
  size?: ButtonSize;
  
  /**
   * Whether the button is disabled.
   * 
   * @defaultValue false
   */
  disabled?: boolean;
  
  /**
   * Whether the button is in a loading state.
   * When true, shows a loading spinner and disables the button.
   * 
   * @defaultValue false
   */
  loading?: boolean;
  
  /**
   * Click event handler.
   * 
   * @param event - The click event
   */
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  
  /**
   * Button content (text, icons, etc.).
   */
  children: React.ReactNode;
  
  /**
   * Additional CSS classes to apply.
   */
  className?: string;
  
  /**
   * HTML button type attribute.
   * 
   * @defaultValue "button"
   */
  type?: 'button' | 'submit' | 'reset';
  
  /**
   * ARIA label for accessibility.
   * Use when the button text doesn't fully describe its purpose.
   */
  'aria-label'?: string;
  
  /**
   * ARIA described by element ID.
   * References an element that provides additional description.
   */
  'aria-describedby'?: string;
}

/**
 * Button component with multiple variants, sizes, and states.
 * 
 * Features:
 * - Multiple visual variants (primary, secondary, tertiary, danger)
 * - Three size options (sm, md, lg)
 * - Loading and disabled states
 * - Full keyboard navigation support
 * - WCAG 2.1 AA compliant contrast ratios
 * - Smooth animations with Framer Motion
 * 
 * @public
 * 
 * @example
 * ```tsx
 * // Primary button
 * <Button variant="primary" onClick={handleClick}>
 *   Save Changes
 * </Button>
 * 
 * // Loading state
 * <Button loading>Processing...</Button>
 * 
 * // With icon
 * <Button variant="secondary">
 *   <Icon name="download" />
 *   Download
 * </Button>
 * ```
 */
export const Button: React.FC<ButtonProps> = ({
  variant = \'''' + default_variant + '''',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  children,
  className = '',
  type = 'button',
  'aria-label': ariaLabel,
  'aria-describedby': ariaDescribedBy,
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';

  const variantClasses = {
    primary: 'bg-primary-500 hover:bg-primary-600 text-white focus:ring-primary-500',
    secondary: 'bg-background-surface hover:bg-neutral-200 text-text-base focus:ring-neutral-500',
    tertiary: 'border border-border-base hover:bg-background-surface text-text-base focus:ring-neutral-500',
    danger: 'bg-error-500 hover:bg-error-600 text-white focus:ring-error-500'
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm rounded-md',
    md: 'px-4 py-2 text-base rounded-md',
    lg: 'px-6 py-3 text-lg rounded-lg'
  };

  const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`.trim();

  const handleKeyDown = (event: React.KeyboardEvent<HTMLButtonElement>) => {
    // Support keyboard activation (Enter and Space)
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (!disabled && !loading && onClick) {
        onClick(event as any);
      }
    }
  };

  return (
    <motion.button
      type={type}
      className={classes}
      disabled={disabled || loading}
      onClick={onClick}
      onKeyDown={handleKeyDown}
      aria-label={ariaLabel}
      aria-busy={loading}
      aria-disabled={disabled || loading}
      aria-describedby={ariaDescribedBy}
      whileHover={disabled || loading ? {} : { scale: 1.02 }}
      whileTap={disabled || loading ? {} : { scale: 0.98 }}
      tabIndex={disabled || loading ? -1 : 0}
    >
      {loading && (
        <span className="mr-2" aria-hidden="true">
          <svg 
            className="animate-spin h-4 w-4" 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24"
            role="img"
            aria-label="Loading"
          >
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </span>
      )}
      {children}
    </motion.button>
  );
};

export default Button;
'''
        return button_code

    def generate_input_component(self, spec: ComponentSpec) -> str:
        """Generate an Input component."""
        variants_union = ' | '.join(f'"{v}"' for v in spec.variants)
        default_variant = spec.variants[0]

        input_code = '''import React, { useState } from 'react';

interface InputProps {
  type?: ''' + variants_union + ''';
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  error?: boolean;
  disabled?: boolean;
  required?: boolean;
}

export const Input: React.FC<InputProps> = ({
  type = \'''' + default_variant + '''',
  placeholder,
  value,
  onChange,
  error = false,
  disabled = false,
  required = false
}) => {
  const [internalValue, setInternalValue] = useState(value || '');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setInternalValue(newValue);
    onChange?.(newValue);
  };

  const baseClasses = 'w-full px-3 py-2 border rounded-md shadow-sm bg-background-base text-text-base border-border-base placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-background-surface disabled:text-text-muted disabled:cursor-not-allowed transition-colors';

  const stateClasses = error
    ? 'border-error-500 text-error-500 placeholder-error-300 focus:ring-error-500 focus:border-error-500'
    : 'border-border-base text-text-base';

  const classes = baseClasses + ' ' + stateClasses;

  return (
    <input
      type={type}
      className={classes}
      placeholder={placeholder}
      value={internalValue}
      onChange={handleChange}
      disabled={disabled}
      required={required}
      aria-invalid={error}
    />
  );
};

export default Input;
'''
        return input_code

    def generate_select_component(self, spec: ComponentSpec) -> str:
        """Generate a Select component."""
        select_code = '''import React, { useState } from 'react';

interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps {
  options: SelectOption[];
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  error?: boolean;
  disabled?: boolean;
  required?: boolean;
}

export const Select: React.FC<SelectProps> = ({
  options,
  placeholder = 'Select an option',
  value,
  onChange,
  error = false,
  disabled = false,
  required = false
}) => {
  const [internalValue, setInternalValue] = useState(value || '');

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newValue = e.target.value;
    setInternalValue(newValue);
    onChange?.(newValue);
  };

  const baseClasses = 'w-full px-3 py-2 bg-background-base text-text-base border-border-base rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-background-surface disabled:text-text-muted disabled:cursor-not-allowed transition-colors appearance-none';

  const stateClasses = error
    ? 'border-error-500 text-error-500 focus:ring-error-500 focus:border-error-500'
    : 'border-border-base text-text-base';

  const classes = baseClasses + ' ' + stateClasses;

  return (
    <div className="relative">
      <select
        className={classes}
        value={internalValue}
        onChange={handleChange}
        disabled={disabled}
        required={required}
        aria-invalid={error}
      >
        <option value="" disabled>{placeholder}</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      <div className="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
        <svg className="w-5 h-5 text-text-muted" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
    </div>
  );
};

export default Select;
'''
        return select_code

    def generate_alert_component(self, spec: ComponentSpec) -> str:
        """Generate an Alert component."""
        alert_code = '''import React from 'react';

interface AlertProps {{
  variant?: ''' + ' | '.join(f'"{v}"' for v in spec.variants) + ''';
  title?: string;
  children: React.ReactNode;
  onDismiss?: () => void;
}}

export const Alert: React.FC<AlertProps> = ({{
  variant = \'''' + spec.variants[0] + '''',
  title,
  children,
  onDismiss
}}) => {{
  const variantClasses = {{
    success: 'bg-success-50 border-success-200 text-success-800',
    warning: 'bg-warning-50 border-warning-200 text-warning-800',
    error: 'bg-error-50 border-error-200 text-error-800',
    info: 'bg-info-50 border-info-200 text-info-800'
  }};

  const iconClasses = {{
    success: 'text-success-400',
    warning: 'text-warning-400',
    error: 'text-error-400',
    info: 'text-info-400'
  }};

  return (
      <div className={`p-4 rounded-md border ${variantClasses[variant]}`} role="alert">
      <div className="flex">
        <div className="flex-shrink-0">
          <svg className={`h-5 w-5 ${iconClasses[variant]}`} viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="ml-3 flex-1">
          {{title && <h3 className="text-sm font-medium">{title}</h3>}}
          <div className="text-sm">
            {{children}}
          </div>
        </div>
        {{onDismiss && (
          <div className="ml-auto pl-3">
            <button
              type="button"
              className={`inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2 ${variantClasses[variant].replace('bg-', 'focus:ring-').replace(' text-', ' focus:ring-')}`}
              onClick={{onDismiss}}
            >
              <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        )}}
      </div>
    </div>
  );
}};

export default Alert;
'''
        return alert_code

    def generate_modal_component(self, spec: ComponentSpec) -> str:
        """Generate a Modal component."""
        modal_code = '''import React, { useEffect } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  closeOnOverlayClick?: boolean;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  closeOnOverlayClick = true
}) => {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl'
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={closeOnOverlayClick ? onClose : undefined}
      />

      {/* Modal */}
      <div className={`relative bg-background-surface rounded-lg shadow-xl ${sizeClasses[size]} w-full mx-4 max-h-[90vh] overflow-hidden`}>
        {/* Header */}
        {(title || onClose) && (
          <div className="flex items-center justify-between p-6 border-b border-border-base">
            {title && <h3 className="text-lg font-semibold text-text-base">{title}</h3>}
            {onClose && (
              <button
                onClick={onClose}
                className="text-text-muted hover:text-text-base transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        )}

        {/* Content */}
        <div className="p-6 overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal;
'''
        return modal_code

    def generate_table_component(self, spec: ComponentSpec) -> str:
        """Generate a Table component."""
        table_code = '''import React from 'react';

interface TableColumn<T> {
  key: keyof T;
  header: string;
  render?: (value: any, item: T) => React.ReactNode;
  sortable?: boolean;
}

interface TableProps<T> {
  data: T[];
  columns: TableColumn<T>[];
  loading?: boolean;
  emptyMessage?: string;
  selectable?: boolean;
  onRowSelect?: (item: T) => void;
  selectedRows?: T[];
}

export function Table<T extends Record<string, any>>({
  data,
  columns,
  loading = false,
  emptyMessage = 'No data available',
  selectable = false,
  onRowSelect,
  selectedRows = []
}: TableProps<T>) {
  const isSelected = (item: T) => {
    return selectedRows.some(selected => JSON.stringify(selected) === JSON.stringify(item));
  };

  if (loading) {
    return (
      <div className="w-full">
        <div className="animate-pulse">
          <div className="h-4 bg-background-surface rounded w-full mb-2"></div>
          <div className="h-4 bg-background-surface rounded w-5/6 mb-2"></div>
          <div className="h-4 bg-background-surface rounded w-4/6"></div>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-text-muted">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-border-base">
        <thead className="bg-background-surface">
          <tr>
            {selectable && (
              <th className="px-6 py-3 text-left text-xs font-medium text-text-muted uppercase tracking-wider">
                Select
              </th>
            )}
            {columns.map((column) => (
              <th
                key={String(column.key)}
                className="px-6 py-3 text-left text-xs font-medium text-text-muted uppercase tracking-wider"
              >
                {column.header}
                {column.sortable && (
                  <span className="ml-1">↕</span>
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-background-base divide-y divide-border-base">
          {data.map((item, index) => (
            <tr
              key={index}
              className={`hover:bg-background-surface ${isSelected(item) ? 'bg-primary-50' : ''} ${selectable ? 'cursor-pointer' : ''}`}
              onClick={() => selectable && onRowSelect?.(item)}
            >
              {selectable && (
                <td className="px-6 py-4 whitespace-nowrap">
                  <input
                    type="checkbox"
                    checked={isSelected(item)}
                    onChange={() => onRowSelect?.(item)}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-border-base rounded"
                  />
                </td>
              )}
              {columns.map((column) => (
                <td key={String(column.key)} className="px-6 py-4 whitespace-nowrap text-sm text-text-base">
                  {column.render
                    ? column.render(item[column.key], item)
                    : String(item[column.key])
                  }
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Table;
'''
        return table_code

    def generate_navigation_component(self, spec: ComponentSpec) -> str:
        """Generate a Navigation component."""
        nav_code = '''import React, { useState } from 'react';

interface NavItem {
  label: string;
  href?: string;
  onClick?: () => void;
  children?: NavItem[];
  icon?: React.ReactNode;
}

interface NavigationProps {
  items: NavItem[];
  variant?: 'horizontal' | 'vertical';
  collapsible?: boolean;
  activeItem?: string;
  onItemClick?: (item: NavItem) => void;
}

export const Navigation: React.FC<NavigationProps> = ({
  items,
  variant = 'horizontal',
  collapsible = false,
  activeItem,
  onItemClick
}) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  const toggleExpanded = (itemLabel: string) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(itemLabel)) {
      newExpanded.delete(itemLabel);
    } else {
      newExpanded.add(itemLabel);
    }
    setExpandedItems(newExpanded);
  };

  const handleItemClick = (item: NavItem) => {
    if (item.children) {
      toggleExpanded(item.label);
    }
    onItemClick?.(item);
    item.onClick?.();
  };

  const renderNavItem = (item: NavItem, depth = 0) => {
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedItems.has(item.label);
    const isActive = activeItem === item.label;

    return (
      <div key={item.label}>
        <div
          className={`flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
            isActive
              ? 'bg-primary-100 text-primary-700'
              : 'text-text-muted hover:bg-background-surface hover:text-text-base'
          } ${depth > 0 ? 'ml-4' : ''}`}
          onClick={() => handleItemClick(item)}
        >
          {item.icon && <span className="mr-2">{item.icon}</span>}
          <span className="flex-1">{item.label}</span>
          {hasChildren && (
            <svg
              className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          )}
        </div>
        {hasChildren && isExpanded && (
          <div className="mt-1">
            {item.children.map(child => renderNavItem(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  const containerClasses = variant === 'horizontal'
    ? 'flex space-x-1'
    : 'space-y-1';

  return (
    <nav className={containerClasses}>
      {collapsible && variant === 'vertical' && (
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="w-full flex items-center justify-between px-3 py-2 text-sm font-medium text-neutral-600 hover:bg-neutral-100 rounded-md"
        >
          Menu
          <svg
            className={`w-4 h-4 transition-transform ${isCollapsed ? '' : 'rotate-180'}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      )}
      {(!isCollapsed || variant === 'horizontal') && (
        <div className={variant === 'vertical' ? 'space-y-1' : 'flex space-x-1'}>
          {items.map(item => renderNavItem(item))}
        </div>
      )}
    </nav>
  );
};

export default Navigation;
'''
        return nav_code

    def generate_datepicker_component(self, spec: ComponentSpec) -> str:
        """Generate a DatePicker component."""
        return '''import React, { useState, useRef } from 'react';
import { Button } from './Button';
import { Input } from './Input';

interface DatePickerProps {
  value?: Date;
  onChange?: (date: Date | null) => void;
  placeholder?: string;
  disabled?: boolean;
  required?: boolean;
  minDate?: Date;
  maxDate?: Date;
  format?: string;
}

export const DatePicker: React.FC<DatePickerProps> = ({
  value,
  onChange,
  placeholder = 'Select date',
  disabled = false,
  required = false,
  minDate,
  maxDate,
  format = 'MM/dd/yyyy'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState<Date | null>(value || null);
  const inputRef = useRef<HTMLInputElement>(null);

  const formatDate = (date: Date | null): string => {
    if (!date) return '';
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });
  };

  const handleDateSelect = (date: Date) => {
    setSelectedDate(date);
    onChange?.(date);
    setIsOpen(false);
  };

  const generateCalendarDays = () => {
    const today = new Date();
    const currentMonth = selectedDate || today;
    const firstDay = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), 1);
    const lastDay = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay());

    const days = [];
    const current = new Date(startDate);

    for (let i = 0; i < 42; i++) {
      const isCurrentMonth = current.getMonth() === currentMonth.getMonth();
      const isSelected = selectedDate &&
        current.toDateString() === selectedDate.toDateString();
      const isToday = current.toDateString() === today.toDateString();
      const isDisabled = (minDate && current < minDate) || (maxDate && current > maxDate);

      days.push({
        date: new Date(current),
        day: current.getDate(),
        isCurrentMonth,
        isSelected,
        isToday,
        isDisabled
      });

      current.setDate(current.getDate() + 1);
    }

    return days;
  };

  return (
    <div className="relative">
      <div onClick={() => !disabled && setIsOpen(!isOpen)}>
        <Input
          ref={inputRef}
          value={formatDate(selectedDate)}
          placeholder={placeholder}
          disabled={disabled}
          required={required}
          readOnly
          className="cursor-pointer"
        />
      </div>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute z-20 mt-1 bg-background-surface border border-border-base rounded-md shadow-lg p-4 w-72">
            <div className="flex items-center justify-between mb-4">
              <button className="p-1 hover:bg-background-base rounded text-text-base">
                ‹
              </button>
              <h3 className="font-semibold text-text-base">
                {selectedDate?.toLocaleDateString('en-US', { month: 'long', year: 'numeric' }) ||
                 new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
              </h3>
              <button className="p-1 hover:bg-background-base rounded text-text-base">
                ›
              </button>
            </div>

            <div className="grid grid-cols-7 gap-1 mb-2">
              {['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map(day => (
                <div key={day} className="text-center text-sm font-medium text-text-muted py-1">
                  {day}
                </div>
              ))}
            </div>

            <div className="grid grid-cols-7 gap-1">
              {generateCalendarDays().map((day, index) => (
                <button
                  key={index}
                  onClick={() => !day.isDisabled && handleDateSelect(day.date)}
                  disabled={day.isDisabled}
                  className={`text-sm p-2 hover:bg-background-base rounded ${
                    !day.isCurrentMonth ? 'text-text-muted' : 'text-text-base'
                  } ${
                    day.isSelected ? 'bg-primary-500 text-white hover:bg-primary-600' : ''
                  } ${
                    day.isToday && !day.isSelected ? 'bg-background-base' : ''
                  } ${
                    day.isDisabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'
                  }`}
                >
                  {day.day}
                </button>
              ))}
            </div>

            <div className="flex justify-end mt-4 pt-2 border-t border-border-base">
              <Button
                variant="secondary"
                size="sm"
                onClick={() => setIsOpen(false)}
              >
                Cancel
              </Button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default DatePicker;
'''

    def generate_switch_component(self, spec: ComponentSpec) -> str:
        """Generate a Switch/Toggle component."""
        return '''import React from 'react';

interface SwitchProps {
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  disabled?: boolean;
  size?: 'sm' | 'md' | 'lg';
  label?: string;
}

export const Switch: React.FC<SwitchProps> = ({
  checked = false,
  onChange,
  disabled = false,
  size = 'md',
  label
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange?.(e.target.checked);
  };

  const sizeClasses = {
    sm: {
      switch: 'h-4 w-7',
      knob: 'h-3 w-3',
      translate: 'translate-x-3'
    },
    md: {
      switch: 'h-5 w-9',
      knob: 'h-4 w-4',
      translate: 'translate-x-4'
    },
    lg: {
      switch: 'h-6 w-11',
      knob: 'h-5 w-5',
      translate: 'translate-x-5'
    }
  };

  return (
    <label className={`inline-flex items-center ${disabled ? 'cursor-not-allowed' : 'cursor-pointer'}`}>
      <div className="relative">
        <input
          type="checkbox"
          className="sr-only"
          checked={checked}
          onChange={handleChange}
          disabled={disabled}
        />
        <div
          className={`relative rounded-full transition-colors ${
            checked ? 'bg-primary-500' : 'bg-border-base'
          } ${sizeClasses[size].switch} ${disabled ? 'opacity-50' : ''}`}
        >
          <div
            className={`absolute top-0.5 left-0.5 bg-white rounded-full shadow transition-transform ${
              sizeClasses[size].knob
            } ${checked ? sizeClasses[size].translate : ''}`}
          />
        </div>
      </div>
      {label && (
        <span className={`ml-3 ${size === 'sm' ? 'text-sm' : size === 'lg' ? 'text-lg' : 'text-base'} ${
          disabled ? 'text-text-muted' : 'text-text-base'
        }`}>
          {label}
        </span>
      )}
    </label>
  );
};

export default Switch;
'''

    def generate_progress_component(self, spec: ComponentSpec) -> str:
        """Generate a Progress component."""
        return '''import React from 'react';

interface ProgressProps {
  value?: number;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'success' | 'warning' | 'error';
  showLabel?: boolean;
  label?: string;
  animated?: boolean;
}

export const Progress: React.FC<ProgressProps> = ({
  value = 0,
  max = 100,
  size = 'md',
  variant = 'default',
  showLabel = false,
  label,
  animated = false
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  const sizeClasses = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3'
  };

  const variantClasses = {
    default: 'bg-primary-500',
    success: 'bg-success-500',
    warning: 'bg-warning-500',
    error: 'bg-error-500'
  };

  return (
    <div className="w-full">
      {(showLabel || label) && (
        <div className="flex justify-between items-center mb-2">
          {label && <span className="text-sm font-medium text-text-base">{label}</span>}
          {showLabel && <span className="text-sm text-text-muted">{Math.round(percentage)}%</span>}
        </div>
      )}

      <div className={`w-full bg-background-base rounded-full overflow-hidden ${sizeClasses[size]}`}>
        <div
          className={`h-full ${variantClasses[variant]} transition-all duration-300 ease-out ${
            animated ? 'transition-all duration-500' : ''
          }`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default Progress;
'''

    def generate_accordion_component(self, spec: ComponentSpec) -> str:
        """Generate an Accordion component."""
        return '''import React, { useState } from 'react';

interface AccordionItem {
  id: string;
  title: string;
  content: React.ReactNode;
  disabled?: boolean;
}

interface AccordionProps {
  items: AccordionItem[];
  multiple?: boolean;
  defaultExpanded?: string[];
  size?: 'sm' | 'md' | 'lg';
}

export const Accordion: React.FC<AccordionProps> = ({
  items,
  multiple = false,
  defaultExpanded = [],
  size = 'md'
}) => {
  const [expandedItems, setExpandedItems] = useState<Set<string>>(
    new Set(defaultExpanded)
  );

  const toggleItem = (itemId: string) => {
    const newExpanded = new Set(expandedItems);

    if (multiple) {
      if (newExpanded.has(itemId)) {
        newExpanded.delete(itemId);
      } else {
        newExpanded.add(itemId);
      }
    } else {
      if (newExpanded.has(itemId)) {
        newExpanded.clear();
      } else {
        newExpanded.clear();
        newExpanded.add(itemId);
      }
    }

    setExpandedItems(newExpanded);
  };

  const sizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  };

  return (
    <div className="space-y-2">
      {items.map((item) => {
        const isExpanded = expandedItems.has(item.id);
        const isDisabled = item.disabled;

        return (
          <div key={item.id} className="border border-border-base rounded-md">
            <button
              onClick={() => !isDisabled && toggleItem(item.id)}
              disabled={isDisabled}
              className={`w-full flex items-center justify-between p-4 text-left ${
                sizeClasses[size]
              } font-medium hover:bg-background-surface focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-inset ${
                isDisabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'
              }`}
            >
              <span className={isDisabled ? 'text-text-muted' : 'text-text-base'}>
                {item.title}
              </span>
              <svg
                className={`w-5 h-5 text-text-muted transition-transform ${
                  isExpanded ? 'rotate-180' : ''
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {isExpanded && (
              <div className="px-4 pb-4">
                <div className="text-text-base">
                  {item.content}
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default Accordion;
'''

    def generate_breadcrumb_component(self, spec: ComponentSpec) -> str:
        """Generate a Breadcrumb component."""
        return '''import React from 'react';

interface BreadcrumbItem {
  label: string;
  href?: string;
  onClick?: () => void;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  separator?: React.ReactNode;
  size?: 'sm' | 'md' | 'lg';
  maxItems?: number;
}

export const Breadcrumb: React.FC<BreadcrumbProps> = ({
  items,
  separator,
  size = 'md',
  maxItems
}) => {
  const displayItems = maxItems && items.length > maxItems
    ? [
        items[0],
        { label: '...', disabled: true },
        ...items.slice(-maxItems + 2)
      ]
    : items;

  const sizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  };

  const defaultSeparator = (
    <svg className="w-4 h-4 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
    </svg>
  );

  return (
    <nav aria-label="Breadcrumb">
      <ol className="flex items-center space-x-2">
        {displayItems.map((item, index) => {
          const isLast = index === displayItems.length - 1;
          const isDisabled = item.disabled;

          return (
            <li key={index} className="flex items-center">
              {index > 0 && (
                <span className="mx-2 text-text-muted">
                  {separator || defaultSeparator}
                </span>
              )}

              {isLast || isDisabled ? (
                <span className={`${sizeClasses[size]} text-text-muted`}>
                  {item.label}
                </span>
              ) : item.href ? (
                <a
                  href={item.href}
                  className={`${sizeClasses[size]} text-primary-600 hover:text-primary-800 transition-colors`}
                >
                  {item.label}
                </a>
              ) : (
                <button
                  onClick={item.onClick}
                  className={`${sizeClasses[size]} text-primary-600 hover:text-primary-800 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded`}
                >
                  {item.label}
                </button>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
};

export default Breadcrumb;
'''

    def generate_skeleton_component(self, spec: ComponentSpec) -> str:
        """Generate a Skeleton component."""
        return '''import React from 'react';

interface SkeletonProps {
  variant?: 'text' | 'rectangular' | 'circular';
  width?: string | number;
  height?: string | number;
  animation?: 'pulse' | 'wave' | 'none';
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  variant = 'text',
  width,
  height,
  animation = 'pulse',
  className = ''
}) => {
  const baseClasses = 'bg-background-base';

  const animationClasses = {
    pulse: 'animate-pulse',
    wave: 'animate-pulse', // Could be enhanced with a wave animation
    none: ''
  };

  const variantClasses = {
    text: 'rounded',
    rectangular: 'rounded-md',
    circular: 'rounded-full'
  };

  const getDimensions = () => {
    if (variant === 'text') {
      return {
        height: height || '1rem',
        width: width || '100%'
      };
    }

    if (variant === 'circular') {
      const size = width || height || '2rem';
      return {
        width: size,
        height: size
      };
    }

    return {
      width: width || '100%',
      height: height || '2rem'
    };
  };

  const dimensions = getDimensions();

  return (
    <div
      className={`${baseClasses} ${variantClasses[variant]} ${animationClasses[animation]} ${className}`}
      style={{
        width: dimensions.width,
        height: dimensions.height
      }}
    />
  );
};

// Compound component for common skeleton patterns
interface SkeletonTextProps {
  lines?: number;
  className?: string;
}

export const SkeletonText: React.FC<SkeletonTextProps> = ({
  lines = 3,
  className = ''
}) => (
  <div className={`space-y-2 ${className}`}>
    {Array.from({ length: lines }, (_, i) => (
      <Skeleton
        key={i}
        variant="text"
        width={i === lines - 1 ? '60%' : '100%'}
      />
    ))}
  </div>
);

interface SkeletonCardProps {
  showAvatar?: boolean;
  lines?: number;
  className?: string;
}

export const SkeletonCard: React.FC<SkeletonCardProps> = ({
  showAvatar = false,
  lines = 3,
  className = ''
}) => (
  <div className={`p-4 border border-border-base rounded-md ${className}`}>
    {showAvatar && (
      <div className="flex items-center space-x-3 mb-3">
        <Skeleton variant="circular" width="2.5rem" height="2.5rem" />
        <div className="space-y-1 flex-1">
          <Skeleton variant="text" width="60%" height="1rem" />
          <Skeleton variant="text" width="40%" height="0.75rem" />
        </div>
      </div>
    )}
    <SkeletonText lines={lines} />
  </div>
);

export default Skeleton;
'''

    def generate_pagination_component(self, spec: ComponentSpec) -> str:
        """Generate a Pagination component."""
        return '''import React from 'react';
import { Button } from './Button';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  showFirstLast?: boolean;
  showPageNumbers?: boolean;
  maxPageNumbers?: number;
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

export const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
  showFirstLast = true,
  showPageNumbers = true,
  maxPageNumbers = 5,
  size = 'md',
  disabled = false
}) => {
  const getPageNumbers = () => {
    const pages = [];
    const half = Math.floor(maxPageNumbers / 2);

    let start = Math.max(1, currentPage - half);
    let end = Math.min(totalPages, start + maxPageNumbers - 1);

    if (end - start + 1 < maxPageNumbers) {
      start = Math.max(1, end - maxPageNumbers + 1);
    }

    for (let i = start; i <= end; i++) {
      pages.push(i);
    }

    return pages;
  };

  const sizeClasses = {
    sm: 'text-sm px-2 py-1',
    md: 'text-base px-3 py-2',
    lg: 'text-lg px-4 py-2'
  };

  if (totalPages <= 1) return null;

  return (
    <nav className="flex items-center justify-between" aria-label="Pagination">
      <div className="flex items-center space-x-1">
        {showFirstLast && (
          <Button
            variant="secondary"
            size="sm"
            disabled={disabled || currentPage === 1}
            onClick={() => onPageChange(1)}
            className={sizeClasses[size]}
          >
            First
          </Button>
        )}

        <Button
          variant="secondary"
          size="sm"
          disabled={disabled || currentPage === 1}
          onClick={() => onPageChange(currentPage - 1)}
          className={sizeClasses[size]}
        >
          Previous
        </Button>

        {showPageNumbers && (
          <div className="flex items-center space-x-1">
            {getPageNumbers().map((page) => (
              <button
                key={page}
                onClick={() => onPageChange(page)}
                disabled={disabled}
                className={`relative inline-flex items-center justify-center rounded-md transition-colors ${
                  page === currentPage
                    ? 'bg-primary-500 text-white'
                    : 'text-text-base hover:bg-background-surface'
                } ${sizeClasses[size]} ${
                  disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'
                }`}
              >
                {page}
              </button>
            ))}
          </div>
        )}

        <Button
          variant="secondary"
          size="sm"
          disabled={disabled || currentPage === totalPages}
          onClick={() => onPageChange(currentPage + 1)}
          className={sizeClasses[size]}
        >
          Next
        </Button>

        {showFirstLast && (
          <Button
            variant="secondary"
            size="sm"
            disabled={disabled || currentPage === totalPages}
            onClick={() => onPageChange(totalPages)}
            className={sizeClasses[size]}
          >
            Last
          </Button>
        )}
      </div>

      <div className="text-sm text-neutral-700">
        Page {currentPage} of {totalPages}
      </div>
    </nav>
  );
};

export default Pagination;
'''

    def generate_search_component(self, spec: ComponentSpec) -> str:
        """Generate a Search component."""
        return '''import React, { useState, useRef, useEffect } from 'react';
import { Input } from './Input';

interface SearchResult {
  id: string;
  title: string;
  description?: string;
  category?: string;
}

interface SearchProps {
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  onSearch?: (query: string) => void;
  results?: SearchResult[];
  onResultSelect?: (result: SearchResult) => void;
  loading?: boolean;
  disabled?: boolean;
  debounceMs?: number;
  showSuggestions?: boolean;
}

export const Search: React.FC<SearchProps> = ({
  placeholder = 'Search...',
  value = '',
  onChange,
  onSearch,
  results = [],
  onResultSelect,
  loading = false,
  disabled = false,
  debounceMs = 300,
  showSuggestions = true
}) => {
  const [internalValue, setInternalValue] = useState(value);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const debounceRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    setInternalValue(value);
  }, [value]);

  const handleInputChange = (newValue: string) => {
    setInternalValue(newValue);
    setSelectedIndex(-1);
    onChange?.(newValue);

    // Debounced search
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    debounceRef.current = setTimeout(() => {
      onSearch?.(newValue);
      setIsOpen(newValue.length > 0 && showSuggestions);
    }, debounceMs);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!isOpen || results.length === 0) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => Math.min(prev + 1, results.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => Math.max(prev - 1, -1));
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && results[selectedIndex]) {
          handleResultSelect(results[selectedIndex]);
        } else {
          onSearch?.(internalValue);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        setSelectedIndex(-1);
        inputRef.current?.blur();
        break;
    }
  };

  const handleResultSelect = (result: SearchResult) => {
    setInternalValue(result.title);
    setIsOpen(false);
    setSelectedIndex(-1);
    onResultSelect?.(result);
    onChange?.(result.title);
  };

  const handleFocus = () => {
    if (internalValue && showSuggestions) {
      setIsOpen(true);
    }
  };

  const handleBlur = () => {
    // Delay closing to allow for result clicks
    setTimeout(() => setIsOpen(false), 150);
  };

  return (
    <div className="relative">
      <div className="relative">
        <Input
          ref={inputRef}
          type="text"
          placeholder={placeholder}
          value={internalValue}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={handleFocus}
          onBlur={handleBlur}
          disabled={disabled}
          className="pr-10"
        />
        <div className="absolute inset-y-0 right-0 flex items-center pr-3">
          {loading ? (
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-text-muted"></div>
          ) : (
            <svg className="h-4 w-4 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          )}
        </div>
      </div>

      {isOpen && results.length > 0 && (
        <div className="absolute z-50 w-full mt-1 bg-background-surface border border-border-base rounded-md shadow-lg max-h-60 overflow-y-auto">
          {results.map((result, index) => (
            <button
              key={result.id}
              onClick={() => handleResultSelect(result)}
              className={`w-full px-4 py-3 text-left hover:bg-background-base focus:outline-none focus:bg-background-base ${
                index === selectedIndex ? 'bg-background-base' : ''
              }`}
            >
              <div className="font-medium text-text-base">{result.title}</div>
              {result.description && (
                <div className="text-sm text-text-muted truncate">{result.description}</div>
              )}
              {result.category && (
                <div className="text-xs text-text-muted mt-1">{result.category}</div>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default Search;
'''

    def generate_textarea_component(self, spec: ComponentSpec) -> str:
        """Generate a Textarea component."""
        return '''import React, { useState } from 'react';

interface TextareaProps {
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  error?: boolean;
  disabled?: boolean;
  required?: boolean;
  rows?: number;
  maxLength?: number;
  resize?: 'none' | 'vertical' | 'horizontal' | 'both';
}

export const Textarea: React.FC<TextareaProps> = ({
  placeholder,
  value,
  onChange,
  error = false,
  disabled = false,
  required = false,
  rows = 4,
  maxLength,
  resize = 'vertical'
}) => {
  const [internalValue, setInternalValue] = useState(value || '');

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    if (maxLength && newValue.length > maxLength) return;

    setInternalValue(newValue);
    onChange?.(newValue);
  };

  const resizeClass = {
    none: 'resize-none',
    vertical: 'resize-y',
    horizontal: 'resize-x',
    both: 'resize'
  };

  const baseClasses = 'w-full px-3 py-2 bg-background-base text-text-base border border-border-base rounded-md shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-background-surface disabled:text-text-muted disabled:cursor-not-allowed transition-colors';

  const stateClasses = error
    ? 'border-error-500 text-error-500 placeholder-error-300 focus:ring-error-500 focus:border-error-500'
    : 'border-border-base text-text-base';

  const classes = baseClasses + ' ' + stateClasses + ' ' + resizeClass[resize];

  return (
    <div className="relative">
      <textarea
        className={classes}
        placeholder={placeholder}
        value={internalValue}
        onChange={handleChange}
        disabled={disabled}
        required={required}
        rows={rows}
        maxLength={maxLength}
        aria-invalid={error}
      />
      {maxLength && (
        <div className="absolute bottom-2 right-2 text-xs text-neutral-500">
          {internalValue.length}/{maxLength}
        </div>
      )}
    </div>
  );
};

export default Textarea;
'''

    def generate_checkbox_component(self, spec: ComponentSpec) -> str:
        """Generate a Checkbox component."""
        return '''import React from 'react';

interface CheckboxProps {
  label?: string;
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  disabled?: boolean;
  required?: boolean;
  indeterminate?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export const Checkbox: React.FC<CheckboxProps> = ({
  label,
  checked = false,
  onChange,
  disabled = false,
  required = false,
  indeterminate = false,
  size = 'md'
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange?.(e.target.checked);
  };

  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6'
  };

  const textSizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  };

  return (
    <label className={`flex items-center space-x-3 cursor-pointer ${disabled ? 'cursor-not-allowed' : ''}`}>
      <input
        type="checkbox"
        className={`${sizeClasses[size]} text-primary-600 bg-background-base border-border-base rounded focus:ring-primary-500 focus:ring-2 disabled:bg-background-surface disabled:text-text-muted ${indeterminate ? 'indeterminate' : ''}`}
        checked={checked}
        onChange={handleChange}
        disabled={disabled}
        required={required}
        ref={(el) => {
          if (el) el.indeterminate = indeterminate;
        }}
      />
      {label && (
        <span className={`${textSizeClasses[size]} text-text-base ${disabled ? 'text-text-muted' : ''}`}>
          {label}
        </span>
      )}
    </label>
  );
};

export default Checkbox;
'''

    def generate_radio_component(self, spec: ComponentSpec) -> str:
        """Generate a Radio component."""
        return '''import React from 'react';

interface RadioOption {
  value: string;
  label: string;
  disabled?: boolean;
}

interface RadioProps {
  options: RadioOption[];
  value?: string;
  onChange?: (value: string) => void;
  disabled?: boolean;
  required?: boolean;
  size?: 'sm' | 'md' | 'lg';
  orientation?: 'vertical' | 'horizontal';
}

export const Radio: React.FC<RadioProps> = ({
  options,
  value,
  onChange,
  disabled = false,
  required = false,
  size = 'md',
  orientation = 'vertical'
}) => {
  const handleChange = (optionValue: string) => {
    onChange?.(optionValue);
  };

  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6'
  };

  const textSizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  };

  const containerClasses = orientation === 'horizontal'
    ? 'flex flex-wrap gap-6'
    : 'space-y-3';

  return (
    <div className={containerClasses}>
      {options.map((option) => {
        const isDisabled = disabled || option.disabled;
        const isChecked = value === option.value;

        return (
          <label
            key={option.value}
            className={`flex items-center space-x-3 cursor-pointer ${isDisabled ? 'cursor-not-allowed' : ''}`}
          >
            <input
              type="radio"
              className={`${sizeClasses[size]} text-primary-600 bg-background-base border-border-base focus:ring-primary-500 focus:ring-2 disabled:bg-background-surface disabled:text-text-muted`}
              value={option.value}
              checked={isChecked}
              onChange={() => handleChange(option.value)}
              disabled={isDisabled}
              required={required}
              name="radio-group"
            />
            <span className={`${textSizeClasses[size]} text-text-base ${isDisabled ? 'text-text-muted' : ''}`}>
              {option.label}
            </span>
          </label>
        );
      })}
    </div>
  );
};

export default Radio;
'''

    def generate_badge_component(self, spec: ComponentSpec) -> str:
        """Generate a Badge component."""
        return '''import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info';
  size?: 'sm' | 'md' | 'lg';
  rounded?: boolean;
  dot?: boolean;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  rounded = false,
  dot = false
}) => {
  const variantClasses = {
    primary: 'bg-primary-100 text-primary-800',
    secondary: 'bg-background-surface text-text-base',
    success: 'bg-success-100 text-success-800',
    warning: 'bg-warning-100 text-warning-800',
    error: 'bg-error-100 text-error-800',
    info: 'bg-info-100 text-info-800'
  };

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-0.5 text-sm',
    lg: 'px-3 py-1 text-base'
  };

  const roundedClass = rounded ? 'rounded-full' : 'rounded-md';

  if (dot) {
    return (
      <div className="flex items-center space-x-2">
        <div className={`h-2 w-2 rounded-full bg-${variant}-500`} />
        <span className="text-sm text-text-base">{children}</span>
      </div>
    );
  }

  return (
    <span className={`${sizeClasses[size]} ${variantClasses[variant]} ${roundedClass} font-medium inline-flex items-center`}>
      {children}
    </span>
  );
};

export default Badge;
'''

    def generate_tooltip_component(self, spec: ComponentSpec) -> str:
        """Generate a Tooltip component."""
        return '''import React, { useState, useRef } from 'react';

interface TooltipProps {
  content: string;
  children: React.ReactNode;
  position?: 'top' | 'bottom' | 'left' | 'right';
  delay?: number;
  disabled?: boolean;
}

export const Tooltip: React.FC<TooltipProps> = ({
  content,
  children,
  position = 'top',
  delay = 300,
  disabled = false
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [timeoutId, setTimeoutId] = useState<NodeJS.Timeout | null>(null);
  const triggerRef = useRef<HTMLDivElement>(null);

  const showTooltip = () => {
    if (disabled) return;
    const id = setTimeout(() => setIsVisible(true), delay);
    setTimeoutId(id);
  };

  const hideTooltip = () => {
    if (timeoutId) {
      clearTimeout(timeoutId);
      setTimeoutId(null);
    }
    setIsVisible(false);
  };

  const positionClasses = {
    top: 'bottom-full left-1/2 transform -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 transform -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 transform -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 transform -translate-y-1/2 ml-2'
  };

  const arrowClasses = {
    top: 'top-full left-1/2 transform -translate-x-1/2 border-l-transparent border-r-transparent border-b-transparent',
    bottom: 'bottom-full left-1/2 transform -translate-x-1/2 border-l-transparent border-r-transparent border-t-transparent',
    left: 'left-full top-1/2 transform -translate-y-1/2 border-t-transparent border-b-transparent border-l-transparent',
    right: 'right-full top-1/2 transform -translate-y-1/2 border-t-transparent border-b-transparent border-r-transparent'
  };

  return (
    <div className="relative inline-block">
      <div
        ref={triggerRef}
        onMouseEnter={showTooltip}
        onMouseLeave={hideTooltip}
        onFocus={showTooltip}
        onBlur={hideTooltip}
        className="inline-block"
      >
        {children}
      </div>

      {isVisible && (
        <div
          className={`absolute z-50 ${positionClasses[position]} pointer-events-none`}
          role="tooltip"
        >
          <div className="bg-text-base text-background-base text-sm px-3 py-2 rounded-md shadow-lg max-w-xs whitespace-nowrap">
            {content}
            <div
              className={`absolute w-0 h-0 border-4 border-text-base ${arrowClasses[position]}`}
              style={{ borderWidth: '4px' }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Tooltip;
'''

    def generate_tabs_component(self, spec: ComponentSpec) -> str:
        """Generate a Tabs component."""
        return '''import React, { useState } from 'react';

interface TabItem {
  id: string;
  label: string;
  content: React.ReactNode;
  disabled?: boolean;
}

interface TabsProps {
  tabs: TabItem[];
  defaultTab?: string;
  onChange?: (tabId: string) => void;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'underline' | 'pills' | 'buttons';
}

export const Tabs: React.FC<TabsProps> = ({
  tabs,
  defaultTab,
  onChange,
  size = 'md',
  variant = 'underline'
}) => {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id);

  const handleTabClick = (tabId: string) => {
    if (tabs.find(tab => tab.id === tabId)?.disabled) return;
    setActiveTab(tabId);
    onChange?.(tabId);
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  const getTabClasses = (tabId: string, isDisabled: boolean) => {
    const baseClasses = `font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${sizeClasses[size]}`;

    if (isDisabled) {
      return `${baseClasses} text-text-muted cursor-not-allowed`;
    }

    const isActive = activeTab === tabId;

    if (variant === 'underline') {
      return `${baseClasses} border-b-2 ${isActive ? 'border-primary-500 text-primary-600' : 'border-transparent text-text-muted hover:text-text-base hover:border-border-base'}`;
    } else if (variant === 'pills') {
      return `${baseClasses} rounded-md ${isActive ? 'bg-primary-100 text-primary-700' : 'text-text-muted hover:text-text-base hover:bg-background-surface'}`;
    } else { // buttons
      return `${baseClasses} rounded-md border ${isActive ? 'bg-primary-50 border-primary-200 text-primary-700' : 'border-border-base text-text-base hover:bg-background-surface'}`;
    }
  };

  const containerClasses = variant === 'underline'
    ? 'border-b border-border-base'
    : 'bg-background-base p-1 rounded-lg inline-flex';

  return (
    <div>
      <div className={containerClasses}>
        <div className={variant === 'underline' ? 'flex space-x-8' : 'flex space-x-1'}>
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => handleTabClick(tab.id)}
              disabled={tab.disabled}
              className={getTabClasses(tab.id, tab.disabled || false)}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-4">
        {tabs.find(tab => tab.id === activeTab)?.content}
      </div>
    </div>
  );
};

export default Tabs;
'''

    def generate_card_component(self, spec: ComponentSpec) -> str:
        """Generate a Card component."""
        return '''import React from 'react';

interface CardProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  headerActions?: React.ReactNode;
  footer?: React.ReactNode;
  variant?: 'default' | 'elevated' | 'outlined' | 'filled';
  size?: 'sm' | 'md' | 'lg';
  hover?: boolean;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({
  children,
  title,
  subtitle,
  headerActions,
  footer,
  variant = 'default',
  size = 'md',
  hover = false,
  onClick
}) => {
  const variantClasses = {
    default: 'bg-background-surface border border-border-base',
    elevated: 'bg-background-surface border border-border-base shadow-lg',
    outlined: 'bg-background-surface border-2 border-border-base',
    filled: 'bg-background-base border border-border-base'
  };

  const sizeClasses = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  };

  const baseClasses = `rounded-lg transition-shadow ${variantClasses[variant]} ${sizeClasses[size]} ${hover ? 'hover:shadow-md cursor-pointer' : ''} ${onClick ? 'cursor-pointer' : ''}`;

  const content = (
    <>
      {(title || subtitle || headerActions) && (
        <div className="flex items-start justify-between mb-4">
          <div>
            {title && <h3 className="text-lg font-semibold text-text-base">{title}</h3>}
            {subtitle && <p className="text-sm text-text-muted mt-1">{subtitle}</p>}
          </div>
          {headerActions && <div className="flex items-center space-x-2">{headerActions}</div>}
        </div>
      )}

      <div className="text-text-base">
        {children}
      </div>

      {footer && (
        <div className="mt-6 pt-4 border-t border-neutral-200">
          {footer}
        </div>
      )}
    </>
  );

  if (onClick) {
    return (
      <div className={baseClasses} onClick={onClick} role="button" tabIndex={0}>
        {content}
      </div>
    );
  }

  return (
    <div className={baseClasses}>
      {content}
    </div>
  );
};

export default Card;
'''

    def generate_avatar_component(self, spec: ComponentSpec) -> str:
        """Generate an Avatar component."""
        return '''import React from 'react';

interface AvatarProps {
  src?: string;
  alt?: string;
  name?: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
  variant?: 'circle' | 'square' | 'rounded';
  status?: 'online' | 'offline' | 'away' | 'busy';
  showStatus?: boolean;
  fallback?: React.ReactNode;
}

export const Avatar: React.FC<AvatarProps> = ({
  src,
  alt,
  name,
  size = 'md',
  variant = 'circle',
  status,
  showStatus = false,
  fallback
}) => {
  const sizeClasses = {
    xs: 'h-6 w-6 text-xs',
    sm: 'h-8 w-8 text-sm',
    md: 'h-10 w-10 text-base',
    lg: 'h-12 w-12 text-lg',
    xl: 'h-16 w-16 text-xl',
    '2xl': 'h-20 w-20 text-2xl'
  };

  const variantClasses = {
    circle: 'rounded-full',
    square: 'rounded-none',
    rounded: 'rounded-md'
  };

  const statusColors = {
    online: 'bg-green-400',
    offline: 'bg-text-muted',
    away: 'bg-yellow-400',
    busy: 'bg-red-400'
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(word => word.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const renderContent = () => {
    if (src) {
      return <img src={src} alt={alt || name} className="h-full w-full object-cover" />;
    }

    if (fallback) {
      return fallback;
    }

    if (name) {
      return (
        <span className="font-medium text-neutral-700">
          {getInitials(name)}
        </span>
      );
    }

    return (
      <svg
        className="h-full w-full text-neutral-400"
        fill="currentColor"
        viewBox="0 0 24 24"
      >
        <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
    );
  };

  return (
    <div className="relative inline-block">
      <div
        className={`inline-flex items-center justify-center overflow-hidden bg-neutral-200 ${sizeClasses[size]} ${variantClasses[variant]}`}
      >
        {renderContent()}
      </div>

      {showStatus && status && (
        <div
          className={`absolute -bottom-0.5 -right-0.5 h-3 w-3 ${statusColors[status]} border-2 border-white rounded-full`}
          aria-label={`${status} status`}
        />
      )}
    </div>
  );
};

export default Avatar;
'''

    def generate_datepicker_stories(self) -> str:
        """Generate Storybook stories for the DatePicker component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { DatePicker } from './DatePicker';

const meta: Meta<typeof DatePicker> = {
  title: 'Components/DatePicker',
  component: DatePicker,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A date picker component with an interactive calendar interface.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    format: {
      control: 'text',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    placeholder: 'Select a date',
  },
};

export const WithValue: Story = {
  args: {
    value: new Date(),
    placeholder: 'Select a date',
  },
};

export const Disabled: Story = {
  args: {
    placeholder: 'Disabled date picker',
    disabled: true,
  },
};

export const WithMinMax: Story = {
  args: {
    placeholder: 'Select date (limited range)',
    minDate: new Date(),
    maxDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days from now
  },
};

export const Required: Story = {
  args: {
    placeholder: 'Required date selection',
    required: true,
  },
};
'''

    def generate_switch_stories(self) -> str:
        """Generate Storybook stories for the Switch component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Switch } from './Switch';

const meta: Meta<typeof Switch> = {
  title: 'Components/Switch',
  component: Switch,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A toggle switch component for boolean settings and preferences.',
      },
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    label: 'Enable notifications',
  },
};

export const Checked: Story = {
  args: {
    label: 'Dark mode enabled',
    checked: true,
  },
};

export const Small: Story = {
  args: {
    label: 'Small switch',
    size: 'sm',
  },
};

export const Large: Story = {
  args: {
    label: 'Large switch',
    size: 'lg',
  },
};

export const Disabled: Story = {
  args: {
    label: 'Disabled switch',
    disabled: true,
  },
};

export const DisabledChecked: Story = {
  args: {
    label: 'Disabled and checked',
    disabled: true,
    checked: true,
  },
};

export const NoLabel: Story = {
  args: {},
};
'''

    def generate_progress_stories(self) -> str:
        """Generate Storybook stories for the Progress component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Progress } from './Progress';

const meta: Meta<typeof Progress> = {
  title: 'Components/Progress',
  component: Progress,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A progress indicator component for showing loading states and completion.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    value: {
      control: { type: 'range', min: 0, max: 100 },
    },
    max: {
      control: 'number',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    value: 65,
  },
};

export const WithLabel: Story = {
  args: {
    value: 75,
    showLabel: true,
    label: 'Upload progress',
  },
};

export const Success: Story = {
  args: {
    value: 100,
    variant: 'success',
    showLabel: true,
    label: 'Complete',
  },
};

export const Warning: Story = {
  args: {
    value: 25,
    variant: 'warning',
    showLabel: true,
    label: 'Processing',
  },
};

export const Error: Story = {
  args: {
    value: 15,
    variant: 'error',
    showLabel: true,
    label: 'Failed',
  },
};

export const Small: Story = {
  args: {
    value: 50,
    size: 'sm',
    showLabel: true,
  },
};

export const Large: Story = {
  args: {
    value: 80,
    size: 'lg',
    showLabel: true,
  },
};

export const Animated: Story = {
  args: {
    value: 45,
    animated: true,
    showLabel: true,
    label: 'Loading...',
  },
};
'''

    def generate_accordion_stories(self) -> str:
        """Generate Storybook stories for the Accordion component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Accordion } from './Accordion';

const meta: Meta<typeof Accordion> = {
  title: 'Components/Accordion',
  component: Accordion,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'A collapsible accordion component for organizing content into expandable panels.',
      },
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

const sampleItems = [
  {
    id: 'item1',
    title: 'Getting Started',
    content: (
      <div className="space-y-2">
        <p>Welcome to our platform! Here's how to get started:</p>
        <ul className="list-disc list-inside space-y-1 text-sm">
          <li>Create your account</li>
          <li>Set up your profile</li>
          <li>Explore the features</li>
        </ul>
      </div>
    ),
  },
  {
    id: 'item2',
    title: 'Account Settings',
    content: (
      <div className="space-y-3">
        <p>Manage your account preferences and settings.</p>
        <div className="bg-neutral-50 p-3 rounded">
          <p className="text-sm">Account settings panel content...</p>
        </div>
      </div>
    ),
  },
  {
    id: 'item3',
    title: 'Privacy & Security',
    content: (
      <div className="space-y-2">
        <p>Your privacy and security are important to us.</p>
        <p className="text-sm text-neutral-600">
          Learn about our data protection measures and security features.
        </p>
      </div>
    ),
  },
];

export const Single: Story = {
  args: {
    items: sampleItems,
    multiple: false,
  },
};

export const Multiple: Story = {
  args: {
    items: sampleItems,
    multiple: true,
  },
};

export const PreExpanded: Story = {
  args: {
    items: sampleItems,
    defaultExpanded: ['item2'],
  },
};

export const Small: Story = {
  args: {
    items: sampleItems.map(item => ({
      ...item,
      title: item.title.substring(0, 10) + '...'
    })),
    size: 'sm',
  },
};

export const Large: Story = {
  args: {
    items: sampleItems,
    size: 'lg',
  },
};

export const WithDisabled: Story = {
  args: {
    items: [
      ...sampleItems.slice(0, 2),
      {
        id: 'item3',
        title: 'Disabled Item',
        content: 'This item is disabled and cannot be expanded.',
        disabled: true,
      },
    ],
  },
};
'''

    def generate_breadcrumb_stories(self) -> str:
        """Generate Storybook stories for the Breadcrumb component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Breadcrumb } from './Breadcrumb';

const meta: Meta<typeof Breadcrumb> = {
  title: 'Components/Breadcrumb',
  component: Breadcrumb,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A breadcrumb navigation component for showing page hierarchy.',
      },
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

const sampleItems = [
  { label: 'Home', href: '/' },
  { label: 'Products', href: '/products' },
  { label: 'Electronics', href: '/products/electronics' },
  { label: 'Smartphones', href: '/products/electronics/smartphones' },
];

export const Default: Story = {
  args: {
    items: sampleItems,
  },
};

export const WithMaxItems: Story = {
  args: {
    items: [
      { label: 'Home', href: '/' },
      { label: 'Category', href: '/category' },
      { label: 'Subcategory', href: '/category/sub' },
      { label: 'Subsubcategory', href: '/category/sub/sub' },
      { label: 'Product', href: '/category/sub/sub/product' },
    ],
    maxItems: 4,
  },
};

export const Small: Story = {
  args: {
    items: sampleItems,
    size: 'sm',
  },
};

export const Large: Story = {
  args: {
    items: sampleItems,
    size: 'lg',
  },
};

export const WithOnClick: Story = {
  args: {
    items: sampleItems.map(item => ({
      ...item,
      onClick: () => console.log(`Clicked: ${item.label}`),
    })),
  },
};

export const CustomSeparator: Story = {
  args: {
    items: sampleItems,
    separator: '>',
  },
};
'''

    def generate_skeleton_stories(self) -> str:
        """Generate Storybook stories for the Skeleton component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Skeleton, SkeletonText, SkeletonCard } from './Skeleton';

const meta: Meta<typeof Skeleton> = {
  title: 'Components/Skeleton',
  component: Skeleton,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Skeleton loading components for displaying placeholder content while data loads.',
      },
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Text: Story = {
  args: {
    variant: 'text',
    width: '200px',
  },
};

export const Rectangular: Story = {
  args: {
    variant: 'rectangular',
    width: '200px',
    height: '100px',
  },
};

export const Circular: Story = {
  args: {
    variant: 'circular',
    width: '50px',
    height: '50px',
  },
};

export const NoAnimation: Story = {
  args: {
    variant: 'rectangular',
    width: '200px',
    height: '100px',
    animation: 'none',
  },
};

export const SkeletonTextStory = () => (
  <div>
    <h3 className="text-lg font-semibold mb-4">Loading Article</h3>
    <SkeletonText lines={4} />
  </div>
);

export const SkeletonCardStory = () => (
  <div className="space-y-4">
    <SkeletonCard />
    <SkeletonCard showAvatar={true} />
    <SkeletonCard showAvatar={true} lines={2} />
  </div>
);
'''

    def generate_pagination_stories(self) -> str:
        """Generate Storybook stories for the Pagination component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Pagination } from './Pagination';

const meta: Meta<typeof Pagination> = {
  title: 'Components/Pagination',
  component: Pagination,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A pagination component for navigating through large datasets and content.',
      },
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    currentPage: 1,
    totalPages: 10,
    onPageChange: (page) => console.log('Page changed to:', page),
  },
};

export const MiddlePage: Story = {
  args: {
    currentPage: 5,
    totalPages: 20,
    onPageChange: (page) => console.log('Page changed to:', page),
  },
};

export const LastPage: Story = {
  args: {
    currentPage: 15,
    totalPages: 15,
    onPageChange: (page) => console.log('Page changed to:', page),
  },
};

export const Small: Story = {
  args: {
    currentPage: 3,
    totalPages: 8,
    size: 'sm',
    onPageChange: (page) => console.log('Page changed to:', page),
  },
};

export const Large: Story = {
  args: {
    currentPage: 2,
    totalPages: 12,
    size: 'lg',
    onPageChange: (page) => console.log('Page changed to:', page),
  },
};

export const WithoutFirstLast: Story = {
  args: {
    currentPage: 4,
    totalPages: 10,
    showFirstLast: false,
    onPageChange: (page) => console.log('Page changed to:', page),
  },
};

export const WithoutPageNumbers: Story = {
  args: {
    currentPage: 5,
    totalPages: 10,
    showPageNumbers: false,
    onPageChange: (page) => console.log('Page changed to:', page),
  },
};

export const Disabled: Story = {
  args: {
    currentPage: 3,
    totalPages: 8,
    disabled: true,
    onPageChange: (page) => console.log('Page changed to:', page),
  },
};
'''

    def generate_search_stories(self) -> str:
        """Generate Storybook stories for the Search component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { useState } from 'react';
import { Search } from './Search';

const meta: Meta<typeof Search> = {
  title: 'Components/Search',
  component: Search,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A search input component with autocomplete suggestions and keyboard navigation.',
      },
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

const sampleResults = [
  { id: '1', title: 'React Components', description: 'Reusable UI components', category: 'Documentation' },
  { id: '2', title: 'React Hooks', description: 'State management and side effects', category: 'Documentation' },
  { id: '3', title: 'TypeScript Guide', description: 'Type-safe JavaScript development', category: 'Documentation' },
  { id: '4', title: 'Design System', description: 'Consistent UI patterns', category: 'Design' },
  { id: '5', title: 'Component Library', description: 'Pre-built components', category: 'Development' },
];

const SearchWithState = (args: any) => {
  const [results, setResults] = useState<typeof sampleResults>([]);

  const handleSearch = (query: string) => {
    if (query.length > 0) {
      const filtered = sampleResults.filter(item =>
        item.title.toLowerCase().includes(query.toLowerCase()) ||
        item.description?.toLowerCase().includes(query.toLowerCase())
      );
      setResults(filtered);
    } else {
      setResults([]);
    }
  };

  return (
    <Search
      {...args}
      results={results}
      onSearch={handleSearch}
    />
  );
};

export const Default: Story = {
  render: (args) => <SearchWithState {...args} />,
  args: {
    placeholder: 'Search documentation...',
  },
};

export const Loading: Story = {
  render: (args) => <SearchWithState {...args} />,
  args: {
    placeholder: 'Search...',
    loading: true,
  },
};

export const Disabled: Story = {
  args: {
    placeholder: 'Disabled search',
    disabled: true,
  },
};

export const NoSuggestions: Story = {
  args: {
    placeholder: 'Search without suggestions',
    showSuggestions: false,
  },
};

export const CustomDebounce: Story = {
  render: (args) => <SearchWithState {...args} />,
  args: {
    placeholder: 'Fast search (100ms)',
    debounceMs: 100,
  },
};
'''

    def generate_storybook_main_config(self) -> str:
        """Generate Storybook main configuration."""
        return '''/** @type { import('@storybook/react-vite').StorybookConfig } */
const config = {
  stories: ['../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  docs: {
    autodocs: 'tag',
  },
  typescript: {
    check: false,
    checkOptions: {},
    reactDocgen: 'react-docgen-typescript',
    reactDocgenTypescriptOptions: {
      shouldExtractLiteralValuesFromEnum: true,
      propFilter: (prop) => (prop.parent ? !/node_modules/.test(prop.parent.fileName) : true),
    },
  },
};

export default config;
'''

    def generate_readme(self, components: List[ComponentCode], design_principles: dict, product_context: str) -> str:
        """Generate a README for the component library."""
        component_list = "\n".join([f"- **{comp.name}** - {comp.file_path}" for comp in components])

        readme = f'''# Design System Components

Auto-generated React component library with TypeScript and Tailwind CSS.

## Overview

This component library was generated for: **{product_context}**

**Design Philosophy:** {design_principles.get('philosophy', 'N/A')}
**UI Density:** {design_principles.get('density', 'N/A')}
**Clarity:** {design_principles.get('clarity', 'N/A')}/10

## Components

This component library includes 24+ production-ready React components:

{component_list}

### Component Categories
- **Form Components**: Button, Input, Select, Textarea, Checkbox, Radio, DatePicker, Switch
- **Feedback Components**: Alert, Badge, Tooltip, Modal, Progress, Skeleton
- **Navigation Components**: Navigation, Tabs, Breadcrumb, Pagination
- **Layout Components**: Card, Accordion
- **Data Display**: Table, Avatar
- **Utility Components**: Search

Each component includes:
- Full TypeScript interfaces
- Accessibility features (ARIA attributes, keyboard navigation)
- Comprehensive Storybook documentation
- Automated Jest tests
- Responsive design with Tailwind CSS

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

## Build

```bash
npm run build
```

## Storybook

This component library includes a complete Storybook setup for interactive component documentation.

```bash
npm run storybook
```

Then open [http://localhost:6006](http://localhost:6006) to view the interactive component documentation.

Each component includes multiple stories showcasing:
- Different variants and sizes
- Interactive states (hover, focus, disabled)
- Usage examples with real data
- Accessibility features

## Testing

This component library includes comprehensive testing setup with Jest and React Testing Library.

```bash
npm test
npm run test:watch
npm run test:coverage
```

### Test Coverage

- **Unit tests** for all components
- **Accessibility testing** with jest-axe
- **Interaction testing** with user-event
- **Coverage reporting** with minimum thresholds

## Usage

```tsx
import {{ Button, Input, Modal }} from './src';

function App() {{
  return (
    <div>
      <Button variant="primary" onClick={{() => console.log('Clicked!')}}>
        Click me
      </Button>
      <Input placeholder="Enter text..." />
    </div>
  );
}}
```

## Design Tokens

All components use design tokens defined in `src/styles/variables.css`. The tokens include:

- **Colors**: Primary, neutral, and semantic color scales
- **Typography**: Heading and body text scales
- **Spacing**: Consistent spacing scale
- **Shadows**: Elevation system
- **Border Radius**: Consistent corner rounding

## Accessibility

All components are designed with accessibility in mind:
- Proper ARIA attributes
- Keyboard navigation support
- Screen reader compatibility
- WCAG 2.1 AA contrast compliance

## Customization

The components are built with Tailwind CSS and use CSS custom properties for theming. To customize:

1. Modify the CSS variables in `src/styles/variables.css`
2. Update the Tailwind config in `tailwind.config.js`
3. Rebuild the component library

## Generated Files

- `src/components/` - Individual component files
- `src/index.ts` - Component exports
- `src/styles/variables.css` - Design token variables
- `tailwind.config.js` - Tailwind configuration
- `package.json` - Package configuration
- `README.md` - This documentation

---

*Generated by Design System Generator - Autonomous AI-powered design system creation*
'''
        return readme



    def generate_storybook_preview_config(self) -> str:
        """Generate Storybook preview configuration."""
        return '''/** @type { import('@storybook/react').Preview } */
const preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
    docs: {
      toc: true,
    },
  },
  tags: ['autodocs'],
};

export default preview;
'''

    def generate_jest_config(self) -> str:
        """Generate Jest configuration."""
        return '''/** @type {import('jest').Config} */
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapping: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest',
  },
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.(ts|tsx|js)',
    '<rootDir>/src/**/*.(test|spec).(ts|tsx|js)',
  ],
  collectCoverageFrom: [
    'src/**/*.(ts|tsx)',
    '!src/**/*.stories.(ts|tsx)',
    '!src/**/*.d.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
'''

    def generate_setup_tests(self) -> str:
        """Generate setupTests.ts for Jest."""
        return '''import '@testing-library/jest-dom';
'''

    def generate_sidebar_tests(self) -> str:
        """Generate tests for the Sidebar component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Sidebar } from './Sidebar';

describe('Sidebar', () => {
  const items = [
    { label: 'Home', href: '/' },
    { label: 'Settings', href: '/settings' }
  ];

  it('renders brand name when not collapsed', () => {
    render(<Sidebar items={items} brandName="TestBrand" />);
    expect(screen.getByText('TestBrand')).toBeInTheDocument();
  });

  it('toggles collapse state', () => {
    const onToggle = jest.fn();
    render(<Sidebar items={items} onToggle={onToggle} />);
    fireEvent.click(screen.getByRole('button'));
    expect(onToggle).toHaveBeenCalled();
  });
});
'''

    def generate_header_tests(self) -> str:
        """Generate tests for the Header component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Header } from './Header';

describe('Header', () => {
  const links = [{ label: 'About', href: '/about' }];

  it('renders brand name', () => {
    render(<Header links={links} brandName="MyBrand" />);
    expect(screen.getByText('MyBrand')).toBeInTheDocument();
  });

  it('renders links', () => {
    render(<Header links={links} />);
    expect(screen.getByText('About')).toBeInTheDocument();
  });
});
'''

    def generate_footer_tests(self) -> str:
        """Generate tests for the Footer component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Footer } from './Footer';

describe('Footer', () => {
  const columns = [
    { title: 'Product', links: [{ label: 'Features', href: '#' }] }
  ];

  it('renders column titles', () => {
    render(<Footer columns={columns} />);
    expect(screen.getByText('Product')).toBeInTheDocument();
  });

  it('renders copyright text', () => {
    render(<Footer columns={columns} copyright="Custom Copyright" />);
    expect(screen.getByText('Custom Copyright')).toBeInTheDocument();
  });
});
'''

    def generate_hero_tests(self) -> str:
        """Generate tests for the Hero component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Hero } from './Hero';

describe('Hero', () => {
  it('renders title and subtitle', () => {
    render(<Hero title="Main Title" subtitle="Sub Heading" />);
    expect(screen.getByText('Main Title')).toBeInTheDocument();
    expect(screen.getByText('Sub Heading')).toBeInTheDocument();
  });

  it('renders primary action button', () => {
    render(<Hero title="X" subtitle="Y" primaryAction={{ label: 'Get Started', onClick: () => {} }} />);
    expect(screen.getByText('Get Started')).toBeInTheDocument();
  });
});
'''

    def generate_container_tests(self) -> str:
        """Generate tests for the Container component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Container } from './Container';

describe('Container', () => {
  it('renders children correctly', () => {
    render(<Container>Test Content</Container>);
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('applies correct size class', () => {
    const { container } = render(<Container size="sm">Content</Container>);
    expect(container.firstChild).toHaveClass('max-w-screen-sm');
  });

  it('centers content by default', () => {
    const { container } = render(<Container>Content</Container>);
    expect(container.firstChild).toHaveClass('mx-auto');
  });
});
'''

    def generate_stack_tests(self) -> str:
        """Generate tests for the Stack component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Stack } from './Stack';

describe('Stack', () => {
  it('renders children correctly', () => {
    render(<Stack><div>Item 1</div><div>Item 2</div></Stack>);
    expect(screen.getByText('Item 1')).toBeInTheDocument();
    expect(screen.getByText('Item 2')).toBeInTheDocument();
  });

  it('applies correct direction class', () => {
    const { container } = render(<Stack direction="row">Content</Stack>);
    expect(container.firstChild).toHaveClass('flex-row');
  });

  it('applies spacing class correctly', () => {
    const { container } = render(<Stack spacing={6}>Content</Stack>);
    expect(container.firstChild).toHaveClass('space-y-6');
  });
});
'''

    def generate_grid_tests(self) -> str:
        """Generate tests for the Grid component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Grid } from './Grid';

describe('Grid', () => {
  it('renders children correctly', () => {
    render(<Grid><div>Item 1</div></Grid>);
    expect(screen.getByText('Item 1')).toBeInTheDocument();
  });

  it('applies numeric columns correctly', () => {
    const { container } = render(<Grid cols={3}>Content</Grid>);
    expect(container.firstChild).toHaveClass('grid-cols-3');
  });

  it('applies responsive columns correctly', () => {
    const { container } = render(<Grid cols={{ sm: 1, md: 2, lg: 4 }}>Content</Grid>);
    expect(container.firstChild).toHaveClass('sm:grid-cols-1');
    expect(container.firstChild).toHaveClass('md:grid-cols-2');
    expect(container.firstChild).toHaveClass('lg:grid-cols-4');
  });
});
'''

    def generate_button_tests(self) -> str:
        """Generate Jest tests for the Button component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = jest.fn();
    const user = userEvent.setup();

    render(<Button onClick={handleClick}>Click me</Button>);

    await user.click(screen.getByRole('button', { name: /click me/i }));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies correct variant classes', () => {
    const { rerender } = render(<Button variant="primary">Button</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-primary-500');

    rerender(<Button variant="secondary">Button</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-neutral-100');
  });

  it('applies correct size classes', () => {
    const { rerender } = render(<Button size="sm">Button</Button>);
    expect(screen.getByRole('button')).toHaveClass('px-3', 'py-1.5', 'text-sm');

    rerender(<Button size="lg">Button</Button>);
    expect(screen.getByRole('button')).toHaveClass('px-6', 'py-3', 'text-lg');
  });

  it('shows loading spinner when loading', () => {
    render(<Button loading>Loading</Button>);

    const button = screen.getByRole('button');
    expect(button).toHaveAttribute('disabled');
    expect(button).toHaveClass('disabled:opacity-50', 'disabled:pointer-events-none');
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>);

    const button = screen.getByRole('button');
    expect(button).toHaveAttribute('disabled');
    expect(button).toHaveClass('disabled:opacity-50', 'disabled:pointer-events-none');
  });

  it('does not call onClick when disabled', async () => {
    const handleClick = jest.fn();
    const user = userEvent.setup();

    render(<Button disabled onClick={handleClick}>Disabled</Button>);

    await user.click(screen.getByRole('button'));

    expect(handleClick).not.toHaveBeenCalled();
  });
});
'''

    def generate_input_tests(self) -> str:
        """Generate Jest tests for the Input component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Input } from './Input';

describe('Input', () => {
  it('renders correctly with placeholder', () => {
    render(<Input placeholder="Enter name" />);
    expect(screen.getByPlaceholderText(/enter name/i)).toBeInTheDocument();
  });

  it('updates value on change', async () => {
    const handleChange = jest.fn();
    const user = userEvent.setup();
    render(<Input onChange={handleChange} />);
    
    const input = screen.getByRole('textbox');
    await user.type(input, 'Hello');
    
    expect(handleChange).toHaveBeenCalledWith('Hello');
  });

  it('shows error state', () => {
    render(<Input error />);
    expect(screen.getByRole('textbox')).toHaveClass('border-error-300');
  });

  it('is disabled when disabled prop is true', () => {
    render(<Input disabled />);
    expect(screen.getByRole('textbox')).toBeDisabled();
  });
});
'''

    def generate_alert_tests(self) -> str:
        """Generate Jest tests for the Alert component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Alert } from './Alert';

describe('Alert', () => {
  it('renders children correctly', () => {
    render(<Alert>Something happened</Alert>);
    expect(screen.getByText(/something happened/i)).toBeInTheDocument();
  });

  it('renders title if provided', () => {
    render(<Alert title="Success">Operation complete</Alert>);
    expect(screen.getByText(/success/i)).toBeInTheDocument();
  });

  it('calls onDismiss when close button is clicked', () => {
    const handleDismiss = jest.fn();
    render(<Alert onDismiss={handleDismiss}>Dismiss me</Alert>);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleDismiss).toHaveBeenCalledTimes(1);
  });

  it('applies correct variant classes', () => {
    const { rerender } = render(<Alert variant="error">Error message</Alert>);
    expect(screen.getByRole('alert')).toHaveClass('bg-error-50');

    rerender(<Alert variant="success">Success message</Alert>);
    expect(screen.getByRole('alert')).toHaveClass('bg-success-50');
  });
});
'''

    def generate_select_tests(self) -> str:
        """Generate Jest tests for the Select component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Select } from './Select';

const options = [
  { value: '1', label: 'Option 1' },
  { value: '2', label: 'Option 2' },
];

describe('Select', () => {
  it('renders with placeholder', () => {
    render(<Select options={options} placeholder="Choose one" />);
    expect(screen.getByText(/choose one/i)).toBeInTheDocument();
  });

  it('calls onChange when selection changes', () => {
    const handleChange = jest.fn();
    render(<Select options={options} onChange={handleChange} />);
    
    fireEvent.change(screen.getByRole('combobox'), { target: { value: '2' } });
    expect(handleChange).toHaveBeenCalledWith('2');
  });

  it('is disabled when disabled prop is true', () => {
    render(<Select options={options} disabled />);
    expect(screen.getByRole('combobox')).toBeDisabled();
  });
});
'''

    def generate_badge_tests(self) -> str:
        """Generate Jest tests for the Badge component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Badge } from './Badge';

describe('Badge', () => {
  it('renders children correctly', () => {
    render(<Badge>Active</Badge>);
    expect(screen.getByText(/active/i)).toBeInTheDocument();
  });

  it('applies correct variant classes', () => {
    const { rerender } = render(<Badge variant="success">Success</Badge>);
    expect(screen.getByText(/success/i)).toHaveClass('bg-success-100');

    rerender(<Badge variant="danger">Error</Badge>);
    expect(screen.getByText(/error/i)).toHaveClass('bg-error-100');
  });
});
'''

    def generate_card_tests(self) -> str:
        """Generate Jest tests for the Card component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Card } from './Card';

describe('Card', () => {
  it('renders children correctly', () => {
    render(<Card>Card content</Card>);
    expect(screen.getByText(/card content/i)).toBeInTheDocument();
  });

  it('renders with title', () => {
    render(<Card title="Card Title">Card content</Card>);
    expect(screen.getByText(/card title/i)).toBeInTheDocument();
  });

  it('applies elevated variant', () => {
    render(<Card variant="elevated">Content</Card>);
    expect(screen.getByRole('article')).toHaveClass('shadow-md');
  });
});
'''

    def generate_modal_tests(self) -> str:
        """Generate Jest tests for the Modal component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Modal } from './Modal';

describe('Modal', () => {
  it('does not render when its not open', () => {
    render(<Modal isOpen={false} onClose={() => {}}>Content</Modal>);
    expect(screen.queryByText(/content/i)).not.toBeInTheDocument();
  });

  it('renders when open', () => {
    render(<Modal isOpen={true} onClose={() => {}} title="Modal Title">Content</Modal>);
    expect(screen.getByText(/modal title/i)).toBeInTheDocument();
    expect(screen.getByText(/content/i)).toBeInTheDocument();
  });

  it('calls onClose when close button clicked', () => {
    const handleClose = jest.fn();
    render(<Modal isOpen={true} onClose={handleClose}>Content</Modal>);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClose).toHaveBeenCalledTimes(1);
  });
});
'''

    def generate_table_tests(self) -> str:
        """Generate Jest tests for the Table component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Table } from './Table';

const columns = [
  { key: 'name', header: 'Name' },
  { key: 'age', header: 'Age' },
];
const data = [
  { name: 'John', age: 30 },
  { name: 'Jane', age: 25 },
];

describe('Table', () => {
  it('renders headers correctly', () => {
    render(<Table columns={columns} data={data} />);
    expect(screen.getByText('Name')).toBeInTheDocument();
    expect(screen.getByText('Age')).toBeInTheDocument();
  });

  it('renders data correctly', () => {
    render(<Table columns={columns} data={data} />);
    expect(screen.getByText('John')).toBeInTheDocument();
    expect(screen.getByText('Jane')).toBeInTheDocument();
  });

  it('shows empty message when no data', () => {
    render(<Table columns={columns} data={[]} emptyMessage="No users found" />);
    expect(screen.getByText(/no users found/i)).toBeInTheDocument();
  });
});
'''

    def generate_tabs_tests(self) -> str:
        """Generate Jest tests for the Tabs component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Tabs } from './Tabs';

const tabs = [
  { id: '1', label: 'Tab 1', content: 'Content 1' },
  { id: '2', label: 'Tab 2', content: 'Content 2' },
];

describe('Tabs', () => {
  it('renders all tab labels', () => {
    render(<Tabs tabs={tabs} />);
    expect(screen.getByText('Tab 1')).toBeInTheDocument();
    expect(screen.getByText('Tab 2')).toBeInTheDocument();
  });

  it('shows active tab content by default', () => {
    render(<Tabs tabs={tabs} defaultTab="1" />);
    expect(screen.getByText('Content 1')).toBeInTheDocument();
  });

  it('changes content when tab is clicked', () => {
    render(<Tabs tabs={tabs} defaultTab="1" />);
    fireEvent.click(screen.getByText('Tab 2'));
    expect(screen.getByText('Content 2')).toBeInTheDocument();
  });
});
'''

    def generate_navigation_tests(self) -> str:
        """Generate Jest tests for the Navigation component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Navigation } from './Navigation';

const items = [
  { label: 'Home', href: '#' },
  { 
    label: 'Products', 
    children: [
      { label: 'Electronics', href: '#' },
      { label: 'Books', href: '#' }
    ] 
  }
];

describe('Navigation', () => {
  it('renders all top-level items', () => {
    render(<Navigation items={items} />);
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Products')).toBeInTheDocument();
  });

  it('expands submenu on click', () => {
    render(<Navigation items={items} />);
    
    // Submenu should be hidden initially (or just not rendered)
    expect(screen.queryByText('Electronics')).not.toBeInTheDocument();
    
    // Click parent
    fireEvent.click(screen.getByText('Products'));
    
    // Submenu should appear
    expect(screen.getByText('Electronics')).toBeInTheDocument();
  });

  it('calls onItemClick when item clicked', () => {
    const handleClick = jest.fn();
    render(<Navigation items={items} onItemClick={handleClick} />);
    
    fireEvent.click(screen.getByText('Home'));
    expect(handleClick).toHaveBeenCalled();
  });
});
'''

    def generate_breadcrumb_tests(self) -> str:
        """Generate Jest tests for the Breadcrumb component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Breadcrumb } from './Breadcrumb';

const items = [
  { label: 'Home', href: '/' },
  { label: 'Products', href: '/products' },
  { label: 'Shoes', active: true }
];

describe('Breadcrumb', () => {
  it('renders all items', () => {
    render(<Breadcrumb items={items} />);
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Products')).toBeInTheDocument();
    expect(screen.getByText('Shoes')).toBeInTheDocument();
  });

  it('renders separators', () => {
    render(<Breadcrumb items={items} />);
    const separators = screen.getAllByText('/');
    expect(separators.length).toBeGreaterThan(0);
  });

  it('active item is current page', () => {
    render(<Breadcrumb items={items} />);
    const activeItem = screen.getByText('Shoes');
    expect(activeItem).toHaveAttribute('aria-current', 'page');
  });
});
'''

    def generate_pagination_tests(self) -> str:
        """Generate Jest tests for the Pagination component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Pagination } from './Pagination';

describe('Pagination', () => {
  it('renders page numbers', () => {
    render(<Pagination currentPage={1} totalPages={5} onPageChange={() => {}} />);
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('5')).toBeInTheDocument();
  });

  it('calls onPageChange when number clicked', () => {
    const handleChange = jest.fn();
    render(<Pagination currentPage={1} totalPages={5} onPageChange={handleChange} />);
    
    fireEvent.click(screen.getByText('2'));
    expect(handleChange).toHaveBeenCalledWith(2);
  });

  it('disables prev button on first page', () => {
    render(<Pagination currentPage={1} totalPages={5} onPageChange={() => {}} />);
    expect(screen.getByText('Previous').closest('button')).toBeDisabled();
  });

  it('disables next button on last page', () => {
    render(<Pagination currentPage={5} totalPages={5} onPageChange={() => {}} />);
    expect(screen.getByText('Next').closest('button')).toBeDisabled();
  });
});
'''

    def generate_textarea_tests(self) -> str:
        """Generate Jest tests for the Textarea component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Textarea } from './Textarea';

describe('Textarea', () => {
  it('renders with placeholder', () => {
    render(<Textarea placeholder="Enter details" />);
    expect(screen.getByPlaceholderText(/enter details/i)).toBeInTheDocument();
  });

  it('updates value on change', async () => {
    const handleChange = jest.fn();
    const user = userEvent.setup();
    render(<Textarea onChange={handleChange} />);
    
    await user.type(screen.getByRole('textbox'), 'Hello');
    expect(handleChange).toHaveBeenCalledWith('Hello');
  });

  it('shows error state', () => {
    render(<Textarea error />);
    expect(screen.getByRole('textbox')).toHaveClass('border-error-300');
  });

  it('renders disabled state', () => {
    render(<Textarea disabled />);
    expect(screen.getByRole('textbox')).toBeDisabled();
  });
});
'''

    def generate_checkbox_tests(self) -> str:
        """Generate Jest tests for the Checkbox component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Checkbox } from './Checkbox';

describe('Checkbox', () => {
  it('renders key label', () => {
    render(<Checkbox label="Accept terms" />);
    expect(screen.getByLabelText(/accept terms/i)).toBeInTheDocument();
  });

  it('calls onChange when clicked', () => {
    const handleChange = jest.fn();
    render(<Checkbox label="Option" onChange={handleChange} />);
    
    fireEvent.click(screen.getByLabelText(/option/i));
    expect(handleChange).toHaveBeenCalledWith(true);
  });

  it('renders checked state', () => {
    render(<Checkbox label="Option" checked onChange={() => {}} />);
    expect(screen.getByLabelText(/option/i)).toBeChecked();
  });

  it('renders disabled state', () => {
    render(<Checkbox label="Option" disabled />);
    expect(screen.getByLabelText(/option/i)).toBeDisabled();
  });
});
'''

    def generate_radio_tests(self) -> str:
        """Generate Jest tests for the Radio component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Radio } from './Radio';

const options = [
  { value: '1', label: 'Option 1' },
  { value: '2', label: 'Option 2' },
];

describe('Radio', () => {
  it('renders all options', () => {
    render(<Radio name="test" options={options} />);
    expect(screen.getByLabelText('Option 1')).toBeInTheDocument();
    expect(screen.getByLabelText('Option 2')).toBeInTheDocument();
  });

  it('calls onChange with selected value', () => {
    const handleChange = jest.fn();
    render(<Radio name="test" options={options} onChange={handleChange} />);
    
    fireEvent.click(screen.getByLabelText('Option 2'));
    expect(handleChange).toHaveBeenCalledWith('2');
  });

  it('renders selected option as checked', () => {
    render(<Radio name="test" options={options} value="1" />);
    expect(screen.getByLabelText('Option 1')).toBeChecked();
    expect(screen.getByLabelText('Option 2')).not.toBeChecked();
  });
});
'''

    def generate_switch_tests(self) -> str:
        """Generate Jest tests for the Switch component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Switch } from './Switch';

describe('Switch', () => {
  it('renders correctly', () => {
    render(<Switch label="Toggle me" />);
    expect(screen.getByLabelText(/toggle me/i)).toBeInTheDocument();
  });

  it('toggles state on click', () => {
    const handleChange = jest.fn();
    render(<Switch label="Toggle" onChange={handleChange} />);
    
    fireEvent.click(screen.getByRole('switch'));
    expect(handleChange).toHaveBeenCalledWith(true);
  });

  it('renders checked state', () => {
    render(<Switch label="Toggle" checked onChange={() => {}} />);
    expect(screen.getByRole('switch')).toBeChecked();
  });

  it('renders disabled state', () => {
    render(<Switch label="Toggle" disabled />);
    expect(screen.getByRole('switch')).toBeDisabled();
  });
});
'''

    def generate_search_tests(self) -> str:
        """Generate Jest tests for the Search component."""
        return '''import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Search } from './Search';

describe('Search', () => {
  it('renders with placeholder', () => {
    render(<Search placeholder="Search users" />);
    expect(screen.getByPlaceholderText(/search users/i)).toBeInTheDocument();
  });

  it('calls onSearch after debounce/input', async () => {
    const handleSearch = jest.fn();
    const user = userEvent.setup();
    render(<Search onSearch={handleSearch} />);
    
    await user.type(screen.getByRole('searchbox'), 'test');
    
    // Assuming debounce or immediate effect
    await waitFor(() => {
      expect(handleSearch).toHaveBeenCalledWith('test');
    }, { timeout: 1000 });
  });

  it('renders loading state', () => {
    render(<Search loading />);
    // Look for spinner or loading indicator
    expect(screen.getByRole('status')).toBeInTheDocument(); 
  });
});
'''

    def generate_datepicker_tests(self) -> str:
        """Generate Jest tests for the DatePicker component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { DatePicker } from './DatePicker';

describe('DatePicker', () => {
  it('renders input field', () => {
    render(<DatePicker placeholder="Select date" />);
    expect(screen.getByPlaceholderText(/select date/i)).toBeInTheDocument();
  });

  it('opens calendar on click', () => {
    render(<DatePicker />);
    fireEvent.click(screen.getByRole('textbox'));
    // Check for calendar elements (e.g., days of week)
    expect(screen.getByText('Su')).toBeInTheDocument();
    expect(screen.getByText('Mo')).toBeInTheDocument();
  });

  it('selects a date', () => {
    const handleChange = jest.fn();
    render(<DatePicker onChange={handleChange} />);
    
    fireEvent.click(screen.getByRole('textbox'));
    
    // Click a day (e.g., 15th)
    // Note: This relies on "15" being present in the current month view
    const dayButton = screen.getAllByText('15').find(el => !el.classList.contains('text-neutral-400'));
    if (dayButton) fireEvent.click(dayButton);
    
    expect(handleChange).toHaveBeenCalled();
  });
});
'''

    def generate_tooltip_tests(self) -> str:
        """Generate Jest tests for the Tooltip component."""
        return '''import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Tooltip } from './Tooltip';

describe('Tooltip', () => {
  it('renders children', () => {
    render(<Tooltip content="Help text"><button>Hover me</button></Tooltip>);
    expect(screen.getByText('Hover me')).toBeInTheDocument();
  });

  it('shows tooltip on hover', async () => {
    render(<Tooltip content="Help text"><button>Hover me</button></Tooltip>);
    
    expect(screen.queryByRole('tooltip')).not.toBeInTheDocument();
    
    fireEvent.mouseEnter(screen.getByText('Hover me'));
    expect(screen.getByRole('tooltip')).toBeInTheDocument();
    expect(screen.getByText('Help text')).toBeInTheDocument();
  });

  it('hides tooltip on mouse leave', async () => {
    render(<Tooltip content="Help text"><button>Hover me</button></Tooltip>);
    
    fireEvent.mouseEnter(screen.getByText('Hover me'));
    expect(screen.getByRole('tooltip')).toBeInTheDocument();
    
    fireEvent.mouseLeave(screen.getByText('Hover me'));
    expect(screen.queryByRole('tooltip')).not.toBeInTheDocument();
  });
});
'''

    def generate_avatar_tests(self) -> str:
        """Generate Jest tests for the Avatar component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Avatar } from './Avatar';

describe('Avatar', () => {
  it('renders initials when no src provided', () => {
    render(<Avatar name="John Doe" />);
    expect(screen.getByText('JD')).toBeInTheDocument();
  });

  it('renders image when src provided', () => {
    render(<Avatar name="John Doe" src="https://example.com/avatar.jpg" />);
    expect(screen.getByRole('img')).toHaveAttribute('src', 'https://example.com/avatar.jpg');
  });

  it('renders status indicator', () => {
    render(<Avatar name="John Doe" status="online" showStatus />);
    // Status indicator usually has a specific class or aria-label
    const status = screen.getByRole('presentation', { hidden: true }); // Depending on implementation
    expect(status).toHaveClass('bg-success-500'); // Assuming success color for online
  });
});
'''

    def generate_progress_tests(self) -> str:
        """Generate Jest tests for the Progress component."""
        return '''import React from 'react';
import { render, screen } from '@testing-library/react';
import { Progress } from './Progress';

describe('Progress', () => {
  it('renders correctly', () => {
    render(<Progress value={50} />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('shows correct percentage width', () => {
    const { container } = render(<Progress value={75} />);
    const progressBar = container.querySelector('.bg-primary-600');
    expect(progressBar).toHaveStyle('width: 75%');
  });

  it('displays label if requested', () => {
    render(<Progress value={50} showLabel />);
    expect(screen.getByText('50%')).toBeInTheDocument();
  });
});
'''

    def generate_skeleton_tests(self) -> str:
        """Generate Jest tests for the Skeleton component."""
        return '''import React from 'react';
import { render } from '@testing-library/react';
import { Skeleton } from './Skeleton';

describe('Skeleton', () => {
  it('renders correctly', () => {
    const { container } = render(<Skeleton />);
    expect(container.firstChild).toHaveClass('animate-pulse');
  });

  it('applies circles variant', () => {
    const { container } = render(<Skeleton variant="circle" />);
    expect(container.firstChild).toHaveClass('rounded-full');
  });

  it('applies custom dimensions', () => {
    const { container } = render(<Skeleton width={100} height={50} />);
    expect(container.firstChild).toHaveStyle('width: 100px');
    expect(container.firstChild).toHaveStyle('height: 50px');
  });
});
'''

    def generate_accordion_tests(self) -> str:
        """Generate Jest tests for the Accordion component."""
        return '''import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Accordion } from './Accordion';

const items = [
  { id: '1', title: 'Item 1', content: 'Content 1' },
  { id: '2', title: 'Item 2', content: 'Content 2' },
];

describe('Accordion', () => {
  it('renders all titles', () => {
    render(<Accordion items={items} />);
    expect(screen.getByText('Item 1')).toBeInTheDocument();
    expect(screen.getByText('Item 2')).toBeInTheDocument();
  });

  it('expands item on click', () => {
    render(<Accordion items={items} />);
    
    // Content hidden initially
    expect(screen.queryByText('Content 1')).not.toBeVisible();
    
    fireEvent.click(screen.getByText('Item 1'));
    
    // Content visible
    expect(screen.getByText('Content 1')).toBeVisible();
  });

  it('allows multiple items expanded if configured', () => {
    render(<Accordion items={items} allowMultiple />);
    
    fireEvent.click(screen.getByText('Item 1'));
    fireEvent.click(screen.getByText('Item 2'));
    
    expect(screen.getByText('Content 1')).toBeVisible();
    expect(screen.getByText('Content 2')).toBeVisible();
  });
});
'''

    def generate_card_stories(self) -> str:
        """Generate Storybook stories for the Card component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Card } from './Card';

const meta: Meta<typeof Card> = {
  title: 'Components/Card',
  component: Card,
  parameters: {
    layout: 'centered',
  },
};

export default meta;
type Story = StoryObj<typeof Card>;

export const Default: Story = {
  args: {
    children: 'This is a basic card component that can contain any content.',
  },
};

export const WithTitle: Story = {
  args: {
    title: 'Card Title',
    children: 'Card components are used to group related content and actions.',
  },
};

export const Elevated: Story = {
  args: {
    variant: 'elevated',
    children: 'Elevated cards use shadows to create depth and emphasis.',
  },
};
'''

    def generate_sidebar_stories(self) -> str:
        """Generate Storybook stories for the Sidebar component."""
        return '''import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { Sidebar } from './Sidebar';

const meta: Meta<typeof Sidebar> = {
  title: 'Layout/Sidebar',
  component: Sidebar,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Sidebar>;

export const Default: Story = {
  args: {
    items: [
      { label: 'Dashboard', href: '#', active: true },
      { label: 'Analytics', href: '#' },
      { label: 'Customers', href: '#' },
      { label: 'Settings', href: '#' },
    ],
  },
};
'''

    def generate_header_stories(self) -> str:
        """Generate Storybook stories for the Header component."""
        return '''import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { Header } from './Header';

const meta: Meta<typeof Header> = {
  title: 'Layout/Header',
  component: Header,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Header>;

export const Default: Story = {
  args: {
    links: [
      { label: 'Product', href: '#' },
      { label: 'Solutions', href: '#' },
      { label: 'Resources', href: '#' },
      { label: 'Pricing', href: '#' },
    ],
    brandName: 'DesignSystem',
  },
};
'''

    def generate_footer_stories(self) -> str:
        """Generate Storybook stories for the Footer component."""
        return '''import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { Footer } from './Footer';

const meta: Meta<typeof Footer> = {
  title: 'Layout/Footer',
  component: Footer,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Footer>;

export const Default: Story = {
  args: {
    columns: [
      {
        title: 'Product',
        links: [
          { label: 'Features', href: '#' },
          { label: 'Integrations', href: '#' },
          { label: 'Pricing', href: '#' },
        ],
      },
      {
        title: 'Company',
        links: [
          { label: 'About', href: '#' },
          { label: 'Careers', href: '#' },
          { label: 'Contact', href: '#' },
        ],
      },
    ],
  },
};
'''

    def generate_hero_stories(self) -> str:
        """Generate Storybook stories for the Hero component."""
        return '''import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { Hero } from './Hero';

const meta: Meta<typeof Hero> = {
  title: 'Layout/Hero',
  component: Hero,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Hero>;

export const Default: Story = {
  args: {
    title: 'Design your future with us',
    subtitle: 'The best design system generator for modern developers. Build faster, stay consistent.',
    primaryAction: { label: 'Get Started', onClick: () => alert('Clicked') },
    secondaryAction: { label: 'Learn More', onClick: () => {} },
  },
};
'''

    def generate_container_stories(self) -> str:
        """Generate Storybook stories for the Container component."""
        return '''import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { Container } from './Container';

const meta: Meta<typeof Container> = {
  title: 'Layout/Container',
  component: Container,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Container>;

export const Default: Story = {
  args: {
    children: <div className="bg-primary-100 p-4 border border-primary-300">Container Content</div>,
  },
};

export const Small: Story = {
  args: {
    size: 'sm',
    children: <div className="bg-primary-100 p-4 border border-primary-300">Small Container</div>,
  },
};
'''

    def generate_stack_stories(self) -> str:
        """Generate Storybook stories for the Stack component."""
        return '''import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { Stack } from './Stack';

const meta: Meta<typeof Stack> = {
  title: 'Layout/Stack',
  component: Stack,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Stack>;

export const Vertical: Story = {
  args: {
    direction: 'col',
    spacing: 4,
    children: [
      <div key="1" className="bg-neutral-100 p-4">Item 1</div>,
      <div key="2" className="bg-neutral-100 p-4">Item 2</div>,
      <div key="3" className="bg-neutral-100 p-4">Item 3</div>,
    ],
  },
};

export const Horizontal: Story = {
  args: {
    direction: 'row',
    spacing: 4,
    children: [
      <div key="1" className="bg-neutral-100 p-4">Item 1</div>,
      <div key="2" className="bg-neutral-100 p-4">Item 2</div>,
      <div key="3" className="bg-neutral-100 p-4">Item 3</div>,
    ],
  },
};
'''

    def generate_grid_stories(self) -> str:
        """Generate Storybook stories for the Grid component."""
        return '''import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import { Grid } from './Grid';

const meta: Meta<typeof Grid> = {
  title: 'Layout/Grid',
  component: Grid,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Grid>;

export const ThreeColumns: Story = {
  args: {
    cols: 3,
    gap: 4,
    children: [
      <div key="1" className="bg-neutral-100 p-8 text-center">1</div>,
      <div key="2" className="bg-neutral-100 p-8 text-center">2</div>,
      <div key="3" className="bg-neutral-100 p-8 text-center">3</div>,
      <div key="4" className="bg-neutral-100 p-8 text-center">4</div>,
      <div key="5" className="bg-neutral-100 p-8 text-center">5</div>,
      <div key="6" className="bg-neutral-100 p-8 text-center">6</div>,
    ],
  },
};

export const Responsive: Story = {
  args: {
    cols: { sm: 1, md: 2, lg: 3 },
    gap: 4,
    children: [
      <div key="1" className="bg-neutral-100 p-8 text-center">1</div>,
      <div key="2" className="bg-neutral-100 p-8 text-center">2</div>,
      <div key="3" className="bg-neutral-100 p-8 text-center">3</div>,
    ],
  },
};
'''

    def generate_button_stories(self) -> str:
        """Generate Storybook stories for the Button component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A versatile button component with multiple variants and states.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'tertiary', 'danger'],
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg'],
    },
    disabled: {
      control: 'boolean',
    },
    loading: {
      control: 'boolean',
    },
    onClick: { action: 'clicked' },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button',
  },
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
};

export const Tertiary: Story = {
  args: {
    variant: 'tertiary',
    children: 'Tertiary Button',
  },
};

export const Danger: Story = {
  args: {
    variant: 'danger',
    children: 'Danger Button',
  },
};

export const Small: Story = {
  args: {
    size: 'sm',
    children: 'Small Button',
  },
};

export const Medium: Story = {
  args: {
    size: 'md',
    children: 'Medium Button',
  },
};

export const Large: Story = {
  args: {
    size: 'lg',
    children: 'Large Button',
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled Button',
  },
};

export const Loading: Story = {
  args: {
    loading: true,
    children: 'Loading Button',
  },
};

export const WithIcons: Story = {
  args: {
    children: 'Button with Icon',
  },
  render: (args) => (
    <Button {...args}>
      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
      {args.children}
    </Button>
  ),
};
'''

    def generate_input_stories(self) -> str:
        """Generate Storybook stories for the Input component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Input } from './Input';

const meta: Meta<typeof Input> = {
  title: 'Components/Input',
  component: Input,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A flexible input component supporting various input types and validation states.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    type: {
      control: { type: 'select' },
      options: ['text', 'email', 'password', 'search', 'number'],
    },
    placeholder: {
      control: 'text',
    },
    value: {
      control: 'text',
    },
    error: {
      control: 'boolean',
    },
    disabled: {
      control: 'boolean',
    },
    required: {
      control: 'boolean',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Text: Story = {
  args: {
    type: 'text',
    placeholder: 'Enter text...',
  },
};

export const Email: Story = {
  args: {
    type: 'email',
    placeholder: 'Enter email address...',
  },
};

export const Password: Story = {
  args: {
    type: 'password',
    placeholder: 'Enter password...',
  },
};

export const Search: Story = {
  args: {
    type: 'search',
    placeholder: 'Search...',
  },
};

export const Number: Story = {
  args: {
    type: 'number',
    placeholder: 'Enter number...',
  },
};

export const WithValue: Story = {
  args: {
    value: 'Pre-filled value',
    placeholder: 'Enter text...',
  },
};

export const Error: Story = {
  args: {
    placeholder: 'Enter text...',
    error: true,
  },
};

export const Disabled: Story = {
  args: {
    placeholder: 'Disabled input...',
    disabled: true,
  },
};

export const Required: Story = {
  args: {
    placeholder: 'Required field...',
    required: true,
  },
};
'''

    def generate_modal_stories(self) -> str:
        """Generate Storybook stories for the Modal component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { useState } from 'react';
import { Modal } from './Modal';
import { Button } from './Button';

const meta: Meta<typeof Modal> = {
  title: 'Components/Modal',
  component: Modal,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'A modal dialog component with proper focus management and accessibility features.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg', 'xl'],
    },
    closeOnOverlayClick: {
      control: 'boolean',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const ModalWithControls = (args: any) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setIsOpen(true)}>Open Modal</Button>
      <Modal {...args} isOpen={isOpen} onClose={() => setIsOpen(false)}>
        <div className="space-y-4">
          <p className="text-sm text-neutral-600">
            This is the modal content. You can put any content here.
          </p>
          <div className="flex space-x-3 justify-end">
            <Button variant="secondary" onClick={() => setIsOpen(false)}>
              Cancel
            </Button>
            <Button onClick={() => setIsOpen(false)}>
              Confirm
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
};

export const Default: Story = {
  render: (args) => <ModalWithControls {...args} />,
  args: {
    title: 'Modal Title',
    size: 'md',
  },
};

export const Small: Story = {
  render: (args) => <ModalWithControls {...args} />,
  args: {
    title: 'Small Modal',
    size: 'sm',
  },
};

export const Large: Story = {
  render: (args) => <ModalWithControls {...args} />,
  args: {
    title: 'Large Modal',
    size: 'lg',
  },
};

export const ExtraLarge: Story = {
  render: (args) => <ModalWithControls {...args} />,
  args: {
    title: 'Extra Large Modal',
    size: 'xl',
  },
};

export const WithoutTitle: Story = {
  render: (args) => <ModalWithControls {...args} />,
  args: {
    size: 'md',
  },
};

export const NoOverlayClick: Story = {
  render: (args) => <ModalWithControls {...args} />,
  args: {
    title: 'Modal with Overlay Protection',
    size: 'md',
    closeOnOverlayClick: false,
  },
};
'''

    def generate_alert_stories(self) -> str:
        """Generate Storybook stories for the Alert component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { useState } from 'react';
import { Alert } from './Alert';

const meta: Meta<typeof Alert> = {
  title: 'Components/Alert',
  component: Alert,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'An alert component for displaying important messages and notifications.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['success', 'warning', 'error', 'info'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Success: Story = {
  args: {
    variant: 'success',
    title: 'Success!',
    children: 'Your changes have been saved successfully.',
  },
};

export const Warning: Story = {
  args: {
    variant: 'warning',
    title: 'Warning',
    children: 'Please review your input before proceeding.',
  },
};

export const Error: Story = {
  args: {
    variant: 'error',
    title: 'Error',
    children: 'Something went wrong. Please try again.',
  },
};

export const Info: Story = {
  args: {
    variant: 'info',
    title: 'Information',
    children: 'Here is some important information you should know.',
  },
};

export const WithoutTitle: Story = {
  args: {
    variant: 'info',
    children: 'This alert has no title, just content.',
  },
};

const DismissibleAlert = (args: any) => {
  const [visible, setVisible] = useState(true);

  if (!visible) return null;

  return (
    <Alert {...args} onDismiss={() => setVisible(false)}>
      {args.children}
    </Alert>
  );
};

export const Dismissible: Story = {
  render: (args) => <DismissibleAlert {...args} />,
  args: {
    variant: 'info',
    title: 'Dismissible Alert',
    children: 'Click the X to dismiss this alert.',
  },
};
'''

    def generate_select_stories(self) -> str:
        """Generate Storybook stories for the Select component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Select } from './Select';

const meta: Meta<typeof Select> = {
  title: 'Components/Select',
  component: Select,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A select dropdown component with keyboard navigation and accessibility support.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    placeholder: {
      control: 'text',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const sampleOptions = [
  { value: 'option1', label: 'Option 1' },
  { value: 'option2', label: 'Option 2' },
  { value: 'option3', label: 'Option 3' },
  { value: 'option4', label: 'Option 4' },
];

export const Default: Story = {
  args: {
    options: sampleOptions,
    placeholder: 'Select an option',
  },
};

export const WithValue: Story = {
  args: {
    options: sampleOptions,
    value: 'option2',
    placeholder: 'Select an option',
  },
};

export const Disabled: Story = {
  args: {
    options: sampleOptions,
    placeholder: 'Disabled select',
    disabled: true,
  },
};

export const WithError: Story = {
  args: {
    options: sampleOptions,
    placeholder: 'Select with error',
    error: true,
  },
};

export const Required: Story = {
  args: {
    options: sampleOptions,
    placeholder: 'Required field',
    required: true,
  },
};
'''

    def generate_table_stories(self) -> str:
        """Generate Storybook stories for the Table component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Table } from './Table';

const meta: Meta<typeof Table> = {
  title: 'Components/Table',
  component: Table,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'A flexible data table component with sorting, selection, and responsive features.',
      },
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  status: string;
}

const sampleData: User[] = [
  { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin', status: 'Active' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'User', status: 'Active' },
  { id: 3, name: 'Bob Johnson', email: 'bob@example.com', role: 'User', status: 'Inactive' },
  { id: 4, name: 'Alice Brown', email: 'alice@example.com', role: 'Moderator', status: 'Active' },
];

const columns = [
  { key: 'name' as keyof User, header: 'Name' },
  { key: 'email' as keyof User, header: 'Email' },
  { key: 'role' as keyof User, header: 'Role' },
  {
    key: 'status' as keyof User,
    header: 'Status',
    render: (value: string) => (
      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
        value === 'Active'
          ? 'bg-green-100 text-green-800'
          : 'bg-red-100 text-red-800'
      }`}>
        {value}
      </span>
    )
  },
];

export const Default: Story = {
  args: {
    data: sampleData,
    columns: columns,
  },
};

export const Selectable: Story = {
  args: {
    data: sampleData,
    columns: columns,
    selectable: true,
  },
};

export const Loading: Story = {
  args: {
    data: [],
    columns: columns,
    loading: true,
  },
};

export const Empty: Story = {
  args: {
    data: [],
    columns: columns,
    emptyMessage: 'No users found',
  },
};

export const WithSelection: Story = {
  args: {
    data: sampleData,
    columns: columns,
    selectable: true,
    selectedRows: [sampleData[1]],
  },
};
'''

    def generate_navigation_stories(self) -> str:
        """Generate Storybook stories for the Navigation component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Navigation } from './Navigation';

const meta: Meta<typeof Navigation> = {
  title: 'Components/Navigation',
  component: Navigation,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'A flexible navigation component supporting horizontal and vertical layouts with nested menus.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['horizontal', 'vertical'],
    },
    collapsible: {
      control: 'boolean',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const sampleItems = [
  { label: 'Home', href: '/' },
  {
    label: 'Products',
    children: [
      { label: 'Web App', href: '/products/web' },
      { label: 'Mobile App', href: '/products/mobile' },
      { label: 'API', href: '/products/api' },
    ]
  },
  { label: 'About', href: '/about' },
  {
    label: 'Resources',
    children: [
      { label: 'Documentation', href: '/docs' },
      { label: 'Blog', href: '/blog' },
      { label: 'Support', href: '/support' },
    ]
  },
  { label: 'Contact', href: '/contact' },
];

export const Horizontal: Story = {
  args: {
    items: sampleItems,
    variant: 'horizontal',
  },
};

export const Vertical: Story = {
  args: {
    items: sampleItems,
    variant: 'vertical',
  },
};

export const CollapsibleVertical: Story = {
  args: {
    items: sampleItems,
    variant: 'vertical',
    collapsible: true,
  },
};

export const WithActiveItem: Story = {
  args: {
    items: sampleItems,
    variant: 'horizontal',
    activeItem: 'About',
  },
};
'''

    def generate_textarea_stories(self) -> str:
        """Generate Storybook stories for the Textarea component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Textarea } from './Textarea';

const meta: Meta<typeof Textarea> = {
  title: 'Components/Textarea',
  component: Textarea,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A multi-line text input component with character counting and resize options.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    rows: {
      control: { type: 'number', min: 1, max: 10 },
    },
    maxLength: {
      control: 'number',
    },
    resize: {
      control: { type: 'select' },
      options: ['none', 'vertical', 'horizontal', 'both'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    placeholder: 'Enter your message...',
    rows: 4,
  },
};

export const WithValue: Story = {
  args: {
    value: 'This is some pre-filled content in the textarea.',
    placeholder: 'Enter your message...',
  },
};

export const WithMaxLength: Story = {
  args: {
    placeholder: 'Enter a short message...',
    maxLength: 100,
  },
};

export const NoResize: Story = {
  args: {
    placeholder: 'This textarea cannot be resized',
    resize: 'none',
    rows: 3,
  },
};

export const Error: Story = {
  args: {
    placeholder: 'Enter your message...',
    error: true,
  },
};

export const Disabled: Story = {
  args: {
    placeholder: 'This textarea is disabled',
    disabled: true,
    value: 'Disabled content',
  },
};
'''

    def generate_checkbox_stories(self) -> str:
        """Generate Storybook stories for the Checkbox component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Checkbox } from './Checkbox';

const meta: Meta<typeof Checkbox> = {
  title: 'Components/Checkbox',
  component: Checkbox,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A checkbox component for boolean selections with support for indeterminate state.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    label: 'Accept terms and conditions',
  },
};

export const Checked: Story = {
  args: {
    label: 'I agree to the terms',
    checked: true,
  },
};

export const Indeterminate: Story = {
  args: {
    label: 'Select all items',
    indeterminate: true,
  },
};

export const Small: Story = {
  args: {
    label: 'Small checkbox',
    size: 'sm',
  },
};

export const Large: Story = {
  args: {
    label: 'Large checkbox',
    size: 'lg',
  },
};

export const Disabled: Story = {
  args: {
    label: 'Disabled checkbox',
    disabled: true,
  },
};

export const DisabledChecked: Story = {
  args: {
    label: 'Disabled and checked',
    disabled: true,
    checked: true,
  },
};
'''

    def generate_radio_stories(self) -> str:
        """Generate Storybook stories for the Radio component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Radio } from './Radio';

const meta: Meta<typeof Radio> = {
  title: 'Components/Radio',
  component: Radio,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A radio button group component for single selections from multiple options.',
      },
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

const sampleOptions = [
  { value: 'option1', label: 'Option 1' },
  { value: 'option2', label: 'Option 2' },
  { value: 'option3', label: 'Option 3' },
];

export const Default: Story = {
  args: {
    options: sampleOptions,
  },
};

export const Preselected: Story = {
  args: {
    options: sampleOptions,
    value: 'option2',
  },
};

export const Vertical: Story = {
  args: {
    options: sampleOptions,
    orientation: 'vertical',
  },
};

export const Horizontal: Story = {
  args: {
    options: [
      { value: 'small', label: 'Small' },
      { value: 'medium', label: 'Medium' },
      { value: 'large', label: 'Large' },
    ],
    orientation: 'horizontal',
  },
};

export const WithDisabled: Story = {
  args: {
    options: [
      { value: 'enabled1', label: 'Enabled Option 1' },
      { value: 'disabled', label: 'Disabled Option', disabled: true },
      { value: 'enabled2', label: 'Enabled Option 2' },
    ],
  },
};
'''

    def generate_badge_stories(self) -> str:
        """Generate Storybook stories for the Badge component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Badge } from './Badge';

const meta: Meta<typeof Badge> = {
  title: 'Components/Badge',
  component: Badge,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A badge component for displaying status, labels, and counts.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'success', 'warning', 'error', 'info'],
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    children: 'Primary',
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    children: 'Secondary',
    variant: 'secondary',
  },
};

export const Success: Story = {
  args: {
    children: 'Success',
    variant: 'success',
  },
};

export const Warning: Story = {
  args: {
    children: 'Warning',
    variant: 'warning',
  },
};

export const Error: Story = {
  args: {
    children: 'Error',
    variant: 'error',
  },
};

export const Info: Story = {
  args: {
    children: 'Info',
    variant: 'info',
  },
};

export const Small: Story = {
  args: {
    children: 'Small',
    size: 'sm',
  },
};

export const Large: Story = {
  args: {
    children: 'Large',
    size: 'lg',
  },
};

export const Rounded: Story = {
  args: {
    children: 'New',
    variant: 'success',
    rounded: true,
  },
};

export const Dot: Story = {
  args: {
    children: 'Online',
    variant: 'success',
    dot: true,
  },
};
'''

    def generate_tooltip_stories(self) -> str:
        """Generate Storybook stories for the Tooltip component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Tooltip } from './Tooltip';
import { Button } from './Button';

const meta: Meta<typeof Tooltip> = {
  title: 'Components/Tooltip',
  component: Tooltip,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A tooltip component for displaying contextual help and information.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    position: {
      control: { type: 'select' },
      options: ['top', 'bottom', 'left', 'right'],
    },
    delay: {
      control: 'number',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Top: Story = {
  args: {
    content: 'This is a tooltip positioned at the top',
    children: <Button>Hover me (Top)</Button>,
    position: 'top',
  },
};

export const Bottom: Story = {
  args: {
    content: 'This is a tooltip positioned at the bottom',
    children: <Button>Hover me (Bottom)</Button>,
    position: 'bottom',
  },
};

export const Left: Story = {
  args: {
    content: 'This is a tooltip positioned to the left',
    children: <Button>Hover me (Left)</Button>,
    position: 'left',
  },
};

export const Right: Story = {
  args: {
    content: 'This is a tooltip positioned to the right',
    children: <Button>Hover me (Right)</Button>,
    position: 'right',
  },
};

export const LongContent: Story = {
  args: {
    content: 'This is a longer tooltip with more detailed information that might wrap to multiple lines if needed.',
    children: <Button>Hover for long tooltip</Button>,
  },
};

export const NoDelay: Story = {
  args: {
    content: 'This tooltip appears immediately',
    children: <Button>Instant tooltip</Button>,
    delay: 0,
  },
};

export const WithText: Story = {
  args: {
    content: 'Helpful information about this text',
    children: <span className="underline cursor-help">Hover this text</span>,
  },
};
'''

    def generate_tabs_stories(self) -> str:
        """Generate Storybook stories for the Tabs component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Tabs } from './Tabs';

const meta: Meta<typeof Tabs> = {
  title: 'Components/Tabs',
  component: Tabs,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'A tabs component for organizing content into separate panels.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['underline', 'pills', 'buttons'],
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const sampleTabs = [
  {
    id: 'tab1',
    label: 'Profile',
    content: (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Profile Settings</h3>
        <p className="text-neutral-600">Manage your profile information and preferences.</p>
        <div className="bg-neutral-50 p-4 rounded-md">
          <p className="text-sm text-neutral-700">Profile content goes here...</p>
        </div>
      </div>
    ),
  },
  {
    id: 'tab2',
    label: 'Security',
    content: (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Security Settings</h3>
        <p className="text-neutral-600">Configure your account security and privacy settings.</p>
        <div className="bg-neutral-50 p-4 rounded-md">
          <p className="text-sm text-neutral-700">Security settings go here...</p>
        </div>
      </div>
    ),
  },
  {
    id: 'tab3',
    label: 'Notifications',
    content: (
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Notification Preferences</h3>
        <p className="text-neutral-600">Choose how you want to be notified about updates.</p>
        <div className="bg-neutral-50 p-4 rounded-md">
          <p className="text-sm text-neutral-700">Notification settings go here...</p>
        </div>
      </div>
    ),
  },
];

export const Underline: Story = {
  args: {
    tabs: sampleTabs,
    variant: 'underline',
  },
};

export const Pills: Story = {
  args: {
    tabs: sampleTabs,
    variant: 'pills',
  },
};

export const Buttons: Story = {
  args: {
    tabs: sampleTabs,
    variant: 'buttons',
  },
};

export const Small: Story = {
  args: {
    tabs: sampleTabs,
    size: 'sm',
  },
};

export const Large: Story = {
  args: {
    tabs: sampleTabs,
    size: 'lg',
  },
};

export const Preselected: Story = {
  args: {
    tabs: sampleTabs,
    defaultTab: 'tab2',
  },
};
'''

    def generate_avatar_stories(self) -> str:
        """Generate Storybook stories for the Avatar component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Avatar } from './Avatar';

const meta: Meta<typeof Avatar> = {
  title: 'Components/Avatar',
  component: Avatar,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'An avatar component for displaying user images, initials, or icons.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    size: {
      control: { type: 'select' },
      options: ['xs', 'sm', 'md', 'lg', 'xl', '2xl'],
    },
    variant: {
      control: { type: 'select' },
      options: ['circle', 'square', 'rounded'],
    },
    status: {
      control: { type: 'select' },
      options: ['online', 'offline', 'away', 'busy'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const WithImage: Story = {
  args: {
    src: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face',
    alt: 'User avatar',
    size: 'md',
  },
};

export const WithInitials: Story = {
  args: {
    name: 'John Doe',
    size: 'md',
  },
};

export const WithStatus: Story = {
  args: {
    src: 'https://images.unsplash.com/photo-1494790108755-2616b612b47c?w=100&h=100&fit=crop&crop=face',
    alt: 'User with status',
    size: 'lg',
    status: 'online',
    showStatus: true,
  },
};

export const Square: Story = {
  args: {
    name: 'Jane Smith',
    variant: 'square',
    size: 'md',
  },
};

export const Rounded: Story = {
  args: {
    name: 'Bob Johnson',
    variant: 'rounded',
    size: 'md',
  },
};

export const ExtraSmall: Story = {
  args: {
    name: 'XS',
    size: 'xs',
  },
};

export const ExtraLarge: Story = {
  args: {
    name: 'XL Avatar',
    size: '2xl',
  },
};

export const FallbackIcon: Story = {
  args: {
    size: 'md',
  },
};

export const BusyStatus: Story = {
  args: {
    name: 'Busy User',
    status: 'busy',
    showStatus: true,
    size: 'md',
  },
};

export const AwayStatus: Story = {
  args: {
    name: 'Away User',
    status: 'away',
    showStatus: true,
    size: 'md',
  },
};
'''



    def generate_storybook_vite_config(self) -> str:
        """Generate Vite configuration for Storybook."""
        return '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    postcss: './postcss.config.js',
  },
})'''

    def generate_storybook_postcss_config(self) -> str:
        """Generate PostCSS configuration for Storybook."""
        return '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}'''

    def generate_button_story(self, spec: ComponentSpec) -> str:
        """Generate Storybook story for Button component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';
import { fn } from '@storybook/test';

const meta = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A versatile button component with multiple variants and states.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'tertiary', 'danger'],
      description: 'The visual style variant of the button',
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg'],
      description: 'The size of the button',
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the button is disabled',
    },
    loading: {
      control: 'boolean',
      description: 'Whether the button shows a loading state',
    },
    children: {
      control: 'text',
      description: 'The button content',
    },
  },
  args: {
    onClick: fn(),
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button',
  },
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
};

export const Tertiary: Story = {
  args: {
    variant: 'tertiary',
    children: 'Tertiary Button',
  },
};

export const Danger: Story = {
  args: {
    variant: 'danger',
    children: 'Danger Button',
  },
};

export const Small: Story = {
  args: {
    size: 'sm',
    children: 'Small Button',
  },
};

export const Medium: Story = {
  args: {
    size: 'md',
    children: 'Medium Button',
  },
};

export const Large: Story = {
  args: {
    size: 'lg',
    children: 'Large Button',
  },
};

export const Loading: Story = {
  args: {
    loading: true,
    children: 'Loading...',
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled Button',
  },
};

export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-col gap-4">
      <div className="flex gap-2">
        <Button variant="primary">Primary</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="tertiary">Tertiary</Button>
        <Button variant="danger">Danger</Button>
      </div>
      <div className="flex gap-2 items-center">
        <Button size="sm">Small</Button>
        <Button size="md">Medium</Button>
        <Button size="lg">Large</Button>
      </div>
      <div className="flex gap-2">
        <Button loading>Loading</Button>
        <Button disabled>Disabled</Button>
      </div>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'All button variants, sizes, and states displayed together.',
      },
    },
  },
};'''

    def generate_input_story(self, spec: ComponentSpec) -> str:
        """Generate Storybook story for Input component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Input } from './Input';

const meta = {
  title: 'Components/Input',
  component: Input,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A flexible input component with validation states and multiple types.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    type: {
      control: { type: 'select' },
      options: ['text', 'email', 'password', 'search', 'number'],
      description: 'The input type',
    },
    placeholder: {
      control: 'text',
      description: 'Placeholder text',
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the input is disabled',
    },
    required: {
      control: 'boolean',
      description: 'Whether the input is required',
    },
    error: {
      control: 'boolean',
      description: 'Whether to show error state',
    },
  },
} satisfies Meta<typeof Input>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Text: Story = {
  args: {
    type: 'text',
    placeholder: 'Enter text...',
  },
};

export const Email: Story = {
  args: {
    type: 'email',
    placeholder: 'Enter email...',
  },
};

export const Password: Story = {
  args: {
    type: 'password',
    placeholder: 'Enter password...',
  },
};

export const Search: Story = {
  args: {
    type: 'search',
    placeholder: 'Search...',
  },
};

export const Number: Story = {
  args: {
    type: 'number',
    placeholder: 'Enter number...',
  },
};

export const WithValue: Story = {
  args: {
    type: 'text',
    placeholder: 'Enter text...',
    value: 'Pre-filled value',
  },
};

export const Error: Story = {
  args: {
    type: 'email',
    placeholder: 'Enter valid email...',
    error: true,
  },
};

export const Disabled: Story = {
  args: {
    type: 'text',
    placeholder: 'Disabled input...',
    disabled: true,
  },
};

export const Required: Story = {
  args: {
    type: 'text',
    placeholder: 'Required field...',
    required: true,
  },
};'''

    def generate_select_story(self, spec: ComponentSpec) -> str:
        """Generate Storybook story for Select component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Select } from './Select';

const meta = {
  title: 'Components/Select',
  component: Select,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A dropdown select component with keyboard navigation and accessibility support.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    placeholder: {
      control: 'text',
      description: 'Placeholder text when no option is selected',
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the select is disabled',
    },
    required: {
      control: 'boolean',
      description: 'Whether the select is required',
    },
    error: {
      control: 'boolean',
      description: 'Whether to show error state',
    },
  },
} satisfies Meta<typeof Select>;

export default meta;
type Story = StoryObj<typeof meta>;

const sampleOptions = [
  { value: 'option1', label: 'Option 1' },
  { value: 'option2', label: 'Option 2' },
  { value: 'option3', label: 'Option 3' },
  { value: 'option4', label: 'Option 4' },
  { value: 'option5', label: 'Option 5' },
];

export const Default: Story = {
  args: {
    options: sampleOptions,
    placeholder: 'Select an option',
  },
};

export const WithSelectedValue: Story = {
  args: {
    options: sampleOptions,
    value: 'option2',
    placeholder: 'Select an option',
  },
};

export const Error: Story = {
  args: {
    options: sampleOptions,
    placeholder: 'Select an option',
    error: true,
  },
};

export const Disabled: Story = {
  args: {
    options: sampleOptions,
    placeholder: 'Select an option',
    disabled: true,
  },
};

export const Required: Story = {
  args: {
    options: sampleOptions,
    placeholder: 'Required selection',
    required: true,
  },
};

export const ManyOptions: Story = {
  args: {
    options: [
      { value: 'us', label: 'United States' },
      { value: 'ca', label: 'Canada' },
      { value: 'uk', label: 'United Kingdom' },
      { value: 'de', label: 'Germany' },
      { value: 'fr', label: 'France' },
      { value: 'jp', label: 'Japan' },
      { value: 'au', label: 'Australia' },
      { value: 'br', label: 'Brazil' },
      { value: 'in', label: 'India' },
      { value: 'cn', label: 'China' },
    ],
    placeholder: 'Select a country',
  },
};'''

    def generate_alert_story(self, spec: ComponentSpec) -> str:
        """Generate Storybook story for Alert component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Alert } from './Alert';
import { fn } from '@storybook/test';

const meta = {
  title: 'Components/Alert',
  component: Alert,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'A notification alert component with different variants and dismiss functionality.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['success', 'warning', 'error', 'info'],
      description: 'The alert variant',
    },
    title: {
      control: 'text',
      description: 'Optional alert title',
    },
    children: {
      control: 'text',
      description: 'Alert content',
    },
  },
  args: {
    onDismiss: fn(),
  },
} satisfies Meta<typeof Alert>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Success: Story = {
  args: {
    variant: 'success',
    title: 'Success!',
    children: 'Your action was completed successfully.',
  },
};

export const Warning: Story = {
  args: {
    variant: 'warning',
    title: 'Warning',
    children: 'Please review this important information.',
  },
};

export const Error: Story = {
  args: {
    variant: 'error',
    title: 'Error',
    children: 'Something went wrong. Please try again.',
  },
};

export const Info: Story = {
  args: {
    variant: 'info',
    title: 'Information',
    children: 'Here is some helpful information.',
  },
};

export const WithoutTitle: Story = {
  args: {
    variant: 'success',
    children: 'This alert has no title, just a message.',
  },
};

export const WithDismiss: Story = {
  args: {
    variant: 'info',
    title: 'Dismissible Alert',
    children: 'Click the X to dismiss this alert.',
    onDismiss: () => alert('Alert dismissed!'),
  },
};

export const AllVariants: Story = {
  render: () => (
    <div className="space-y-4">
      <Alert variant="success" title="Success">
        Your changes have been saved successfully.
      </Alert>
      <Alert variant="warning" title="Warning">
        Please review your input before proceeding.
      </Alert>
      <Alert variant="error" title="Error">
        Failed to save changes. Please try again.
      </Alert>
      <Alert variant="info" title="Info">
        New features are available in this update.
      </Alert>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'All alert variants displayed together.',
      },
    },
  },
};'''

    def generate_modal_story(self, spec: ComponentSpec) -> str:
        """Generate Storybook story for Modal component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Modal } from './Modal';
import { Button } from './Button';
import { useState } from 'react';
import { fn } from '@storybook/test';

const meta = {
  title: 'Components/Modal',
  component: Modal,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'A modal overlay component with focus management and accessibility features.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    isOpen: {
      control: 'boolean',
      description: 'Whether the modal is open',
    },
    title: {
      control: 'text',
      description: 'Modal title',
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md', 'lg', 'xl'],
      description: 'Modal size',
    },
    closeOnOverlayClick: {
      control: 'boolean',
      description: 'Whether clicking the overlay closes the modal',
    },
    children: {
      control: 'text',
      description: 'Modal content',
    },
  },
  args: {
    onClose: fn(),
  },
} satisfies Meta<typeof Modal>;

export default meta;
type Story = StoryObj<typeof meta>;

const ModalWithControls = ({ isOpen, onClose, ...args }: any) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} {...args}>
      <div className="space-y-4">
        <p className="text-sm text-neutral-600">
          This is the modal content. You can put any content here.
        </p>
        <div className="flex justify-end space-x-2">
          <Button variant="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button variant="primary" onClick={onClose}>
            Confirm
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export const Small: Story = {
  render: (args) => <ModalWithControls {...args} />,
  args: {
    isOpen: true,
    title: 'Small Modal',
    size: 'sm',
    children: 'This is a small modal.',
  },
};

export const Medium: Story = {
  render: (args) => <ModalWithControls {...args} />,
  args: {
    isOpen: true,
    title: 'Medium Modal',
    size: 'md',
    children: 'This is a medium modal with the default size.',
  },
};

export const Large: Story = {
  render: (args) => <ModalWithControls {...args} />,
  args: {
    isOpen: true,
    title: 'Large Modal',
    size: 'lg',
    children: 'This is a large modal for more content.',
  },
};

export const ExtraLarge: Story = {
  render: (args) => <ModalWithControls {...args} />,
  args: {
    isOpen: true,
    title: 'Extra Large Modal',
    size: 'xl',
    children: 'This is an extra large modal for complex layouts.',
  },
};

export const WithoutTitle: Story = {
  render: (args) => <ModalWithControls {...args} />,
  args: {
    isOpen: true,
    size: 'md',
    children: 'This modal has no title.',
  },
};

export const WithComplexContent: Story = {
  render: (args) => (
    <Modal isOpen={args.isOpen} onClose={args.onClose} title="Complex Content" size="lg">
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-medium text-neutral-900 mb-2">Section Title</h3>
          <p className="text-sm text-neutral-600">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-1">Field 1</label>
            <input type="text" className="w-full px-3 py-2 border border-neutral-300 rounded-md" placeholder="Enter value" />
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-1">Field 2</label>
            <input type="text" className="w-full px-3 py-2 border border-neutral-300 rounded-md" placeholder="Enter value" />
          </div>
        </div>

        <div className="flex justify-end space-x-3 pt-4 border-t border-neutral-200">
          <Button variant="secondary" onClick={args.onClose}>
            Cancel
          </Button>
          <Button variant="primary" onClick={args.onClose}>
            Save Changes
          </Button>
        </div>
      </div>
    </Modal>
  ),
  args: {
    isOpen: true,
    onClose: fn(),
  },
};'''

    def generate_table_story(self, spec: ComponentSpec) -> str:
        """Generate Storybook story for Table component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Table } from './Table';
import { useState } from 'react';

const meta = {
  title: 'Components/Table',
  component: Table,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'A flexible table component with sorting, selection, and responsive features.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    loading: {
      control: 'boolean',
      description: 'Whether to show loading state',
    },
    selectable: {
      control: 'boolean',
      description: 'Whether rows can be selected',
    },
    emptyMessage: {
      control: 'text',
      description: 'Message to show when no data',
    },
  },
} satisfies Meta<typeof Table>;

export default meta;
type Story = StoryObj<typeof meta>;

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  status: 'active' | 'inactive';
}

const sampleData: User[] = [
  { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin', status: 'active' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'User', status: 'active' },
  { id: 3, name: 'Bob Johnson', email: 'bob@example.com', role: 'User', status: 'inactive' },
  { id: 4, name: 'Alice Brown', email: 'alice@example.com', role: 'Moderator', status: 'active' },
  { id: 5, name: 'Charlie Wilson', email: 'charlie@example.com', role: 'User', status: 'inactive' },
];

const columns = [
  {
    key: 'name' as keyof User,
    header: 'Name',
  },
  {
    key: 'email' as keyof User,
    header: 'Email',
  },
  {
    key: 'role' as keyof User,
    header: 'Role',
  },
  {
    key: 'status' as keyof User,
    header: 'Status',
    render: (value: string) => (
      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
        value === 'active'
          ? 'bg-green-100 text-green-800'
          : 'bg-red-100 text-red-800'
      }`}>
        {value}
      </span>
    ),
  },
];

export const Basic: Story = {
  args: {
    data: sampleData,
    columns: columns,
  },
};

export const Loading: Story = {
  args: {
    data: [],
    columns: columns,
    loading: true,
  },
};

export const Empty: Story = {
  args: {
    data: [],
    columns: columns,
    emptyMessage: 'No users found',
  },
};

export const Selectable: Story = {
  render: () => {
    const [selectedRows, setSelectedRows] = useState<User[]>([]);

    const handleRowSelect = (user: User) => {
      setSelectedRows(prev =>
        prev.find(item => item.id === user.id)
          ? prev.filter(item => item.id !== user.id)
          : [...prev, user]
      );
    };

    return (
      <div className="space-y-4">
        <Table
          data={sampleData}
          columns={columns}
          selectable={true}
          onRowSelect={handleRowSelect}
          selectedRows={selectedRows}
        />
        <div className="text-sm text-neutral-600">
          Selected: {selectedRows.length} row(s)
        </div>
      </div>
    );
  },
};

export const LargeDataset: Story = {
  args: {
    data: Array.from({ length: 50 }, (_, i) => ({
      id: i + 1,
      name: `User ${i + 1}`,
      email: `user${i + 1}@example.com`,
      role: i % 3 === 0 ? 'Admin' : i % 3 === 1 ? 'Moderator' : 'User',
      status: i % 4 === 0 ? 'inactive' : 'active' as 'active' | 'inactive',
    })),
    columns: columns,
  },
};'''

    def generate_navigation_story(self, spec: ComponentSpec) -> str:
        """Generate Storybook story for Navigation component."""
        return '''import type { Meta, StoryObj } from '@storybook/react';
import { Navigation } from './Navigation';
import { fn } from '@storybook/test';

const meta = {
  title: 'Components/Navigation',
  component: Navigation,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'A flexible navigation component supporting horizontal and vertical layouts with nested menus.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['horizontal', 'vertical'],
      description: 'Navigation layout variant',
    },
    collapsible: {
      control: 'boolean',
      description: 'Whether vertical navigation can be collapsed',
    },
  },
  args: {
    onItemClick: fn(),
  },
} satisfies Meta<typeof Navigation>;

export default meta;
type Story = StoryObj<typeof meta>;

const sampleItems = [
  {
    label: 'Dashboard',
    onClick: () => console.log('Dashboard clicked'),
  },
  {
    label: 'Users',
    children: [
      { label: 'All Users', onClick: () => console.log('All Users clicked') },
      { label: 'Add User', onClick: () => console.log('Add User clicked') },
      { label: 'User Roles', onClick: () => console.log('User Roles clicked') },
    ],
  },
  {
    label: 'Settings',
    children: [
      { label: 'General', onClick: () => console.log('General clicked') },
      { label: 'Security', onClick: () => console.log('Security clicked') },
      {
        label: 'Advanced',
        children: [
          { label: 'API Keys', onClick: () => console.log('API Keys clicked') },
          { label: 'Webhooks', onClick: () => console.log('Webhooks clicked') },
        ],
      },
    ],
  },
  {
    label: 'Reports',
    onClick: () => console.log('Reports clicked'),
  },
];

export const Horizontal: Story = {
  args: {
    items: sampleItems.slice(0, 4), // Limit for horizontal layout
    variant: 'horizontal',
  },
};

export const Vertical: Story = {
  args: {
    items: sampleItems,
    variant: 'vertical',
  },
  parameters: {
    layout: 'fullscreen',
  },
};

export const VerticalCollapsible: Story = {
  args: {
    items: sampleItems,
    variant: 'vertical',
    collapsible: true,
  },
  parameters: {
    layout: 'fullscreen',
  },
};

export const WithIcons: Story = {
  args: {
    items: [
      {
        label: 'Dashboard',
        icon: '📊',
        onClick: () => console.log('Dashboard clicked'),
      },
      {
        label: 'Users',
        icon: '👥',
        children: [
          { label: 'All Users', icon: '📋', onClick: () => console.log('All Users clicked') },
          { label: 'Add User', icon: '➕', onClick: () => console.log('Add User clicked') },
        ],
      },
      {
        label: 'Settings',
        icon: '⚙️',
        onClick: () => console.log('Settings clicked'),
      },
    ],
    variant: 'vertical',
  },
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        story: 'Navigation with icons for better visual hierarchy.',
      },
    },
  },
};

export const Simple: Story = {
  args: {
    items: [
      { label: 'Home', onClick: () => console.log('Home') },
      { label: 'About', onClick: () => console.log('About') },
      { label: 'Contact', onClick: () => console.log('Contact') },
    ],
    variant: 'horizontal',
  },
};

export const ActiveItem: Story = {
  args: {
    items: sampleItems,
    variant: 'vertical',
    activeItem: 'Dashboard',
  },
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        story: 'Shows how to highlight the active navigation item.',
      },
    },
  },
};'''

    def generate_container_component(self, spec: ComponentSpec) -> str:
        """Generate a Container component."""
        return '''import React from 'react';

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
  centered?: boolean;
}

export const Container: React.FC<ContainerProps> = ({
  children,
  className = '',
  size = 'lg',
  centered = true
}) => {
  const sizeClasses = {
    sm: 'max-w-screen-sm',
    md: 'max-w-screen-md',
    lg: 'max-w-screen-lg',
    xl: 'max-w-screen-xl',
    '2xl': 'max-w-screen-2xl',
    full: 'max-w-full'
  };

  const classes = [
    sizeClasses[size],
    centered ? 'mx-auto' : '',
    'px-4 sm:px-6 lg:px-8',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={classes}>
      {children}
    </div>
  );
};

export default Container;
'''

    def generate_stack_component(self, spec: ComponentSpec) -> str:
        """Generate a Stack component."""
        return '''import React from 'react';

interface StackProps {
  children: React.ReactNode;
  direction?: 'row' | 'col' | 'row-reverse' | 'col-reverse';
  spacing?: number | string;
  align?: 'start' | 'center' | 'end' | 'baseline' | 'stretch';
  justify?: 'start' | 'center' | 'end' | 'between' | 'around' | 'evenly';
  wrap?: boolean;
  className?: string;
}

export const Stack: React.FC<StackProps> = ({
  children,
  direction = 'col',
  spacing = 4,
  align = 'stretch',
  justify = 'start',
  wrap = false,
  className = ''
}) => {
  const directionClasses = {
    row: 'flex-row',
    col: 'flex-col',
    'row-reverse': 'flex-row-reverse',
    'col-reverse': 'flex-col-reverse'
  };

  const alignClasses = {
    start: 'items-start',
    center: 'items-center',
    end: 'items-end',
    baseline: 'items-baseline',
    stretch: 'items-stretch'
  };

  const justifyClasses = {
    start: 'justify-start',
    center: 'justify-center',
    end: 'justify-end',
    between: 'justify-between',
    around: 'justify-around',
    evenly: 'justify-evenly'
  };

  // Convert numeric spacing to Tailwind spacing classes
  const getSpacingClass = () => {
    if (typeof spacing === 'string') return spacing;
    const prefix = direction === 'row' || direction === 'row-reverse' ? 'space-x' : 'space-y';
    return `${prefix}-${spacing}`;
  };

  const classes = [
    'flex',
    directionClasses[direction],
    getSpacingClass(),
    alignClasses[align],
    justifyClasses[justify],
    wrap ? 'flex-wrap' : 'flex-nowrap',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={classes}>
      {children}
    </div>
  );
};

export default Stack;
'''

    def generate_grid_component(self, spec: ComponentSpec) -> str:
        """Generate a Grid component."""
        return '''import React from 'react';

interface GridProps {
  children: React.ReactNode;
  cols?: number | { sm?: number; md?: number; lg?: number; xl?: number };
  gap?: number | string;
  className?: string;
}

export const Grid: React.FC<GridProps> = ({
  children,
  cols = 1,
  gap = 4,
  className = ''
}) => {
  const getColClasses = () => {
    if (typeof cols === 'number') {
      return `grid-cols-${cols}`;
    }
    
    return [
      cols.sm ? `sm:grid-cols-${cols.sm}` : '',
      cols.md ? `md:grid-cols-${cols.md}` : '',
      cols.lg ? `lg:grid-cols-${cols.lg}` : '',
      cols.xl ? `xl:grid-cols-${cols.xl}` : '',
    ].filter(Boolean).join(' ');
  };

  const getGapClass = () => {
    if (typeof gap === 'string') return gap;
    return `gap-${gap}`;
  };

  const classes = [
    'grid',
    getColClasses(),
    getGapClass(),
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={classes}>
      {children}
    </div>
  );
};

export default Grid;
'''

    def generate_sidebar_component(self, spec: ComponentSpec) -> str:
        """Generate a Sidebar component."""
        return '''import React, { useState } from 'react';

interface SidebarItem {
  label: string;
  icon?: React.ReactNode;
  href: string;
  active?: boolean;
}

interface SidebarProps {
  items: SidebarItem[];
  collapsed?: boolean;
  onToggle?: () => void;
  brandName?: string;
  className?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  items,
  collapsed = false,
  onToggle,
  brandName = 'DesignSystem',
  className = ''
}) => {
  return (
    <aside className={`h-screen bg-background-surface border-r border-border-base transition-all duration-300 ${collapsed ? 'w-20' : 'w-64'} ${className}`}>
      <div className="flex flex-col h-full">
        <div className="p-4 border-b border-border-base flex items-center justify-between">
          {!collapsed && <span className="font-bold text-lg text-text-base">{brandName}</span>}
          <button onClick={onToggle} className="p-2 hover:bg-background-base rounded-md text-text-muted">
            {collapsed ? '→' : '←'}
          </button>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          {items.map((item, idx) => (
            <a
              key={idx}
              href={item.href}
              className={`flex items-center space-x-3 p-3 rounded-md transition-colors ${
                item.active 
                  ? 'bg-primary-500 text-white' 
                  : 'text-text-base hover:bg-background-base'
              }`}
            >
              {item.icon && <span>{item.icon}</span>}
              {!collapsed && <span>{item.label}</span>}
            </a>
          ))}
        </nav>
      </div>
    </aside>
  );
};

export default Sidebar;
'''

    def generate_header_component(self, spec: ComponentSpec) -> str:
        """Generate a Header component."""
        return '''import React from 'react';

interface NavLink {
  label: string;
  href: string;
}

interface HeaderProps {
  links: NavLink[];
  logo?: React.ReactNode;
  brandName?: string;
  sticky?: boolean;
  className?: string;
}

export const Header: React.FC<HeaderProps> = ({
  links,
  logo,
  brandName = 'DesignSystem',
  sticky = true,
  className = ''
}) => {
  return (
    <header className={`w-full bg-background-surface border-b border-border-base px-6 py-4 ${sticky ? 'sticky top-0 z-50' : ''} ${className}`}>
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-2">
          {logo || <div className="w-8 h-8 bg-primary-500 rounded-md" />}
          <span className="font-bold text-xl text-text-base">{brandName}</span>
        </div>
        <nav className="hidden md:flex items-center space-x-8">
          {links.map((link, idx) => (
            <a key={idx} href={link.href} className="text-text-base hover:text-primary-500 transition-colors">
              {link.label}
            </a>
          ))}
        </nav>
        <div className="flex items-center space-x-4">
          <button className="md:hidden p-2 text-text-base">Menu</button>
        </div>
      </div>
    </header>
  );
};

export default Header;
'''

    def generate_footer_component(self, spec: ComponentSpec) -> str:
        """Generate a Footer component."""
        return '''import React from 'react';

interface FooterColumn {
  title: string;
  links: { label: string; href: string }[];
}

interface FooterProps {
  columns: FooterColumn[];
  copyright?: string;
  className?: string;
}

export const Footer: React.FC<FooterProps> = ({
  columns,
  copyright = `© ${new Date().getFullYear()} DesignSystem. All rights reserved.`,
  className = ''
}) => {
  return (
    <footer className={`bg-background-surface border-t border-border-base pt-12 pb-8 px-6 ${className}`}>
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
          {columns.map((col, idx) => (
            <div key={idx}>
              <h4 className="font-bold text-text-base mb-4 uppercase text-xs tracking-wider">{col.title}</h4>
              <ul className="space-y-2">
                {col.links.map((link, lIdx) => (
                  <li key={lIdx}>
                    <a href={link.href} className="text-text-muted hover:text-primary-500 text-sm transition-colors">
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="pt-8 border-t border-border-base text-center text-text-muted text-sm">
          {copyright}
        </div>
      </div>
    </footer>
  );
};

export default Footer;
'''

    def generate_hero_component(self, spec: ComponentSpec) -> str:
        """Generate a Hero component."""
        return '''import React from 'react';
import { Button } from './Button';

interface HeroProps {
  title: string;
  subtitle: string;
  primaryAction?: { label: string; onClick: () => void };
  secondaryAction?: { label: string; onClick: () => void };
  imageSrc?: string;
  centered?: boolean;
  className?: string;
}

export const Hero: React.FC<HeroProps> = ({
  title,
  subtitle,
  primaryAction,
  secondaryAction,
  imageSrc,
  centered = true,
  className = ''
}) => {
  return (
    <section className={`py-20 px-6 ${className}`}>
      <div className={`max-w-7xl mx-auto flex flex-col ${centered ? 'items-center text-center' : 'md:flex-row md:items-center md:text-left'} gap-12`}>
        <div className="flex-1 space-y-8">
          <h1 className="text-5xl md:text-6xl font-extrabold text-text-base leading-tight">
            {title}
          </h1>
          <p className="text-xl text-text-muted max-w-2xl">
            {subtitle}
          </p>
          <div className={`flex flex-wrap gap-4 ${centered ? 'justify-center' : ''}`}>
            {primaryAction && (
              <Button size="lg" onClick={primaryAction.onClick}>
                {primaryAction.label}
              </Button>
            )}
            {secondaryAction && (
              <Button size="lg" variant="secondary" onClick={secondaryAction.onClick}>
                {secondaryAction.label}
              </Button>
            )}
          </div>
        </div>
        {imageSrc && (
          <div className="flex-1 w-full max-w-xl">
            <img src={imageSrc} alt="Hero" className="rounded-2xl shadow-2xl w-full object-cover" />
          </div>
        )}
      </div>
    </section>
  );
};

export default Hero;
'''

    def generate_component_index(self, components: List[ComponentSpec]) -> str:
        """Generate an index file that exports all components."""
        exports = []

        for component in components:
            component_name = component.name
            if component_name.lower() == 'button':
                exports.append(f"export {{ default as Button }} from './Button';")
            elif component_name.lower() == 'input':
                exports.append(f"export {{ default as Input }} from './Input';")
            elif component_name.lower() == 'select':
                exports.append(f"export {{ default as Select }} from './Select';")
            elif component_name.lower() == 'alert':
                exports.append(f"export {{ default as Alert }} from './Alert';")

        return "\n".join(exports)

    def generate_tailwind_config(self) -> str:
        """Generate a Tailwind config that uses our design tokens."""
        config = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary colors
        primary: {
'''

        # Add primary colors
        primary_colors = [c for c in self.tokens.colors if c.role == 'primary']
        for color in primary_colors:
            name = color.name.replace('primary-', '')
            config += f'          {name}: "var(--color-{color.name})",\n'

        config += '''        },
        // Neutral colors
        neutral: {
'''

        # Add neutral colors
        neutral_colors = [c for c in self.tokens.colors if c.role == 'neutral']
        for color in neutral_colors:
            name = color.name.replace('neutral-', '')
            config += f'          {name}: "var(--color-{color.name})",\n'

        config += '''        },
        // Semantic colors
        background: {
          base: "var(--bg-base)",
          surface: "var(--bg-surface)",
        },
        text: {
          base: "var(--text-base)",
          muted: "var(--text-muted)",
        },
        border: {
          base: "var(--border-base)",
        },
        success: "var(--color-success-500)",
        warning: "var(--color-warning-500)",
        error: "var(--color-error-500)",
        info: "var(--color-info-500)",
      },
      fontFamily: {
        sans: ["var(--font-body-1)", "system-ui", "sans-serif"],
        heading: ["var(--font-heading-1)", "system-ui", "sans-serif"],
      },
      fontSize: {
'''

        # Add typography scales
        for typo in self.tokens.typography:
            if typo.role in ['heading', 'body']:
                config += f'        "{typo.name}": ["{typo.size}", "{typo.line_height}"],\n'

        config += '''      },
      spacing: {
'''

        # Add spacing scale
        for space in self.tokens.spacing:
            name = space.name.replace('space-', '')
            config += f'        {name}: "var(--space-{space.name})",\n'

        config += '''      },
      borderRadius: {
'''

        # Add border radius
        for key, value in self.tokens.border_radius.items():
            config += f'        {key}: "var(--radius-{key})",\n'

        config += '''      },
      boxShadow: {
'''

        # Add shadows
        for key, value in self.tokens.shadows.items():
            config += f'        {key}: "var(--shadow-{key})",\n'

        config += '''      },
    },
  },
  plugins: [],
}
'''
        return config

    def generate_package_json(self) -> str:
        """Generate a package.json for the React component library."""
        return '''{
  "name": "design-system-components",
  "version": "1.0.0",
  "description": "Generated React component library",
  "main": "dist/index.js",
  "module": "dist/index.esm.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "rollup -c",
    "dev": "rollup -c -w",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build",
    "preview-storybook": "npm run build-storybook && npx http-server storybook-static -p 3000"
  },
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "dependencies": {
    "framer-motion": "^11.0.0"
  },
  "devDependencies": {
    "@rollup/plugin-commonjs": "^25.0.0",
    "@rollup/plugin-node-resolve": "^15.0.0",
    "@rollup/plugin-typescript": "^11.0.0",
    "@storybook/addon-essentials": "^7.6.0",
    "@storybook/addon-interactions": "^7.6.0",
    "@storybook/addon-links": "^7.6.0",
    "@storybook/blocks": "^7.6.0",
    "@storybook/react": "^7.6.0",
    "@storybook/react-vite": "^7.6.0",
    "@storybook/test": "^7.6.0",
    "@testing-library/jest-dom": "^6.0.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/user-event": "^14.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "autoprefixer": "^10.4.0",
    "http-server": "^14.1.1",
    "jest": "^29.0.0",
    "jest-environment-jsdom": "^29.0.0",
    "postcss": "^8.4.0",
    "rollup": "^4.0.0",
    "rollup-plugin-postcss": "^4.0.0",
    "storybook": "^7.6.0",
    "tailwindcss": "^3.3.0",
    "typescript": "^5.0.0"
  },
  "files": [
    "dist",
    "src"
  ]
}
'''

    def generate_figma_tokens(self) -> str:
        """Generate a JSON file formatted for Figma (Tokens Studio)."""
        import json
        
        tokens_structure = {
            "global": {
                "colors": {},
                "typography": {},
                "spacing": {},
                "borderRadius": {},
                "shadows": {}
            }
        }
        
        # Colors
        for color in self.tokens.colors:
            tokens_structure["global"]["colors"][color.name] = {
                "value": color.value,
                "type": "color"
            }
            
        # Typography
        for typo in self.tokens.typography:
            tokens_structure["global"]["typography"][typo.name] = {
                "value": {
                    "fontFamily": typo.family,
                    "fontWeight": str(typo.weight),
                    "fontSize": typo.size,
                    "lineHeight": str(typo.line_height)
                },
                "type": "typography"
            }
            
        # Spacing
        for space in self.tokens.spacing:
            tokens_structure["global"]["spacing"][space.name] = {
                "value": space.value,
                "type": "spacing"
            }
            
        # Border Radius
        for key, value in self.tokens.border_radius.items():
            tokens_structure["global"]["borderRadius"][key] = {
                "value": value,
                "type": "borderRadius"
            }
            
        # Shadows
        for key, value in self.tokens.shadows.items():
            tokens_structure["global"]["shadows"][key] = {
                "value": value,
                "type": "boxShadow"
            }
            
        return json.dumps(tokens_structure, indent=2)
