// Component Playground JavaScript

let currentComponent = null;
let componentProps = {};
let designSystemData = null;

// Component templates with more details
const componentTemplates = {
    Button: {
        props: {
            variant: { type: 'select', options: ['primary', 'secondary', 'tertiary', 'danger'], default: 'primary', label: 'Variant' },
            size: { type: 'select', options: ['sm', 'md', 'lg'], default: 'md', label: 'Size' },
            disabled: { type: 'checkbox', default: false, label: 'Disabled' },
            children: { type: 'text', default: 'Click me', label: 'Label' }
        },
        code: (props) => `<Button variant="${props.variant}" size="${props.size}" ${props.disabled ? 'disabled' : ''}>
  ${props.children}
</Button>`,
        preview: (props) => {
            const variantClass = props.variant === 'primary' ? 'bg-indigo-600 text-white hover:bg-indigo-700' : 
                               props.variant === 'secondary' ? 'bg-gray-200 text-gray-800 hover:bg-gray-300' :
                               props.variant === 'danger' ? 'bg-red-600 text-white hover:bg-red-700' : 
                               'bg-gray-100 text-gray-800 hover:bg-gray-200';
            const sizeClass = props.size === 'sm' ? 'px-3 py-1 text-sm' : 
                            props.size === 'lg' ? 'px-6 py-3 text-lg' : 'px-4 py-2';
            return `<button class="${variantClass} ${sizeClass} rounded transition-colors ${props.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}">
                ${props.children}
            </button>`;
        }
    },
    Input: {
        props: {
            type: { type: 'select', options: ['text', 'email', 'password', 'number'], default: 'text', label: 'Type' },
            placeholder: { type: 'text', default: 'Enter text...', label: 'Placeholder' },
            disabled: { type: 'checkbox', default: false, label: 'Disabled' },
            error: { type: 'checkbox', default: false, label: 'Error State' }
        },
        code: (props) => `<Input 
  type="${props.type}"
  placeholder="${props.placeholder}"
  ${props.disabled ? 'disabled' : ''}
  ${props.error ? 'error' : ''}
/>`,
        preview: (props) => {
            const errorClass = props.error ? 'border-red-500' : 'border-gray-300';
            return `<input type="${props.type}" 
                placeholder="${props.placeholder}"
                class="w-full px-3 py-2 border rounded ${errorClass} ${props.disabled ? 'opacity-50 cursor-not-allowed bg-gray-100' : ''}"
                ${props.disabled ? 'disabled' : ''} />`;
        }
    },
    Card: {
        props: {
            title: { type: 'text', default: 'Card Title', label: 'Title' },
            description: { type: 'text', default: 'Card description text', label: 'Description' },
            padding: { type: 'select', options: ['sm', 'md', 'lg'], default: 'md', label: 'Padding' }
        },
        code: (props) => `<Card padding="${props.padding}">
  <Card.Title>${props.title}</Card.Title>
  <Card.Description>${props.description}</Card.Description>
</Card>`,
        preview: (props) => {
            const paddingClass = props.padding === 'sm' ? 'p-3' : props.padding === 'lg' ? 'p-6' : 'p-4';
            return `<div class="border rounded-lg shadow-sm ${paddingClass}">
                <h3 class="text-lg font-semibold mb-2">${props.title}</h3>
                <p class="text-gray-600 text-sm">${props.description}</p>
            </div>`;
        }
    },
    Badge: {
        props: {
            variant: { type: 'select', options: ['default', 'success', 'warning', 'error', 'info'], default: 'default', label: 'Variant' },
            children: { type: 'text', default: 'Badge', label: 'Label' }
        },
        code: (props) => `<Badge variant="${props.variant}">${props.children}</Badge>`,
        preview: (props) => {
            const variantClass = props.variant === 'success' ? 'bg-green-100 text-green-800' :
                               props.variant === 'warning' ? 'bg-yellow-100 text-yellow-800' :
                               props.variant === 'error' ? 'bg-red-100 text-red-800' :
                               props.variant === 'info' ? 'bg-blue-100 text-blue-800' :
                               'bg-gray-100 text-gray-800';
            return `<span class="${variantClass} px-2 py-1 rounded-full text-xs font-medium">${props.children}</span>`;
        }
    },
    Alert: {
        props: {
            variant: { type: 'select', options: ['success', 'warning', 'error', 'info'], default: 'info', label: 'Variant' },
            title: { type: 'text', default: 'Alert Title', label: 'Title' },
            message: { type: 'text', default: 'This is an alert message', label: 'Message' }
        },
        code: (props) => `<Alert variant="${props.variant}">
  <Alert.Title>${props.title}</Alert.Title>
  <Alert.Message>${props.message}</Alert.Message>
</Alert>`,
        preview: (props) => {
            const variantClass = props.variant === 'success' ? 'bg-green-50 border-green-200 text-green-800' :
                               props.variant === 'warning' ? 'bg-yellow-50 border-yellow-200 text-yellow-800' :
                               props.variant === 'error' ? 'bg-red-50 border-red-200 text-red-800' :
                               'bg-blue-50 border-blue-200 text-blue-800';
            return `<div class="${variantClass} border rounded-lg p-4">
                <div class="font-semibold mb-1">${props.title}</div>
                <div class="text-sm">${props.message}</div>
            </div>`;
        }
    }
};

