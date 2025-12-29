from typing import Any, Dict, List


class BoundsFilter:
    """Keep Android elements with valid bounds that intersect the screen."""
    
    def __init__(self, screen_width: int = 0, screen_height: int = 0):
        self._screen_width = screen_width
        self._screen_height = screen_height
    
    def apply(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result = []
        for e in elements:
            bbox = e.get('bbox', {})
            if not bbox:
                continue
            
            x = bbox.get('x', 0)
            y = bbox.get('y', 0)
            w = bbox.get('width', 0)
            h = bbox.get('height', 0)
            
            if w <= 0 or h <= 0:
                continue
            
            if self._screen_width > 0 and self._screen_height > 0:
                if x + w < 0 or y + h < 0:
                    continue
                if x > self._screen_width or y > self._screen_height:
                    continue
            
            result.append(e)
        return result

