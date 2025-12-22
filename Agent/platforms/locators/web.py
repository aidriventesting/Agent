from typing import Any, Dict
import re


class WebLocatorBuilder:
    """Builds Playwright selectors from element attributes."""
    
    def build(self, element: Dict[str, Any]) -> str:
        """
        Args:
            element: {text, role, resource_id, name, class_name, type, href, aria_label, placeholder}
        Returns:
            Complete CSS selector combining all available attributes
        """
        resource_id = element.get('resource_id', '').strip()
        name = element.get('name', '').strip()
        class_name = element.get('class_name', '').strip()
        css_class = element.get('css_class', '').strip()
        text = element.get('text', '').strip()
        placeholder = element.get('placeholder', '').strip()
        aria_label = element.get('aria_label', '').strip()
        role = element.get('role', '').strip()
        elem_type = element.get('type', '').strip()
        href = element.get('href', '').strip()
        
        text_cleaned = ' '.join(text.split()) if text else ''
        
        css_parts = []
        
        if class_name:
            css_parts.append(class_name)
        
        if css_class:
            first_class = css_class.split()[0]
            if first_class and not first_class.startswith('_') and not re.search(r'\d{5,}', first_class):
                css_parts.append(f'.{first_class}')
        
        if resource_id and not resource_id.startswith('_') and len(resource_id) >= 3:
            if 'testid' in resource_id.lower():
                css_parts.append(f'[data-testid="{self._escape(resource_id)}"]')
            else:
                css_parts.append(f'#{resource_id}')
        
        if elem_type and elem_type not in ['text', 'submit', 'button', '']:
            css_parts.append(f'[type="{elem_type}"]')
        
        if name and len(name) < 50:
            css_parts.append(f'[name="{self._escape(name)}"]')
        
        if placeholder and len(placeholder) < 50:
            css_parts.append(f'[placeholder="{self._escape(placeholder)}"]')
        
        if aria_label and len(aria_label) < 50:
            css_parts.append(f'[aria-label="{self._escape(aria_label)}"]')
        
        if role:
            css_parts.append(f'[role="{role}"]')
        
        if href and class_name == 'a':
            if '#' in href:
                fragment = href.split('#')[-1]
                if fragment and len(fragment) < 30:
                    css_parts.append(f'[href*="#{fragment}"]')
            else:
                path = href.split('/')[-1].split('?')[0] if '/' in href else ''
                if path and len(path) < 40 and path not in ['', 'index.html', 'index.php']:
                    css_parts.append(f'[href*="{path}"]')
        
        css_selector = ''.join(css_parts) if css_parts else ''
        
        if text_cleaned and len(text_cleaned) < 60 and len(text_cleaned) > 1:
            if css_selector:
                return f'{css_selector}:has-text("{self._escape(text_cleaned)}") >> visible=true'
            return f'text={text_cleaned} >> visible=true'
        
        if css_selector:
            return f'{css_selector} >> visible=true'
        
        raise AssertionError(f"Cannot build locator: no usable attributes in {element}")
    
    def _escape(self, value: str) -> str:
        return value.replace('\\', '\\\\').replace('"', '\\"')