// Initialize playground
function initPlayground() {
    // Check for file ID in URL
    const urlParams = new URLSearchParams(window.location.search);
    const fileId = urlParams.get('file');
    if (fileId) {
        loadDesignSystem(fileId);
    }
    
    // Setup component selector
    const componentSelect = document.getElementById('componentSelect');
    if (componentSelect) {
        componentSelect.addEventListener('change', (e) => {
            const componentName = e.target.value;
            if (componentName && componentTemplates[componentName]) {
                loadComponent(componentName);
            } else {
                clearPlayground();
            }
        });
    }
    
    // Setup export buttons
    setupExportButtons();
    
    // Setup JSON editor toggle
    setupJSONEditor();
}

// Load design system from API
async function loadDesignSystem(fileId) {
    try {
        const response = await fetch(`/api/tokens/${fileId}`);
        const data = await response.json();
        if (data.success) {
            designSystemData = data;
            showNotification('Design system loaded', 'success');
        }
    } catch (error) {
        console.error('Error loading design system:', error);
        showNotification('Error loading design system', 'error');
    }
}

// Load component
function loadComponent(name) {
    currentComponent = name;
    const template = componentTemplates[name];
    if (!template) return;
    
    // Initialize props with defaults
    componentProps = {};
    Object.keys(template.props).forEach(key => {
        componentProps[key] = template.props[key].default;
    });

    renderPropsEditor(template.props);
    updatePreview();
    updateCode();
    updateJSONEditor();
}

// Clear playground
function clearPlayground() {
    currentComponent = null;
    componentProps = {};
    document.getElementById('propsEditor').innerHTML = '<p class="text-gray-500 text-sm">Select a component to edit its props</p>';
    document.getElementById('previewContainer').innerHTML = `
        <div class="text-center text-gray-500 py-20">
            <svg class="w-16 h-16 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path>
            </svg>
            <p>Select a component to see it in action</p>
        </div>
    `;
    document.getElementById('codeEditor').value = '';
}

// Render props editor
function renderPropsEditor(props) {
    const container = document.getElementById('propsEditor');
    container.innerHTML = '';

    Object.keys(props).forEach(key => {
        const prop = props[key];
        const div = document.createElement('div');
        const label = prop.label || key;
        
        if (prop.type === 'select') {
            div.innerHTML = `
                <label class="block text-sm font-medium mb-1">${label}</label>
                <select data-prop-key="${key}" class="w-full px-3 py-2 border rounded prop-input">
                    ${prop.options.map(opt => 
                        `<option value="${opt}" ${componentProps[key] === opt ? 'selected' : ''}>${opt}</option>`
                    ).join('')}
                </select>
            `;
        } else if (prop.type === 'checkbox') {
            div.innerHTML = `
                <label class="flex items-center gap-2">
                    <input type="checkbox" data-prop-key="${key}" 
                           ${componentProps[key] ? 'checked' : ''}
                           class="prop-input">
                    <span class="text-sm font-medium">${label}</span>
                </label>
            `;
        } else {
            div.innerHTML = `
                <label class="block text-sm font-medium mb-1">${label}</label>
                <input type="text" data-prop-key="${key}" 
                       value="${componentProps[key] || ''}"
                       class="w-full px-3 py-2 border rounded prop-input">
            `;
        }
        
        // Add event listener
        const input = div.querySelector('.prop-input');
        input.addEventListener('change', (e) => {
            const value = input.type === 'checkbox' ? input.checked : input.value;
            updateProp(key, value);
        });
        
        container.appendChild(div);
    });
}

