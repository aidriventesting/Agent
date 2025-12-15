from typing import Any, Dict


class WebLocatorBuilder:
    """Builds Playwright CSS selectors from element attributes."""
    
    def build(self, element: Dict[str, Any]) -> str:
        """
        Build Playwright locator combining all non-null attributes.
        
        Args:
            element: Dict with text, role, resource_id, name, class_name, type, href, aria_label, placeholder
        Returns:
            CSS/Playwright selector like 'a.sidebar-link[href*="messages"]:text-is("Messages")'
        """
        role = element.get('role', '').strip()
        text = element.get('text', '').strip()
        aria_label = element.get('aria_label', '').strip()
        placeholder = element.get('placeholder', '').strip()
        resource_id = element.get('resource_id', '').strip()
        name = element.get('name', '').strip()
        class_name = element.get('class_name', '').strip()
        css_class = element.get('css_class', '').strip()
        elem_type = element.get('type', '').strip()
        href = element.get('href', '').strip()
        
        text_cleaned = ' '.join(text.split()) if text else ''
        
        css_parts = []
        
        if class_name:
            css_parts.append(class_name)
        
        if css_class:
            first_class = css_class.split()[0]
            if first_class and not first_class.startswith('_'):
                css_parts.append(f'.{first_class}')
        
        if elem_type and elem_type not in ['text', 'submit', 'button', '']:
            css_parts.append(f'[type="{elem_type}"]')
        
        if name:
            css_parts.append(f'[name="{name}"]')
        
        if resource_id:
            if 'testid' in resource_id.lower():
                css_parts.append(f'[data-testid="{resource_id}"]')
            else:
                css_parts.append(f'[id="{resource_id}"]')
        
        if aria_label:
            css_parts.append(f'[aria-label="{aria_label}"]')
        
        if placeholder:
            css_parts.append(f'[placeholder="{placeholder}"]')
        
        if role:
            css_parts.append(f'[role="{role}"]')
        
        if href and class_name == 'a':
            if '#' in href:
                fragment = href.split('#')[-1]
                if fragment:
                    css_parts.append(f'[href*="#{fragment}"]')
            else:
                path = href.split('/')[-1] if '/' in href else ''
                if path and len(path) < 60 and '?' not in path:
                    css_parts.append(f'[href*="{path}"]')
        
        css_selector = ''.join(css_parts) if css_parts else ''
        
        if text_cleaned and len(text_cleaned) < 80:
            text_escaped = text_cleaned.replace('\\', '\\\\').replace('"', '\\"')
            if css_selector:
                return f'{css_selector}:text-is("{text_escaped}")'
            return f':text-is("{text_escaped}")'
        
        if css_selector:
            return css_selector
        
        raise AssertionError(f"Cannot build locator: no usable attributes in {element}")

