from typing import Any, Dict, List


class TextSerializer:
    """Serializes UI elements as numbered text list."""
    
    def serialize(self, elements: List[Dict[str, Any]], platform: str = "android") -> str:
        """
        Args:
            elements: List of UI element dictionaries
            platform: 'android', 'ios', or 'web'
        Returns:
            Formatted numbered text
        """
        if not elements:
            return "(no elements)"
        
        # is_mobile = platform in ("android", "ios")
        # max_items = 50 if is_mobile else 150
        max_items = 50
        
        lines = []
        for i, el in enumerate(elements[:max_items], 1):
            # if platform == "ios":
            #     line = self._ios(i, el)
            # elif platform == "android":
            #     line = self._android(i, el)
            # else:
            #     line = self._web(i, el)
            line = self._android(i, el)
            lines.append(line)
        
        return "\n".join(lines)
    
    # def _web(self, idx: int, el: Dict[str, Any]) -> str:
    #     parts = []
    #     tag = el.get('class_name', '') or el.get('tag', 'unknown')
    #     elem_type = el.get('type', '')
    #     if elem_type and elem_type not in ['text', '']:
    #         parts.append(f"<{tag} type='{elem_type}'>")
    #     else:
    #         parts.append(f"<{tag}>")
    #     
    #     if el.get("aria_label"):
    #         parts.append(f"aria-label='{el['aria_label']}'")
    #     if el.get("placeholder"):
    #         parts.append(f"placeholder='{el['placeholder']}'")
    #     if el.get("text"):
    #         parts.append(f"text='{el['text']}'")
    #     if el.get("resource_id"):
    #         parts.append(f"id='{el['resource_id']}'")
    #     if el.get("name"):
    #         parts.append(f"name='{el['name']}'")
    #     
    #     return f"{idx}. {' | '.join(parts)}"
    
    def _android(self, idx: int, el: Dict[str, Any]) -> str:
        parts = []
        class_name = el.get('class_name') or el.get('class', 'unknown')
        short_class = class_name.split('.')[-1] if '.' in class_name else class_name
        parts.append(f"[{short_class}]")
        
        if el.get("text"):
            parts.append(f"text='{el['text']}'")
        if el.get("resource_id") or el.get("resource-id"):
            parts.append(f"id='{el.get('resource_id') or el.get('resource-id')}'")
        
        content_desc = el.get("accessibility_label", '') or el.get("content_desc", '') or el.get("content-desc", '')
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
        
        return f"{idx}. {' | '.join(parts)}"
    
    # def _ios(self, idx: int, el: Dict[str, Any]) -> str:
    #     parts = []
    #     class_name = el.get('class_name', 'unknown')
    #     short_class = class_name.replace('XCUIElementType', '') if 'XCUIElementType' in class_name else class_name
    #     parts.append(f"[{short_class}]")
    #     
    #     if el.get("text"):
    #         parts.append(f"text='{el['text']}'")
    #     if el.get("resource_id"):
    #         parts.append(f"name='{el['resource_id']}'")
    #     
    #     label = el.get("accessibility_label", '') or el.get("label", '')
    #     if label:
    #         parts.append(f"label='{label}'")
    #     
    #     bbox = el.get("bbox", {})
    #     if bbox:
    #         y = bbox.get("y", 0)
    #         x = bbox.get("x", 0)
    #         w = bbox.get("width", 0)
    #         h = bbox.get("height", 0)
    #         pos = "top" if y < 400 else "middle" if y < 1200 else "bottom"
    #         side = "left" if x < 300 else "center" if x < 700 else "right"
    #         parts.append(f"pos={pos}-{side} size={w}x{h}")
    #     
    #     return f"{idx}. {' | '.join(parts)}"
