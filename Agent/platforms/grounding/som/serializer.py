from typing import Any, Dict, List
import json


class SomSerializer:
    """
    Serializes UI elements as text or JSON for SoM prompts.
    
    Args:
        platform: "android" (implemented), "ios"/"web" (future)
        screen_width: Screen width in pixels
        screen_height: Screen height in pixels
    """
    
    def __init__(self, platform: str = "android", screen_width: int = 1080, screen_height: int = 1920):
        self.platform = platform
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def serialize(
        self, 
        elements: List[Dict[str, Any]], 
        format: str = "compact",
        output_type: str = "text"
    ) -> str:
        """
        Args:
            elements: List of UI elements
            format: "compact", "detailed", "minimal" (for text mode)
            output_type: "text" or "json"
        Returns:
            Formatted string
        """
        if output_type == "json":
            return self._to_json(elements)
        else:
            return self._to_text(elements, format)
    
    def _to_text(self, elements: List[Dict[str, Any]], format: str) -> str:
        if not elements:
            return "(no elements)"
        
        lines = []
        for idx, elem in enumerate(elements, start=1):
            if format == "minimal":
                line = self._minimal(idx, elem)
            elif format == "detailed":
                line = self._detailed(idx, elem)
            else:
                line = self._compact(idx, elem)
            lines.append(line)
        
        return "\n".join(lines)
    
    def _minimal(self, idx: int, elem: Dict[str, Any]) -> str:
        text = self._get_text(elem)
        return f"[{idx}] {text}" if text else f"[{idx}] (no text)"
    
    def _compact(self, idx: int, elem: Dict[str, Any]) -> str:
        class_name = elem.get("class_name") or elem.get("class", "")
        short_class = class_name.split('.')[-1] if '.' in class_name else class_name
        text = self._get_text(elem)
        position = self._get_position(elem.get("bbox", {}))
        return f"[{idx}] {short_class}: {text} @{position}"
    
    def _detailed(self, idx: int, elem: Dict[str, Any]) -> str:
        parts = []
        class_name = elem.get("class_name") or elem.get("class", "")
        short_class = class_name.split('.')[-1] if '.' in class_name else class_name
        parts.append(f"[{idx}] {short_class}")
        
        text = self._get_text(elem)
        if text:
            parts.append(f"text='{text}'")
        
        resource_id = self._get_resource_id(elem)
        if resource_id:
            parts.append(f"id='{resource_id}'")
        
        content_desc = self._get_content_desc(elem)
        if content_desc:
            parts.append(f"desc='{content_desc}'")
        
        bbox = elem.get("bbox", {})
        if bbox:
            position = self._get_position(bbox)
            w = bbox.get("width", 0)
            h = bbox.get("height", 0)
            parts.append(f"pos={position} size={w}x{h}")
        
        return " | ".join(parts)
    
    def _to_json(self, elements: List[Dict[str, Any]]) -> str:
        if self.platform != "android":
            raise NotImplementedError(f"JSON not implemented for: {self.platform}")
        
        boxes = []
        for idx, elem in enumerate(elements, start=1):
            bbox_norm = elem.get("bbox_normalized", {})
            if not bbox_norm:
                bbox_norm = self._normalize(elem.get("bbox", {}))
            
            boxes.append({
                "mark_id": idx,
                "class_name": elem.get("class_name") or elem.get("class", ""),
                "text": self._get_text(elem) or "",
                "resource_id": self._get_resource_id(elem) or "",
                "content_desc": self._get_content_desc(elem) or "",
                "bbox": bbox_norm
            })
        
        return json.dumps({
            "screen": {"width": self.screen_width, "height": self.screen_height},
            "som_version": "1.0",
            "boxes": boxes
        }, indent=2, ensure_ascii=False)
    
    def _normalize(self, bbox: Dict[str, int]) -> Dict[str, float]:
        if not bbox or self.screen_width <= 0 or self.screen_height <= 0:
            return {}
        return {
            'x': round(bbox.get('x', 0) / self.screen_width, 4),
            'y': round(bbox.get('y', 0) / self.screen_height, 4),
            'width': round(bbox.get('width', 0) / self.screen_width, 4),
            'height': round(bbox.get('height', 0) / self.screen_height, 4),
        }
    
    def _get_text(self, elem: Dict[str, Any]) -> str:
        text = elem.get("text", "")
        if isinstance(text, str):
            return text.replace("\n", " ").strip()[:40]
        return ""
    
    def _get_resource_id(self, elem: Dict[str, Any]) -> str:
        return elem.get("resource_id") or elem.get("resource-id", "")
    
    def _get_content_desc(self, elem: Dict[str, Any]) -> str:
        return elem.get("content_desc") or elem.get("content-desc", "")
    
    def _get_position(self, bbox: Dict[str, int]) -> str:
        if not bbox:
            return "unknown"
        y = bbox.get("y", 0)
        x = bbox.get("x", 0)
        pos = "top" if y < 400 else "mid" if y < 1200 else "bot"
        side = "L" if x < 300 else "C" if x < 700 else "R"
        return f"{pos}-{side}"

