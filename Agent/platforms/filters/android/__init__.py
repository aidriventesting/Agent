from typing import Any, Dict, List
from Agent.platforms.filters.android.displayed import DisplayedFilter
from Agent.platforms.filters.android.bounds import BoundsFilter
from Agent.platforms.filters.android.interactive import InteractiveFilter
from Agent.platforms.filters.pipeline import FilterPipeline


class AndroidFilterPipeline:
    """Pre-configured filter pipeline for Android elements."""
    
    def __init__(self, screen_size: Dict[str, int] = None):
        screen_size = screen_size or {}
        self._pipeline = FilterPipeline([
            DisplayedFilter(),
            BoundsFilter(screen_size.get('width', 0), screen_size.get('height', 0)),
            InteractiveFilter(),
        ])
    
    def apply(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return self._pipeline.apply(elements)


__all__ = [
    'DisplayedFilter',
    'BoundsFilter',
    'InteractiveFilter',
    'AndroidFilterPipeline',
]

