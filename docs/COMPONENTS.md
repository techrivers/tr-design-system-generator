# 🧩 Component Library Documentation

Complete documentation for all generated React components.

## Table of Contents

- [Component Overview](#component-overview)
- [Form Components](#form-components)
- [Feedback Components](#feedback-components)
- [Navigation Components](#navigation-components)
- [Layout Components](#layout-components)
- [Data Display Components](#data-display-components)
- [Component Props Reference](#component-props-reference)
- [Accessibility](#accessibility)
- [Styling and Theming](#styling-and-theming)
- [Usage Examples](#usage-examples)

## Component Overview

The Design System Generator creates 24+ production-ready React components organized into logical categories. All components are built with TypeScript, include comprehensive accessibility features, and follow modern React patterns.

### Component Categories

| Category | Count | Description |
|----------|-------|-------------|
| Form | 8 | Input controls and form elements |
| Feedback | 6 | Status indicators and user feedback |
| Navigation | 4 | Site navigation and page structure |
| Layout | 2 | Content organization and layout |
| Data Display | 4 | Data presentation and user info |

### Component Features

Each generated component includes:
- ✅ **TypeScript interfaces** with full prop validation
- ✅ **Accessibility support** (ARIA attributes, keyboard navigation)
- ✅ **Responsive design** with Tailwind CSS
- ✅ **Multiple variants** and interaction states
- ✅ **Interactive Storybook** documentation
- ✅ **Jest unit tests** with coverage
- ✅ **Professional build setup**

## Form Components

### Button

Versatile button component with multiple variants and states.

```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'tertiary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}
```

**Variants:**
- `primary`: Main call-to-action (blue background)
- `secondary`: Alternative action (gray background)
- `tertiary`: Subtle action (bordered)
- `danger`: Destructive action (red background)

**Sizes:**
- `sm`: Compact button (32px height)
- `md`: Standard button (40px height)
- `lg`: Large button (48px height)

**States:**
- `default`: Normal state
- `hover`: Hover state styling
- `focus`: Focus state with ring
- `disabled`: Disabled state
- `loading`: Loading spinner

### Input

Flexible input component supporting various input types.

```tsx
interface InputProps {
  type?: 'text' | 'email' | 'password' | 'search' | 'number';
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  error?: boolean;
  disabled?: boolean;
  required?: boolean;
}
```

**Types:**
- `text`: Standard text input
- `email`: Email validation
- `password`: Masked password input
- `search`: Search input with icon
- `number`: Numeric input

**States:**
- `default`: Normal state
- `focus`: Focused with blue ring
- `error`: Red border and styling
- `disabled`: Grayed out and readonly

### Select

Dropdown selection component with keyboard navigation.

```tsx
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
```

**Features:**
- Keyboard navigation (↑↓ arrows, Enter, Escape)
- Search/filter functionality
- Custom option rendering
- Form integration support

### Textarea

Multi-line text input with character counting.

```tsx
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
```

**Features:**
- Character counter (when `maxLength` specified)
- Resizable options
- Auto-growing height
- Validation states

### Checkbox

Boolean selection with indeterminate state support.

```tsx
interface CheckboxProps {
  label?: string;
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  disabled?: boolean;
  required?: boolean;
  indeterminate?: boolean;
  size?: 'sm' | 'md' | 'lg';
}
```

**States:**
- `checked`: Selected state
- `unchecked`: Unselected state
- `indeterminate`: Mixed state (parent of mixed children)

### Radio

Single selection from multiple options.

```tsx
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
```

**Features:**
- Group selection (only one active)
- Keyboard navigation
- Orientation control
- Individual option disabling

### DatePicker

Calendar-based date selection component.

```tsx
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
```

**Features:**
- Calendar popup interface
- Date range restrictions
- Custom date formatting
- Keyboard navigation
- Mobile-responsive

### Switch

Modern toggle component with smooth animations.

```tsx
interface SwitchProps {
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  disabled?: boolean;
  size?: 'sm' | 'md' | 'lg';
  label?: string;
}
```

**Features:**
- Smooth toggle animation
- Optional label
- Size variants
- Keyboard accessible

## Feedback Components

### Alert

Contextual notification and messaging component.

```tsx
interface AlertProps {
  variant?: 'success' | 'warning' | 'error' | 'info';
  title?: string;
  children: React.ReactNode;
  onDismiss?: () => void;
}
```

**Variants:**
- `success`: Green theme for positive messages
- `warning`: Yellow theme for caution messages
- `error`: Red theme for error messages
- `info`: Blue theme for informational messages

### Badge

Small status and labeling component.

```tsx
interface BadgeProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info';
  size?: 'sm' | 'md' | 'lg';
  rounded?: boolean;
  dot?: boolean;
}
```

**Variants:** Same as Alert component
**Styles:** Rounded or dot-only variants

### Tooltip

Contextual help and information overlay.

```tsx
interface TooltipProps {
  content: string;
  children: React.ReactNode;
  position?: 'top' | 'bottom' | 'left' | 'right';
  delay?: number;
  disabled?: boolean;
}
```

**Features:**
- Configurable positioning
- Hover and focus activation
- Delay timing
- Accessibility compliant

### Modal

Overlay dialog for important information and actions.

```tsx
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  closeOnOverlayClick?: boolean;
}
```

**Features:**
- Focus management
- Escape key handling
- Backdrop overlay
- Size variants

### Progress

Loading and completion progress indicator.

```tsx
interface ProgressProps {
  value?: number;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'success' | 'warning' | 'error';
  showLabel?: boolean;
  label?: string;
  animated?: boolean;
}
```

**Features:**
- Determinate and indeterminate modes
- Size and color variants
- Label display options
- Animation controls

### Skeleton

Loading placeholder component.

```tsx
interface SkeletonProps {
  variant?: 'text' | 'rectangular' | 'circular';
  width?: string | number;
  height?: string | number;
  animation?: 'pulse' | 'wave' | 'none';
  className?: string;
}

interface SkeletonTextProps {
  lines?: number;
  className?: string;
}

interface SkeletonCardProps {
  showAvatar?: boolean;
  lines?: number;
  className?: string;
}
```

**Compound Components:**
- `SkeletonText`: Multi-line text placeholders
- `SkeletonCard`: Card-shaped loading states

## Navigation Components

### Navigation

Site navigation with horizontal/vertical layouts.

```tsx
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
```

**Features:**
- Nested menu support
- Active state management
- Collapsible vertical menus
- Custom icons

### Tabs

Tabbed interface for organizing content.

```tsx
interface TabItem {
  id: string;
  label: string;
  content: React.ReactNode;
  disabled?: boolean;
}

interface TabsProps {
  tabs: TabItem[];
  multiple?: boolean;
  defaultExpanded?: string[];
  size?: 'sm' | 'md' | 'lg';
}
```

**Features:**
- Single/multiple panel expansion
- Keyboard navigation
- Size variants
- Disabled tab support

### Breadcrumb

Page hierarchy navigation.

```tsx
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
```

**Features:**
- Automatic truncation for long paths
- Custom separators
- Click handling
- Size variants

### Pagination

Data navigation for large datasets.

```tsx
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
```

**Features:**
- First/Last navigation
- Page number display
- Size variants
- Keyboard navigation

## Layout Components

### Card

Content container with multiple variants.

```tsx
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
```

**Features:**
- Header/footer sections
- Multiple visual variants
- Clickable cards
- Size variants

### Accordion

Collapsible content panels.

```tsx
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
```

**Features:**
- Single/multiple expansion modes
- Keyboard accessibility
- Size variants
- Disabled items

## Data Display Components

### Table

Data table with sorting and selection.

```tsx
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
```

**Features:**
- Custom column rendering
- Row selection
- Loading states
- Empty states
- Sorting support

### Avatar

User representation component.

```tsx
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
```

**Features:**
- Image or initials display
- Status indicators
- Size and shape variants
- Fallback content

### Search

Advanced search with autocomplete.

```tsx
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
```

**Features:**
- Debounced search
- Autocomplete suggestions
- Keyboard navigation
- Result selection
- Loading states

## Component Props Reference

### Common Props

All components support these common props:

```tsx
interface CommonProps {
  className?: string;        // Additional CSS classes
  style?: React.CSSProperties; // Inline styles
  'data-testid'?: string;    // Test identifiers
}
```

### Event Handlers

Components follow React event naming conventions:

```tsx
onClick?: (event: React.MouseEvent) => void;
onChange?: (value: any) => void;
onFocus?: (event: React.FocusEvent) => void;
onBlur?: (event: React.BlurEvent) => void;
onKeyDown?: (event: React.KeyboardEvent) => void;
```

### Size Variants

Consistent sizing across components:

```tsx
type SizeVariant = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
```

### Color Variants

Consistent color theming:

```tsx
type ColorVariant = 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info';
```

## Accessibility

### ARIA Support

All components include proper ARIA attributes:

```tsx
// Form controls
aria-label="Button label"
aria-describedby="helper-text"
aria-invalid={error}

// Interactive elements
role="button"
aria-expanded={expanded}
aria-selected={selected}

// Status messages
aria-live="polite"
aria-atomic="true"
```

### Keyboard Navigation

Components support keyboard interaction:

- **Tab**: Move between focusable elements
- **Enter/Space**: Activate buttons and controls
- **Arrow Keys**: Navigate menus and lists
- **Escape**: Close modals and dropdowns

### Screen Reader Support

Components are tested with screen readers:

- Semantic HTML structure
- Proper heading hierarchy
- Descriptive labels and instructions
- Status announcements for dynamic content

### Focus Management

Proper focus handling:

- Visible focus indicators
- Logical tab order
- Focus trapping in modals
- Focus restoration after actions

## Styling and Theming

### Design Token Integration

Components use CSS custom properties from design tokens:

```css
:root {
  --color-primary-50: #eff6ff;
  --color-primary-500: #3b82f6;
  --color-primary-900: #1e3a8a;
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --radius-md: 0.375rem;
}
```

### Tailwind CSS Classes

Components use utility-first styling:

```tsx
const classes = `
  px-4 py-2                    // Spacing
  bg-primary-500               // Background color
  hover:bg-primary-600         // Hover states
  text-white                   // Text color
  rounded-md                   // Border radius
  shadow-sm                    // Box shadow
  focus:ring-2                 // Focus ring
  focus:ring-primary-500       // Focus color
  disabled:opacity-50          // Disabled state
`;
```

### Theme Customization

Override design tokens to customize themes:

```css
/* Custom theme overrides */
:root {
  --color-primary-500: #your-brand-color;
  --color-primary-600: #your-hover-color;
  --font-family-sans: 'Your Font', system-ui;
}
```

### CSS-in-JS Support

Components can be extended with styled-components or emotion:

```tsx
import styled from 'styled-components';

const CustomButton = styled(Button)`
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  &:hover {
    transform: translateY(-2px);
  }
`;
```

## Usage Examples

### Complete Form

```tsx
import {
  Button,
  Input,
  Select,
  Textarea,
  Checkbox,
  Radio,
  DatePicker
} from './components';

function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
    newsletter: false,
    contactMethod: 'email'
  });

  const contactOptions = [
    { value: 'email', label: 'Email' },
    { value: 'phone', label: 'Phone' },
    { value: 'text', label: 'Text Message' }
  ];

  return (
    <form className="space-y-6 max-w-md">
      <Input
        type="text"
        placeholder="Your name"
        value={formData.name}
        onChange={(value) => setFormData({...formData, name: value})}
        required
      />

      <Input
        type="email"
        placeholder="your.email@example.com"
        value={formData.email}
        onChange={(value) => setFormData({...formData, email: value})}
        required
      />

      <Textarea
        placeholder="Your message..."
        value={formData.message}
        onChange={(value) => setFormData({...formData, message: value})}
        rows={4}
      />

      <Radio
        options={contactOptions}
        value={formData.contactMethod}
        onChange={(value) => setFormData({...formData, contactMethod: value})}
      />

      <Checkbox
        label="Subscribe to newsletter"
        checked={formData.newsletter}
        onChange={(checked) => setFormData({...formData, newsletter: checked})}
      />

      <Button type="submit" variant="primary" className="w-full">
        Send Message
      </Button>
    </form>
  );
}
```

### Data Dashboard

```tsx
import {
  Card,
  Table,
  Progress,
  Badge,
  Avatar,
  Tabs
} from './components';

function Dashboard() {
  const projects = [
    {
      id: 1,
      name: 'Website Redesign',
      progress: 75,
      status: 'In Progress',
      team: ['Alice', 'Bob', 'Charlie']
    }
  ];

  const tabs = [
    {
      id: 'overview',
      label: 'Overview',
      content: <div>Dashboard overview content...</div>
    },
    {
      id: 'projects',
      label: 'Projects',
      content: (
        <Table
          data={projects}
          columns={[
            { key: 'name', header: 'Project' },
            {
              key: 'progress',
              header: 'Progress',
              render: (value) => <Progress value={value} size="sm" />
            },
            {
              key: 'status',
              header: 'Status',
              render: (value) => <Badge variant="success">{value}</Badge>
            },
            {
              key: 'team',
              header: 'Team',
              render: (team) => (
                <div className="flex -space-x-2">
                  {team.map((name, i) => (
                    <Avatar key={i} name={name} size="sm" />
                  ))}
                </div>
              )
            }
          ]}
        />
      )
    }
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card title="Total Projects" className="text-center">
          <div className="text-3xl font-bold">24</div>
          <Progress value={80} showLabel />
        </Card>

        <Card title="Active Tasks" className="text-center">
          <div className="text-3xl font-bold">12</div>
          <Badge variant="warning">In Progress</Badge>
        </Card>

        <Card title="Completed" className="text-center">
          <div className="text-3xl font-bold">89</div>
          <Badge variant="success">On Track</Badge>
        </Card>
      </div>

      <Card>
        <Tabs tabs={tabs} />
      </Card>
    </div>
  );
}
```

### Navigation Layout

```tsx
import {
  Navigation,
  Breadcrumb,
  Pagination
} from './components';

function AppLayout({ children }: { children: React.ReactNode }) {
  const navItems = [
    { label: 'Dashboard', href: '/' },
    {
      label: 'Projects',
      children: [
        { label: 'All Projects', href: '/projects' },
        { label: 'My Projects', href: '/projects/mine' },
        { label: 'Archived', href: '/projects/archived' }
      ]
    },
    { label: 'Team', href: '/team' },
    { label: 'Settings', href: '/settings' }
  ];

  const breadcrumbItems = [
    { label: 'Projects', href: '/projects' },
    { label: 'Website Redesign', href: '/projects/1' },
    { label: 'Design Review' }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation
        items={navItems}
        variant="horizontal"
        className="bg-white border-b"
      />

      <main className="max-w-7xl mx-auto py-6 px-4">
        <Breadcrumb items={breadcrumbItems} className="mb-6" />

        {children}

        <Pagination
          currentPage={3}
          totalPages={10}
          onPageChange={(page) => console.log('Go to page:', page)}
          className="mt-8"
        />
      </main>
    </div>
  );
}
```

This documentation covers all generated components with their props, features, and usage examples. Each component is designed to be accessible, themeable, and production-ready.

