"""
Base abstract class for UI element collectors.

All collector strategies must inherit from BaseUICollector and implement
the required methods.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseUICollector(ABC):
    """
    Abstract base class for UI element collection strategies.
    
    Each collector strategy must implement:
    1. collect_elements() - to gather UI elements from the page
    2. get_name() - to identify the strategy
    """
    
    @abstractmethod
    def collect_elements(self, max_items: int = 500) -> List[Dict[str, Any]]:
        """
        Collect interactive UI elements from the current page.
        
        Args:
            max_items: Maximum number of elements to return
            
        Returns:
            List of dictionaries with element attributes:
            {
                'text': str,          # Visible text
                'resource_id': str,   # ID or test-id
                'content_desc': str,  # aria-label or placeholder
                'label': str,         # Associated label text
                'class_name': str,    # Tag name (button, input, etc.)
                'role': str,          # ARIA role
                'name': str,          # name attribute
                'type': str,          # input type
                'href': str,          # href for links
                'clickable': bool,    # Is element clickable
                'enabled': bool,      # Is element enabled
                'bbox': dict          # Bounding box {'x': int, 'y': int, 'width': int, 'height': int}
            }
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Return the name of this collector strategy.
        
        Returns:
            String identifier (e.g., "js_query")
        """
        pass

