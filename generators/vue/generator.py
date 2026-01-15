"""Vue 3 component generator with Composition API."""

from typing import List
from models import DesignTokens, ComponentSpec


class VueGenerator:
    """Generates Vue 3 components with Composition API."""
    
    def __init__(self, tokens: DesignTokens):
        self.tokens = tokens
    
    def generate_button_component(self, spec: ComponentSpec) -> str:
        """Generate Vue 3 Button component with <script setup>."""
        variants_union = ' | '.join(f'"{v}"' for v in spec.variants)
        default_variant = spec.variants[0]
        
        return f'''<script setup lang="ts">
import {{ computed }} from 'vue';

/**
 * Button component props
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
  /** HTML button type */
  type?: 'button' | 'submit' | 'reset';
  /** Additional CSS classes */
  class?: string;
  /** ARIA label for accessibility */
  ariaLabel?: string;
}}

const props = withDefaults(defineProps<ButtonProps>(), {{
  variant: '{default_variant}',
  size: 'md',
  disabled: false,
  loading: false,
  type: 'button',
  class: '',
}});

const emit = defineEmits<{{
  click: [];
}}>();

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

const buttonClasses = computed(() => {{
  return `${{baseClasses}} ${{variantClasses[props.variant]}} ${{sizeClasses[props.size]}} ${{props.class}}`;
}});

const handleClick = () => {{
  if (!props.disabled && !props.loading) {{
    emit('click');
  }}
}};
</script>

<template>
  <button
    :type="type"
    :class="buttonClasses"
    :disabled="disabled || loading"
    :aria-label="ariaLabel"
    :aria-busy="loading"
    @click="handleClick"
  >
    <svg
      v-if="loading"
      class="animate-spin h-4 w-4 mr-2"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      ></circle>
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
    <slot />
  </button>
</template>
'''
    
    def generate_input_component(self, spec: ComponentSpec) -> str:
        """Generate Vue 3 Input component."""
        return '''<script setup lang="ts">
import { computed } from 'vue';

/**
 * Input component props
 */
export interface InputProps {
  /** Input type */
  type?: 'text' | 'email' | 'password' | 'search' | 'number';
  /** Placeholder text */
  placeholder?: string;
  /** Input value (v-model) */
  modelValue?: string;
  /** Whether input has error */
  error?: boolean;
  /** Whether input is disabled */
  disabled?: boolean;
  /** Whether input is required */
  required?: boolean;
  /** Additional CSS classes */
  class?: string;
  /** Input name attribute */
  name?: string;
  /** Input id attribute */
  id?: string;
}

const props = withDefaults(defineProps<InputProps>(), {
  type: 'text',
  error: false,
  disabled: false,
  required: false,
  class: '',
});

const emit = defineEmits<{
  'update:modelValue': [value: string];
}>();

const baseClasses = 'w-full px-4 py-2 border rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1';
const stateClasses = computed(() => 
  props.error 
    ? 'border-error-300 focus:ring-error-500 focus:border-error-500' 
    : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500'
);
const disabledClasses = computed(() => 
  props.disabled ? 'bg-neutral-100 cursor-not-allowed opacity-60' : 'bg-white'
);

const inputClasses = computed(() => 
  `${baseClasses} ${stateClasses.value} ${disabledClasses.value} ${props.class}`
);

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:modelValue', target.value);
};
</script>

<template>
  <input
    :type="type"
    :placeholder="placeholder"
    :value="modelValue"
    :disabled="disabled"
    :required="required"
    :class="inputClasses"
    :name="name"
    :id="id"
    :aria-invalid="error"
    :aria-required="required"
    @input="handleInput"
  />
</template>
'''
