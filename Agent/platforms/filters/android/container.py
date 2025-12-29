from typing import Any, Dict, List, Set


class ContainerFilter:
    """Remove containers that have interactive children in the list"""
    
    CONTAINER_CLASSES = {
        'RecyclerView', 'ScrollView', 'HorizontalScrollView',
        'LinearLayout', 'RelativeLayout', 'FrameLayout',
        'ViewGroup', 'ViewPager', 'ConstraintLayout', 'CoordinatorLayout'
    }
    
    def apply(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Args:
            elements: List of interactive elements
        Returns:
            List without containers that have children
        """
        result = []
        
        for elem in elements:
            if not self._is_container(elem):
                result.append(elem)
                continue
            
            if not self._has_interactive_children(elem, elements):
                result.append(elem)
        
        return result
    
    def _is_container(self, elem: Dict[str, Any]) -> bool:
        """Check if element is a layout container"""
        class_name = elem.get('class', '')
        return any(c in class_name for c in self.CONTAINER_CLASSES)
    
    def _has_interactive_children(self, container, all_elements):
        """Check if container has children in the element list"""
        container_bbox = container.get('bbox', {})
        if not container_bbox:
            return False
        
        cx = container_bbox.get('x', 0)
        cy = container_bbox.get('y', 0)
        cw = container_bbox.get('width', 0)
        ch = container_bbox.get('height', 0)
        
        for other in all_elements:
            if other is container:
                continue
            
            other_bbox = other.get('bbox', {})
            if not other_bbox:
                continue
            
            ox = other_bbox.get('x', 0)
            oy = other_bbox.get('y', 0)
            ow = other_bbox.get('width', 0)
            oh = other_bbox.get('height', 0)
            
            # If other is contained in container
            if (ox >= cx and oy >= cy and 
                ox + ow <= cx + cw and oy + oh <= cy + ch):
                return True
        
        return False

