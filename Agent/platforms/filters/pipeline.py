from typing import Any, Dict, List


class FilterPipeline:
    """Composable pipeline of filters."""
    
    def __init__(self, filters: List = None):
        self._filters = filters or []
    
    def add(self, f) -> 'FilterPipeline':
        self._filters.append(f)
        return self
    
    def apply(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for f in self._filters:
            elements = f.apply(elements)
        return elements

