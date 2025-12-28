from typing import Any, Dict, List


class UIRenderer:
    """Renders UI elements as text for AI prompts."""
    
    def render(self, elements: List[Dict[str, Any]], platform: str = "web") -> str:
        """
        Render UI elements as numbered text list for AI prompt.
        
        Args:
            elements: List of UI element dictionaries
            platform: 'web', 'android', or 'ios'
        Returns:
            Formatted string with numbered elements
        """
        if not elements:
            return "(no UI elements found)"
        
        is_mobile = platform in ("android", "ios")
        max_items = 50 if is_mobile else 150
        
        rendered = []
        for i, el in enumerate(elements[:max_items], 1):
            if platform == "ios":
                line = self._render_ios_element(i, el)
            elif platform == "android":
                line = self._render_android_element(i, el)
            else:
                line = self._render_web_element(i, el)
            rendered.append(line)
        
        return "\n".join(rendered)
    
    def _render_web_element(self, index: int, el: Dict[str, Any]) -> str:
        """Render a single web element."""
        parts = []
        
        tag = el.get('class_name', '') or el.get('tag', 'unknown')
        elem_type = el.get('type', '')
        if elem_type and elem_type not in ['text', '']:
            parts.append(f"<{tag} type='{elem_type}'>")
        else:
            parts.append(f"<{tag}>")
        
        aria_label = el.get("aria_label", '')
        if aria_label:
            parts.append(f"aria-label='{aria_label}'")
        
        placeholder = el.get("placeholder", '')
        if placeholder:
            parts.append(f"placeholder='{placeholder}'")
        
        if el.get("text"):
            parts.append(f"text='{el['text']}'")
        
        if el.get("resource_id"):
            parts.append(f"id='{el['resource_id']}'")
        
        if el.get("name"):
            parts.append(f"name='{el['name']}'")
        
        return f"{index}. {' | '.join(parts)}"
    
    def _render_android_element(self, index: int, el: Dict[str, Any]) -> str:
        """Render a single Android element."""
        parts = []
        
        class_name = el.get('class_name', 'unknown')
        short_class = class_name.split('.')[-1] if '.' in class_name else class_name
        parts.append(f"[{short_class}]")
        
        if el.get("text"):
            parts.append(f"text='{el['text']}'")
        
        if el.get("resource_id"):
            parts.append(f"id='{el['resource_id']}'")
        
        content_desc = el.get("accessibility_label", '') or el.get("content_desc", '')
        if content_desc:
            parts.append(f"desc='{content_desc}'")
        
        bbox = el.get("bbox", {})
        if bbox:
            y = bbox.get("y", 0)
            x = bbox.get("x", 0)
            w = bbox.get("width", 0)
            h = bbox.get("height", 0)
            pos = "top" if y < 400 else "middle" if y < 1200 else "bottom"
            side = "left" if x < 300 else "center" if x < 700 else "right"
            parts.append(f"pos={pos}-{side} size={w}x{h}")
        
        return f"{index}. {' | '.join(parts)}"
    
    def _render_ios_element(self, index: int, el: Dict[str, Any]) -> str:
        """Render a single iOS element."""
        parts = []
        
        class_name = el.get('class_name', 'unknown')
        short_class = class_name.replace('XCUIElementType', '') if 'XCUIElementType' in class_name else class_name
        parts.append(f"[{short_class}]")
        
        if el.get("text"):
            parts.append(f"text='{el['text']}'")
        
        if el.get("resource_id"):
            parts.append(f"name='{el['resource_id']}'")
        
        label = el.get("accessibility_label", '') or el.get("label", '')
        if label:
            parts.append(f"label='{label}'")
        
        bbox = el.get("bbox", {})
        if bbox:
            y = bbox.get("y", 0)
            x = bbox.get("x", 0)
            w = bbox.get("width", 0)
            h = bbox.get("height", 0)
            pos = "top" if y < 400 else "middle" if y < 1200 else "bottom"
            side = "left" if x < 300 else "center" if x < 700 else "right"
            parts.append(f"pos={pos}-{side} size={w}x{h}")
        
        return f"{index}. {' | '.join(parts)}"
