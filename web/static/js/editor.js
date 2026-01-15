// Design Token Editor JavaScript
// Extracted from editor.html for better maintainability

let tokens = JSON.parse(localStorage.getItem('designTokens') || '{}');

// Initialize editors on page load
function initEditors() {
    // Try to load from URL parameter if available
    const urlParams = new URLSearchParams(window.location.search);
    const fileId = urlParams.get('file');
    if (fileId) {
        loadTokensFromAPI(fileId);
    } else {
        if (tokens.colors) {
            renderColorsEditor();
        }
        if (tokens.typography) {
            renderTypographyEditor();
        }
        if (tokens.spacing) {
            renderSpacingEditor();
        }
        updatePreview();
    }
}

// Load tokens from API
async function loadTokensFromAPI(fileId) {
    try {
        const response = await fetch(`/api/tokens/${fileId}`);
        const data = await response.json();
        if (data.success && data.tokens) {
            tokens = data.tokens;
            renderColorsEditor();
            renderTypographyEditor();
            renderSpacingEditor();
            updatePreview();
        }
    } catch (error) {
        console.error('Error loading tokens:', error);
        showNotification('Error loading tokens from file', 'error');
    }
}

// Render color editor with drag-and-drop
function renderColorsEditor() {
    const container = document.getElementById('colorsEditor');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!tokens.colors || tokens.colors.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-sm">No colors found. Generate a design system first.</p>';
        return;
    }
    
    // Group colors by role
    const colorsByRole = {};
    tokens.colors.forEach(color => {
        const role = color.role || 'other';
        if (!colorsByRole[role]) {
            colorsByRole[role] = [];
        }
        colorsByRole[role].push(color);
    });
    
    // Render by role
    Object.keys(colorsByRole).forEach(role => {
        const roleDiv = document.createElement('div');
        roleDiv.className = 'mb-6';
        roleDiv.innerHTML = `<h3 class="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wide">${role}</h3>`;
        const roleContainer = document.createElement('div');
        roleContainer.className = 'space-y-3';
        roleContainer.setAttribute('data-role', role);
        
        colorsByRole[role].forEach((color, index) => {
            const div = createColorEditorItem(color, role);
            roleContainer.appendChild(div);
            checkContrast(color.name, color.value);
        });
        
        roleDiv.appendChild(roleContainer);
        container.appendChild(roleDiv);
    });
}

