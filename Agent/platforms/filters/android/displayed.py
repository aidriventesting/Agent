from typing import Any, Dict, List


class DisplayedFilter:
    """Keep only displayed Android elements."""
    
    def apply(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [e for e in elements if e.get('displayed') == 'true']

