from typing import Any, Dict, List
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from Agent.platforms.collectors.base_collector import BaseUICollector


JS_COLLECT_ELEMENTS = """() => {
    const selectors = 'button, a, input, select, textarea, label, [type="submit"], [type="button"], [type="reset"], [type="image"], [type="checkbox"], [type="radio"], [type="file"], [type="color"], [type="date"], [type="datetime-local"], [type="email"], [type="month"], [type="number"], [type="range"], [type="search"], [type="tel"], [type="time"], [type="url"], [type="week"], [role="button"], [role="link"], [role="textbox"], [role="checkbox"], [role="radio"], [role="menuitem"], [role="tab"], [role="switch"], [role="slider"], [role="combobox"], [role="listbox"], [role="option"], [role="searchbox"], [role="spinbutton"], [role="menuitemcheckbox"], [role="menuitemradio"], [role="treeitem"], [role="gridcell"], [role="row"], [onclick], [tabindex]:not([tabindex="-1"]), [contenteditable="true"], [contenteditable=""], svg[onclick]';
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
                    className: el.className || '',
                    name: el.name || el.getAttribute('name') || '',
                    role: el.role || el.getAttribute('role') || '',
                    ariaLabel: el.ariaLabel || el.getAttribute('aria-label') || '',
                    placeholder: el.placeholder || el.getAttribute('placeholder') || '',
                    label: labelText,
                    tag: el.tagName.toLowerCase(),
                    testId: el.getAttribute('data-testid') || '',
                    type: el.getAttribute('type') || el.type || '',
                    href: el.href || el.getAttribute('href') || '',
                    bbox: {
                        x: Math.round(rect.left),
                        y: Math.round(rect.top),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height)
                    }
                });
            }
        } catch (e) {}
    });
    return results;
}"""


class JSQueryCollector(BaseUICollector):
    """Collects UI elements using JavaScript querySelector via Playwright."""
    
    def __init__(self):
        self._browser = None
    
    def _get_page(self):
        if self._browser is None:
            self._browser = BuiltIn().get_library_instance('Browser')
        return self._browser.get_page()
    
    def get_name(self) -> str:
        return "js_query"
    
    def collect_elements(self, max_items: int = 300) -> List[Dict[str, Any]]:
        """Collect interactive web elements using Playwright evaluate."""
        logger.debug(f"[{self.get_name()}] Collecting elements via Playwright...")
        candidates = []
        
        try:
            page = self._get_page()
            result = page.evaluate(JS_COLLECT_ELEMENTS)
            logger.debug(f"Playwright returned {len(result) if result else 0} elements")
            
            if result and isinstance(result, list):
                logger.debug(f"[{self.get_name()}] Found {len(result)} raw elements from page")
                for elem_data in result:
                    attrs = {
                        'text': elem_data.get('text', ''),
                        'resource_id': elem_data.get('testId') or elem_data.get('id', ''),
                        'aria_label': elem_data.get('ariaLabel', ''),
                        'placeholder': elem_data.get('placeholder', ''),
                        'css_class': elem_data.get('className', ''),
                        'label': elem_data.get('label', ''),
                        'class_name': elem_data.get('tag', ''),
                        'role': elem_data.get('role', ''),
                        'name': elem_data.get('name', ''),
                        'type': elem_data.get('type', ''),
                        'href': elem_data.get('href', ''),
                        'clickable': True,
                        'enabled': True,
                        'bbox': elem_data.get('bbox', {}),
                    }
                    candidates.append(attrs)
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
                bool(x.get('aria_label')) or bool(x.get('placeholder')),
                # PRIORITY 3: Elements with visible text
                bool(x.get('text')) and len(x.get('text', '').strip()) > 0,
                # PRIORITY 4: Elements with ID or name
                bool(x.get('resource_id')) or bool(x.get('name')),
                # PRIORITY 5 (last): Special input types (date, file, color, etc.)
                x.get('type') not in ['date', 'file', 'color', 'range', 'datetime-local', 'month', 'week', 'time']
            ),
            reverse=True
        )
        
        logger.debug(f"[{self.get_name()}] Found {len(candidates)} interactive elements after deduplication")
        return candidates[:max_items]

    def _deduplicate_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate elements based on key attributes."""
        seen = set()
        unique = []
        
        for candidate in candidates:
            key = (
                candidate.get('text', ''),
                candidate.get('resource_id', ''),
                candidate.get('aria_label', ''),
                candidate.get('placeholder', ''),
                candidate.get('name', ''),
                candidate.get('class_name', ''),
                candidate.get('css_class', ''),
                candidate.get('href', ''),
            )
            if key not in seen:
                seen.add(key)
                unique.append(candidate)
        
        return unique