// Create a color editor item
function createColorEditorItem(color, role) {
    const div = document.createElement('div');
    div.className = 'flex items-center gap-4 p-3 border rounded-lg hover:bg-gray-50 transition-all cursor-move';
    div.setAttribute('draggable', 'true');
    div.setAttribute('data-color-name', color.name);
    div.setAttribute('data-role', role);
    
    // Calculate text color for contrast (use getContrastColor from color-utils.js if available)
    const getTextColor = (hex) => {
        if (typeof getContrastColor !== 'undefined') {
            return getContrastColor(hex);
        }
        // Fallback calculation
        const rgb = hexToRgb(hex);
        const brightness = (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
        return brightness > 128 ? '#000000' : '#ffffff';
    };
    const textColor = getTextColor(color.value);
    
    div.innerHTML = `
        <div class="flex-shrink-0 cursor-move" title="Drag to reorder">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"></path>
            </svg>
        </div>
        <div class="flex-1">
            <label class="block text-sm font-medium mb-1">${color.name}</label>
            <div class="flex gap-2">
                <input type="color" value="${color.value}" 
                    data-color-name="${color.name}"
                    class="w-16 h-10 rounded border cursor-pointer color-picker">
                <input type="text" value="${color.value}"
                    data-color-name="${color.name}"
                    class="flex-1 px-3 py-2 border rounded font-mono text-sm color-input"
                    style="background-color: ${color.value}; color: ${textColor};">
            </div>
        </div>
        <div class="color-preview flex-shrink-0" style="background: ${color.value}; min-width: 80px; height: 60px; border-radius: 8px; border: 2px solid #e5e7eb;"></div>
        <div id="contrast-${color.name}" class="flex-shrink-0"></div>
    `;
    
    // Add event listeners
    const colorPicker = div.querySelector('.color-picker');
    const colorInput = div.querySelector('.color-input');
    
    colorPicker.addEventListener('change', (e) => {
        updateColor(color.name, e.target.value);
        colorInput.value = e.target.value;
        // Update input background color
        const getTextColor = (hex) => {
            if (typeof getContrastColor !== 'undefined') {
                return getContrastColor(hex);
            }
            const rgb = hexToRgb(hex);
            const brightness = (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
            return brightness > 128 ? '#000000' : '#ffffff';
        };
        const textColor = getTextColor(e.target.value);
        colorInput.style.backgroundColor = e.target.value;
        colorInput.style.color = textColor;
    });
    
    colorInput.addEventListener('change', (e) => {
        const value = e.target.value;
        if (isValidHex(value)) {
            updateColor(color.name, value);
            colorPicker.value = value;
            // Update input background color
            const textColor = typeof getContrastColor !== 'undefined' 
                ? getContrastColor(value)
                : (() => {
                    const rgb = hexToRgb(value);
                    const brightness = (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
                    return brightness > 128 ? '#000000' : '#ffffff';
                })();
            e.target.style.backgroundColor = value;
            e.target.style.color = textColor;
        } else {
            showNotification('Invalid hex color', 'error');
            e.target.value = color.value;
        }
    });
    
    // Also update on input for real-time feedback
    colorInput.addEventListener('input', (e) => {
        const value = e.target.value;
        if (isValidHex(value)) {
            const textColor = typeof getContrastColor !== 'undefined' 
                ? getContrastColor(value)
                : (() => {
                    const rgb = hexToRgb(value);
                    const brightness = (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
                    return brightness > 128 ? '#000000' : '#ffffff';
                })();
            e.target.style.backgroundColor = value;
            e.target.style.color = textColor;
        }
    });
    
    // Drag and drop handlers
    div.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', color.name);
        e.dataTransfer.setData('text/role', role);
        div.classList.add('opacity-50', 'border-indigo-400');
    });
    
    div.addEventListener('dragend', () => {
        div.classList.remove('opacity-50', 'border-indigo-400');
    });
    
    div.addEventListener('dragover', (e) => {
        e.preventDefault();
        div.classList.add('border-indigo-400', 'bg-indigo-50');
    });
    
    div.addEventListener('dragleave', () => {
        div.classList.remove('border-indigo-400', 'bg-indigo-50');
    });
    
    div.addEventListener('drop', (e) => {
        e.preventDefault();
        div.classList.remove('border-indigo-400', 'bg-indigo-50');
        const draggedName = e.dataTransfer.getData('text/plain');
        const draggedRole = e.dataTransfer.getData('text/role');
        if (draggedName !== color.name && draggedRole === role) {
            reorderColor(draggedName, color.name, role);
        }
    });
    
    return div;
}

// Reorder colors
function reorderColor(draggedName, targetName, role) {
    const roleColors = tokens.colors.filter(c => (c.role || 'other') === role);
    const draggedIndex = roleColors.findIndex(c => c.name === draggedName);
    const targetIndex = roleColors.findIndex(c => c.name === targetName);
    
    if (draggedIndex !== -1 && targetIndex !== -1) {
        const [dragged] = roleColors.splice(draggedIndex, 1);
        roleColors.splice(targetIndex, 0, dragged);
        
        // Update tokens.colors order
        const otherColors = tokens.colors.filter(c => (c.role || 'other') !== role);
        tokens.colors = [...otherColors, ...roleColors];
        
        renderColorsEditor();
        saveTokens();
        showNotification('Color order updated', 'success');
    }
}

// Render typography editor
function renderTypographyEditor() {
    const container = document.getElementById('typographyEditor');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!tokens.typography || tokens.typography.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-sm">No typography tokens found.</p>';
        return;
    }
    
    tokens.typography.forEach(typo => {
        const div = document.createElement('div');
        div.className = 'border rounded-lg p-4 hover:shadow-md transition-shadow bg-white';
        div.innerHTML = `
            <div class="flex items-start justify-between mb-3">
                <div>
                    <label class="block text-sm font-medium mb-1">${typo.name}</label>
                    <div class="text-xs text-gray-500">${typo.role || 'general'}</div>
                </div>
            </div>
            <div class="mb-4 p-4 bg-gray-50 rounded-lg border-2 border-dashed" 
                 style="font-family: ${typo.family}; font-size: ${typo.size}; font-weight: ${typo.weight}; line-height: ${typo.line_height};"
                 id="typo-preview-${typo.name}">
                The quick brown fox jumps over the lazy dog
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="text-xs text-gray-600 mb-1 block">Font Family</label>
                    <input type="text" value="${typo.family}" 
                        data-typo-name="${typo.name}"
                        data-typo-prop="family"
                        class="w-full px-3 py-2 border rounded text-sm typo-input">
                </div>
                <div>
                    <label class="text-xs text-gray-600 mb-1 block">Size</label>
                    <input type="text" value="${typo.size}" 
                        data-typo-name="${typo.name}"
                        data-typo-prop="size"
                        class="w-full px-3 py-2 border rounded text-sm typo-input">
                </div>
                <div>
                    <label class="text-xs text-gray-600 mb-1 block">Weight</label>
                    <select data-typo-name="${typo.name}"
                        data-typo-prop="weight"
                        class="w-full px-3 py-2 border rounded text-sm typo-input">
                        <option value="100" ${typo.weight == 100 ? 'selected' : ''}>100 - Thin</option>
                        <option value="200" ${typo.weight == 200 ? 'selected' : ''}>200 - Extra Light</option>
                        <option value="300" ${typo.weight == 300 ? 'selected' : ''}>300 - Light</option>
                        <option value="400" ${typo.weight == 400 ? 'selected' : ''}>400 - Regular</option>
                        <option value="500" ${typo.weight == 500 ? 'selected' : ''}>500 - Medium</option>
                        <option value="600" ${typo.weight == 600 ? 'selected' : ''}>600 - Semi Bold</option>
                        <option value="700" ${typo.weight == 700 ? 'selected' : ''}>700 - Bold</option>
                        <option value="800" ${typo.weight == 800 ? 'selected' : ''}>800 - Extra Bold</option>
                        <option value="900" ${typo.weight == 900 ? 'selected' : ''}>900 - Black</option>
                    </select>
                </div>
                <div>
                    <label class="text-xs text-gray-600 mb-1 block">Line Height</label>
                    <input type="text" value="${typo.line_height}" 
                        data-typo-name="${typo.name}"
                        data-typo-prop="line_height"
                        class="w-full px-3 py-2 border rounded text-sm typo-input">
                </div>
            </div>
        `;
        
        // Add event listeners
        div.querySelectorAll('.typo-input').forEach(input => {
            input.addEventListener('change', (e) => {
                const name = e.target.getAttribute('data-typo-name');
                const prop = e.target.getAttribute('data-typo-prop');
                const value = e.target.value;
                updateTypography(name, prop, value);
            });
        });
        
        container.appendChild(div);
    });
}

// Render spacing editor
function renderSpacingEditor() {
    const container = document.getElementById('spacingEditor');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!tokens.spacing || tokens.spacing.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-sm">No spacing tokens found.</p>';
        return;
    }
    
    tokens.spacing.forEach(space => {
        const valueNum = parseInt(space.value) || 0;
        const div = document.createElement('div');
        div.className = 'border rounded-lg p-4 hover:shadow-md transition-shadow bg-white';
        div.innerHTML = `
            <div class="flex items-center justify-between mb-3">
                <div>
                    <label class="block text-sm font-medium">${space.name}</label>
                    <div class="text-xs text-gray-500">Scale: ${space.scale || 'N/A'}</div>
                </div>
                <div class="text-sm font-mono text-gray-600">${space.value}</div>
            </div>
            <div class="flex items-center gap-4">
                <input type="range" min="0" max="128" value="${valueNum}" 
                    data-spacing-name="${space.name}"
                    class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer spacing-slider">
                <input type="text" value="${space.value}" 
                    data-spacing-name="${space.name}"
                    class="w-24 px-3 py-2 border rounded text-sm font-mono text-center spacing-input">
            </div>
            <div class="mt-3 flex items-center gap-2">
                <div class="text-xs text-gray-500">Visual:</div>
                <div class="flex-1 h-8 bg-indigo-100 rounded border-2 border-indigo-300 flex items-center justify-center spacing-visual"
                     data-spacing-name="${space.name}"
                     style="width: ${Math.min(valueNum, 200)}px; min-width: 20px;">
                    <div class="text-xs text-indigo-700 font-medium">${space.name}</div>
                </div>
            </div>
        `;
        
        // Add event listeners
        const slider = div.querySelector('.spacing-slider');
        const input = div.querySelector('.spacing-input');
        const visual = div.querySelector('.spacing-visual');
        
        slider.addEventListener('input', (e) => {
            const value = e.target.value + 'px';
            input.value = value;
            visual.style.width = `${Math.min(parseInt(e.target.value), 200)}px`;
            updateSpacing(space.name, value);
        });
        
        input.addEventListener('change', (e) => {
            const value = e.target.value;
            updateSpacing(space.name, value);
            const numValue = parseInt(value) || 0;
            slider.value = numValue;
            visual.style.width = `${Math.min(numValue, 200)}px`;
        });
        
        container.appendChild(div);
    });
}