// Update prop
function updateProp(key, value) {
    componentProps[key] = value;
    updatePreview();
    updateCode();
    updateJSONEditor();
}

// Update preview
function updatePreview() {
    if (!currentComponent) return;
    
    const container = document.getElementById('previewContainer');
    const template = componentTemplates[currentComponent];
    
    if (template && template.preview) {
        container.innerHTML = `
            <div class="flex items-center justify-center min-h-[400px]">
                ${template.preview(componentProps)}
            </div>
        `;
    }
}

// Update code
function updateCode() {
    if (!currentComponent || !componentTemplates[currentComponent]) return;
    
    const code = componentTemplates[currentComponent].code(componentProps);
    const codeEditor = document.getElementById('codeEditor');
    codeEditor.value = code;
    
    // Try to highlight with Prism if available
    if (window.Prism) {
        Prism.highlightElement(codeEditor);
    }
}

// Setup JSON editor
function setupJSONEditor() {
    const jsonEditorToggle = document.getElementById('jsonEditorToggle');
    const propsEditor = document.getElementById('propsEditor');
    const jsonEditor = document.getElementById('jsonEditor');
    
    if (!jsonEditorToggle || !jsonEditor) return;
    
    jsonEditorToggle.addEventListener('click', () => {
        const isJSON = jsonEditor.style.display !== 'none';
        if (isJSON) {
            // Switch to form editor
            jsonEditor.style.display = 'none';
            propsEditor.style.display = 'block';
            jsonEditorToggle.textContent = 'Switch to JSON Editor';
        } else {
            // Switch to JSON editor
            propsEditor.style.display = 'none';
            jsonEditor.style.display = 'block';
            updateJSONEditor();
            jsonEditorToggle.textContent = 'Switch to Form Editor';
        }
    });
}

// Update JSON editor
function updateJSONEditor() {
    const jsonEditor = document.getElementById('jsonEditor');
    if (jsonEditor) {
        jsonEditor.value = JSON.stringify(componentProps, null, 2);
    }
}

// Handle JSON editor changes
function handleJSONChange() {
    const jsonEditor = document.getElementById('jsonEditor');
    if (!jsonEditor) return;
    
    try {
        const newProps = JSON.parse(jsonEditor.value);
        componentProps = { ...componentProps, ...newProps };
        renderPropsEditor(componentTemplates[currentComponent].props);
        updatePreview();
        updateCode();
        showNotification('Props updated from JSON', 'success');
    } catch (error) {
        showNotification('Invalid JSON: ' + error.message, 'error');
    }
}

// Setup export buttons
function setupExportButtons() {
    // Copy code button
    const copyCodeBtn = document.getElementById('copyCodeBtn');
    if (copyCodeBtn) {
        copyCodeBtn.addEventListener('click', () => {
            const code = document.getElementById('codeEditor').value;
            navigator.clipboard.writeText(code).then(() => {
                showNotification('Code copied to clipboard!', 'success');
            });
        });
    }
    
    // Export TSX
    const exportTSXBtn = document.getElementById('exportTSXBtn');
    if (exportTSXBtn) {
        exportTSXBtn.addEventListener('click', () => {
            exportCode('tsx');
        });
    }
    
    // Export JSX
    const exportJSXBtn = document.getElementById('exportJSXBtn');
    if (exportJSXBtn) {
        exportJSXBtn.addEventListener('click', () => {
            exportCode('jsx');
        });
    }
    
    // Copy to clipboard
    const exportCopyBtn = document.getElementById('exportCopyBtn');
    if (exportCopyBtn) {
        exportCopyBtn.addEventListener('click', () => {
            const code = document.getElementById('codeEditor').value;
            navigator.clipboard.writeText(code).then(() => {
                showNotification('Code copied to clipboard!', 'success');
            });
        });
    }
}

// Export code
function exportCode(format) {
    const code = document.getElementById('codeEditor').value;
    const filename = `${currentComponent || 'component'}.${format}`;
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
    showNotification(`Exported as ${filename}`, 'success');
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 transition-all ${
        type === 'success' ? 'bg-green-500 text-white' :
        type === 'error' ? 'bg-red-500 text-white' :
        'bg-blue-500 text-white'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('opacity-0');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPlayground);
} else {
    initPlayground();
}

// Make functions available globally if needed
window.updateProp = updateProp;
window.handleJSONChange = handleJSONChange;
