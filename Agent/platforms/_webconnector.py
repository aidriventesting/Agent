from typing import Any, Dict, List
import base64
import os
import tempfile
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class WebConnectorRF:
    """Playwright connector using Robot Framework Browser library keywords."""

    def __init__(self) -> None:
        logger.info("WebConnectorRF initialized - using Browser library keywords")

    def get_platform(self) -> str:
        return "web"

    def collect_ui_candidates(self, max_items: int = 150) -> List[Dict[str, Any]]:
        """Collect interactive web elements using Browser library keywords."""
        logger.info("Collecting web UI candidates via Browser keywords...")
        candidates = []
        
        comprehensive_js = """(function() {
    const selectors = 'button, a, input, select, textarea, [role="button"], [role="link"], [role="textbox"], [type="submit"], [type="button"]';
    const elements = document.querySelectorAll(selectors);
    const results = [];
    elements.forEach(el => {
        try {
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            const isVisible = rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none' && style.opacity !== '0';
            if (isVisible && !el.disabled && !el.hasAttribute('disabled')) {
                let labelText = '';
                const label = el.closest('label') || document.querySelector('label[for="' + el.id + '"]');
                if (label) {
                    labelText = label.textContent.replace(el.textContent || '', '').trim().substring(0, 50);
                }
                results.push({
                    text: (el.textContent || el.value || '').trim().substring(0, 100),
                    id: el.id || '',
                    name: el.name || el.getAttribute('name') || '',
                    role: el.role || el.getAttribute('role') || '',
                    ariaLabel: el.ariaLabel || el.getAttribute('aria-label') || '',
                    placeholder: el.placeholder || el.getAttribute('placeholder') || '',
                    label: labelText,
                    tag: el.tagName.toLowerCase(),
                    testId: el.getAttribute('data-testid') || '',
                    type: el.getAttribute('type') || el.type || '',
                    href: el.href || el.getAttribute('href') || ''
                });
            }
        } catch (e) {}
    });
    return results;
})()"""
        
        try:
            logger.debug("Executing JavaScript to collect elements...")
            result = BuiltIn().run_keyword('Evaluate JavaScript', 'body >> nth=0', comprehensive_js)
            logger.debug(f"JavaScript returned type: {type(result)}, length: {len(result) if result else 0}")
            
            if result and isinstance(result, list):
                logger.info(f"Found {len(result)} raw elements from page")
                for elem_data in result:
                    attrs = {
                        'text': elem_data.get('text', ''),
                        'resource_id': elem_data.get('testId') or elem_data.get('id', ''),
                        'content_desc': elem_data.get('ariaLabel') or elem_data.get('placeholder', ''),
                        'label': elem_data.get('label', ''),
                        'class_name': elem_data.get('tag', ''),
                        'role': elem_data.get('role', ''),
                        'name': elem_data.get('name', ''),
                        'type': elem_data.get('type', ''),
                        'href': elem_data.get('href', ''),
                        'clickable': True,
                        'enabled': True,
                    }
                    candidates.append(attrs)
                    logger.debug(f"Added element: {attrs.get('class_name')} - text: '{attrs.get('text')[:30]}...'")
            else:
                logger.warn(f"JavaScript did not return expected list: {type(result)}")
                
        except Exception as e:
            logger.error(f"Failed to collect elements via JavaScript: {e}")
            import traceback
            logger.debug(f"Traceback: {traceback.format_exc()}")
        
        candidates = self._deduplicate_candidates(candidates)
        candidates.sort(
            key=lambda x: (
                # PRIORITY 1: Input fields (text, search, email, etc.) - CRITICAL for forms
                x.get('class_name') in ['input', 'textarea'],
                # PRIORITY 2: Elements with placeholder/aria-label (empty inputs)
                bool(x.get('content_desc')),
                # PRIORITY 3: Elements with visible text
                bool(x.get('text')) and len(x.get('text', '').strip()) > 0,
                # PRIORITY 4: Elements with ID or name
                bool(x.get('resource_id')) or bool(x.get('name')),
                # PRIORITY 5 (last): Special input types (date, file, color, etc.)
                x.get('type') not in ['date', 'file', 'color', 'range', 'datetime-local', 'month', 'week', 'time']
            ),
            reverse=True
        )
        
        logger.info(f"Platform: web, Found {len(candidates)} interactive elements after deduplication")
        return candidates[:max_items]

    def _deduplicate_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate elements based on key attributes."""
        seen = set()
        unique = []
        
        for candidate in candidates:
            key = (
                candidate.get('text', ''),
                candidate.get('resource_id', ''),
                candidate.get('content_desc', ''),
                candidate.get('name', ''),
                candidate.get('class_name', '')
            )
            if key not in seen:
                seen.add(key)
                unique.append(candidate)
        
        return unique

    def build_locator_from_element(self, element: Dict[str, Any]) -> str:
        """Build Playwright locator following best practices: role > label > test-id > name > text > css."""
        role = element.get('role')
        text = element.get('text', '')
        content_desc = element.get('content_desc')
        resource_id = element.get('resource_id')
        name = element.get('name')
        class_name = element.get('class_name')
        elem_type = element.get('type', '')
        href = element.get('href', '')
        
        # Clean text: remove newlines, tabs, and multiple spaces
        text_cleaned = ' '.join(text.split()) if text else ''
        
        if role and (text_cleaned or content_desc):
            accessible_name = content_desc or text_cleaned
            return f'role={role}[name="{accessible_name}"]'
        
        if role:
            return f'role={role}'
        
        if content_desc:
            return f'[aria-label="{content_desc}"]'
        
        if resource_id and 'testid' in resource_id.lower():
            return f'[data-testid="{resource_id}"]'
        
        if resource_id:
            return f'#{resource_id}'
        
        # Handle select and textarea elements first (they should be selected by name, not by their text content)
        if class_name == 'select' and name:
            return f'select[name="{name}"]'
        
        if class_name == 'textarea' and name:
            return f'textarea[name="{name}"]'
        
        # For inputs with type and name, use more specific locator
        if class_name == 'input' and elem_type and name:
            if elem_type not in ['text', 'submit', 'button']:
                return f'input[type="{elem_type}"][name="{name}"]'
        
        if name and not text_cleaned:
            if class_name:
                return f'{class_name}[name="{name}"]'
            return f'[name="{name}"]'
        
        # PRIORITY: For links (<a>), use href before text (more stable)
        if class_name == 'a' and href:
            # Extract fragment (#section) from full URL if present
            if '#' in href:
                fragment_part = href.split('#')[-1]
                # Only use fragment if it's not empty (avoid href ending with just #)
                if fragment_part:
                    fragment = '#' + fragment_part
                    return f'a[href*="{fragment}"]'
                # If fragment is empty (href ends with #), skip and use text instead
            # Use full href if it starts with # (already a fragment) - but not if it's just '#'
            elif href.startswith('#') and len(href) > 1:
                return f'a[href="{href}"]'
            # For absolute URLs without fragment, use if short enough
            elif href.startswith('http') and len(href) < 150:
                return f'a[href="{href}"]'
        
        # Use cleaned text for locator (now works even if original had \n or \t)
        if text_cleaned and len(text_cleaned) < 100:
            text_escaped = text_cleaned.replace('\\', '\\\\').replace('"', '\\"')
            if class_name:
                return f'{class_name} >> text="{text_escaped}"'
            return f'text="{text_escaped}"'
        
        if name:
            if class_name:
                return f'{class_name}[name="{name}"]'
            return f'[name="{name}"]'
        
        if class_name:
            if elem_type and elem_type not in ['text', 'submit', 'button']:
                return f'{class_name}[type="{elem_type}"]'
            
            # NEVER return just a tag alone - too ambiguous!
            # Try to use partial text if available
            if text_cleaned:
                # Use first 30 chars of text
                text_short = text_cleaned[:30].replace('\\', '\\\\').replace('"', '\\"')
                return f'{class_name} >> text="{text_short}"'
            # Last resort: raise error with details
            raise AssertionError(
                f"Cannot build unique locator for element: {element}. "
                f"Element has class '{class_name}' but no unique attributes (no id, name, or usable text)."
            )
        
        raise AssertionError("Cannot build locator: element has no usable attributes")

    def get_screenshot_base64(self) -> str:
        """Capture screenshot as base64."""
        try:
            # Browser library: Take Screenshot with selector (fullPage for whole page)
            # Returns bytes, we need base64
            screenshot_bytes = BuiltIn().run_keyword('Take Screenshot', 'fullPage')
            if isinstance(screenshot_bytes, bytes):
                return base64.b64encode(screenshot_bytes).decode('utf-8')
            # If it's already a path, read the file
            elif isinstance(screenshot_bytes, str):
                with open(screenshot_bytes, 'rb') as f:
                    return base64.b64encode(f.read()).decode('utf-8')
            else:
                logger.error(f"Unexpected screenshot type: {type(screenshot_bytes)}")
                return ""
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return ""

    def embed_image_to_log(self, base64_screenshot: str, width: int = 400) -> None:
        """Embed screenshot into Robot Framework log."""
        msg = f"</td></tr><tr><td colspan=\"3\"><img src=\"data:image/png;base64, {base64_screenshot}\" width=\"{width}\"></td></tr>"
        logger.info(msg, html=True, also_console=False)

    def render_ui_for_prompt(self, ui_elements: List[Dict[str, Any]]) -> str:
        """Render UI elements as numbered text list for AI prompt."""
        if not ui_elements:
            return "(no UI elements found)"
        
        rendered = []
        # Web pages can have many elements, so we allow more than mobile (150 vs 20)
        for i, el in enumerate(ui_elements[:150], 1):
            parts = []
            

            tag = el.get('class_name', 'unknown')
            elem_type = el.get('type', '')
            if elem_type and elem_type not in ['text', '']:
                parts.append(f"<{tag} type='{elem_type}'>")
            else:
                parts.append(f"<{tag}>")
            
            # CRITICAL: Show placeholder/aria-label FIRST for inputs (they identify empty fields)
            content_desc = el.get("content_desc", '')
            if content_desc:
                parts.append(f"placeholder='{content_desc}'")
            
            if el.get("text"):
                parts.append(f"text='{el['text']}'")
            if el.get("resource_id"):
                parts.append(f"id='{el['resource_id']}'")
            if el.get("name"):
                parts.append(f"name='{el['name']}'")
            
            line = f"{i}. {' | '.join(parts)}"
            rendered.append(line)
        
        return "\n".join(rendered)