// Update color
function updateColor(name, value) {
    const color = tokens.colors.find(c => c.name === name);
    if (color) {
        color.value = value;
        checkContrast(name, value);
        updatePreview();
        saveTokens();
        showNotification(`Updated ${name}`, 'success');
        
        // Update input field background color if it exists
        const colorInput = document.querySelector(`input.color-input[data-color-name="${name}"]`);
        if (colorInput && isValidHex(value)) {
            // Use getContrastColor from color-utils.js if available, otherwise calculate inline
            const getTextColor = (hex) => {
                if (typeof getContrastColor !== 'undefined') {
                    return getContrastColor(hex);
                }
                const rgb = hexToRgb(hex);
                const brightness = (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
                return brightness > 128 ? '#000000' : '#ffffff';
            };
            const textColor = getTextColor(value);
            colorInput.style.backgroundColor = value;
            colorInput.style.color = textColor;
        }
    }
}

// Update typography
function updateTypography(name, property, value) {
    const typo = tokens.typography.find(t => t.name === name);
    if (typo) {
        typo[property] = property === 'weight' || property === 'line_height' ? 
            (property === 'weight' ? parseInt(value) : parseFloat(value)) : value;
        
        // Update live preview
        const preview = document.getElementById(`typo-preview-${name}`);
        if (preview) {
            const styleProp = property === 'family' ? 'fontFamily' : 
                             property === 'size' ? 'fontSize' :
                             property === 'weight' ? 'fontWeight' :
                             'lineHeight';
            preview.style[styleProp] = value;
        }
        updatePreview();
        saveTokens();
        showNotification(`Updated ${name} typography`, 'success');
    }
}

// Update spacing
function updateSpacing(name, value) {
    const space = tokens.spacing.find(s => s.name === name);
    if (space) {
        space.value = value;
        updatePreview();
        saveTokens();
        showNotification(`Updated ${name} spacing`, 'success');
    }
}

// Check contrast ratio
function checkContrast(colorName, hex) {
    const contrast = getContrastRatio(hex, '#ffffff');
    const badge = document.getElementById(`contrast-${colorName}`);
    if (badge) {
        let className = 'contrast-fail';
        let text = 'Fail';
        if (contrast >= 7) {
            className = 'contrast-aaa';
            text = 'AAA';
        } else if (contrast >= 4.5) {
            className = 'contrast-aa';
            text = 'AA';
        }
        badge.innerHTML = `<span class="contrast-badge ${className}">${text} (${contrast.toFixed(1)}:1)</span>`;
    }
}

// Get contrast ratio
function getContrastRatio(color1, color2) {
    const l1 = getLuminance(color1);
    const l2 = getLuminance(color2);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
}

// Get luminance
function getLuminance(hex) {
    const rgb = hexToRgb(hex);
    const [r, g, b] = [rgb.r, rgb.g, rgb.b].map(val => {
        val = val / 255;
        return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

// Convert hex to RGB
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : { r: 0, g: 0, b: 0 };
}

// Validate hex color
function isValidHex(hex) {
    return /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(hex);
}

// Update preview
function updatePreview() {
    const root = document.documentElement;
    if (tokens.colors) {
        tokens.colors.forEach(color => {
            root.style.setProperty(`--color-${color.name}`, color.value);
        });
    }
    if (tokens.typography) {
        tokens.typography.forEach(typo => {
            root.style.setProperty(`--font-${typo.name}`, typo.family);
        });
    }
    
    // Update preview panel
    updatePreviewPanel();
}

// Update preview panel with better examples
function updatePreviewPanel() {
    const preview = document.getElementById('livePreview');
    if (!preview) return;
    
    const primaryColor = tokens.colors?.find(c => c.name.includes('primary-500') || c.name.includes('primary-450'))?.value || '#3b82f6';
    const neutralColor = tokens.colors?.find(c => c.name.includes('neutral-100') || c.name.includes('neutral-50'))?.value || '#f3f4f6';
    
    preview.innerHTML = `
        <div class="space-y-4">
            <div class="p-4 border rounded-lg" style="background: ${neutralColor};">
                <h3 class="text-lg font-semibold mb-2" style="color: ${primaryColor};">Sample Heading</h3>
                <p class="text-sm mb-4">This is sample body text to preview your typography settings.</p>
                <button class="px-4 py-2 rounded text-white transition-colors hover:opacity-90" 
                        style="background: ${primaryColor};">
                    Primary Button
                </button>
            </div>
            <div class="p-4 border rounded-lg bg-white">
                <h4 class="text-sm font-semibold mb-2">Color Palette Preview</h4>
                <div class="grid grid-cols-3 gap-2">
                    ${tokens.colors?.slice(0, 6).map(c => `
                        <div class="h-12 rounded border" style="background: ${c.value};" 
                             title="${c.name}: ${c.value}"></div>
                    `).join('') || ''}
                </div>
            </div>
        </div>
    `;
}

// Save tokens
function saveTokens() {
    localStorage.setItem('designTokens', JSON.stringify(tokens));
}

// Export tokens
function exportTokens() {
    const dataStr = JSON.stringify(tokens, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'design-tokens.json';
    link.click();
    URL.revokeObjectURL(url);
    showNotification('Tokens exported successfully', 'success');
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 transition-all ${
        type === 'success' ? 'bg-green-500 text-white' :
        type === 'error' ? 'bg-red-500 text-white' :
        'bg-blue-500 text-white'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('opacity-0');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEditors);
} else {
    initEditors();
}

// Export button handler
document.addEventListener('DOMContentLoaded', () => {
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportTokens);
    }
});
