from typing import Any, Dict, List, Set, Optional


class SmartHierarchyFilter:
    """
    Args:
        prefer_parent_when_clickable: Keep parent if clickable, ignore children
        min_relevance_score: Min score to keep element
        overlap_threshold: Min overlap ratio (0-1) to group elements
    Example: SmartHierarchyFilter(prefer_parent_when_clickable=True, min_relevance_score=5)
    """
    
    CONTAINER_CLASSES = {
        'RecyclerView', 'ScrollView', 'HorizontalScrollView',
        'LinearLayout', 'RelativeLayout', 'FrameLayout',
        'ViewGroup', 'ViewPager', 'ConstraintLayout'
    }
    
    def __init__(
        self,
        prefer_parent_when_clickable: bool = True,
        min_relevance_score: int = 0,
        overlap_threshold: float = 0.9
    ):
        self._prefer_parent_when_clickable = prefer_parent_when_clickable
        self._min_relevance_score = min_relevance_score
        self._overlap_threshold = overlap_threshold
    
    def apply(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Args:
            elements: List of elements
        Returns:
            List with one element per overlapping group
        """
        if not elements:
            return []
        
        groups = self._build_overlap_groups(elements)
        selected_indices = set()
        
        for group_indices in groups:
            best_idx = self._select_best_from_group(elements, group_indices)
            if best_idx is not None:
                selected_indices.add(best_idx)
        
        return [elements[i] for i in sorted(selected_indices)]
    
    def _build_overlap_groups(self, elements: List[Dict[str, Any]]) -> List[List[int]]:
        """
        Args:
            elements: List of elements
        Returns:
            List of groups, each group is list of overlapping element indices
        """
        n = len(elements)
        visited = [False] * n
        groups = []
        
        for i in range(n):
            if visited[i]:
                continue
            
            elem_i = elements[i]
            bbox_i = elem_i.get('bbox', {})
            if not bbox_i:
                groups.append([i])
                visited[i] = True
                continue
            
            group = [i]
            visited[i] = True
            
            for j in range(i + 1, n):
                if visited[j]:
                    continue
                
                elem_j = elements[j]
                bbox_j = elem_j.get('bbox', {})
                if not bbox_j:
                    continue
                
                if self._should_group(elem_i, elem_j, bbox_i, bbox_j):
                    group.append(j)
                    visited[j] = True
            
            groups.append(group)
        
        return groups
    
    def _should_group(
        self,
        elem1: Dict[str, Any],
        elem2: Dict[str, Any],
        bbox1: Dict[str, int],
        bbox2: Dict[str, int]
    ) -> bool:
        """Check if two elements should be grouped together"""
        if self._is_container(elem1) or self._is_container(elem2):
            return False
        
        if not self._is_interactive(elem1) and not self._is_interactive(elem2):
            return False
        
        return self._has_significant_overlap(bbox1, bbox2)
    
    def _is_container(self, elem: Dict[str, Any]) -> bool:
        """Check if element is a layout container"""
        class_name = elem.get('class', '')
        return any(c in class_name for c in self.CONTAINER_CLASSES)
    
    def _has_significant_overlap(
        self,
        bbox1: Dict[str, int],
        bbox2: Dict[str, int]
    ) -> bool:
        """Check if two bboxes overlap significantly"""
        x1 = bbox1.get('x', 0)
        y1 = bbox1.get('y', 0)
        w1 = bbox1.get('width', 0)
        h1 = bbox1.get('height', 0)
        
        x2 = bbox2.get('x', 0)
        y2 = bbox2.get('y', 0)
        w2 = bbox2.get('width', 0)
        h2 = bbox2.get('height', 0)
        
        x_left = max(x1, x2)
        y_top = max(y1, y2)
        x_right = min(x1 + w1, x2 + w2)
        y_bottom = min(y1 + h1, y2 + h2)
        
        if x_right < x_left or y_bottom < y_top:
            return False
        
        intersection = (x_right - x_left) * (y_bottom - y_top)
        area1 = w1 * h1
        area2 = w2 * h2
        
        if area1 == 0 or area2 == 0:
            return False
        
        overlap_ratio = max(intersection / area1, intersection / area2)
        return overlap_ratio > self._overlap_threshold
    
    def _select_best_from_group(
        self,
        elements: List[Dict[str, Any]],
        group_indices: List[int]
    ) -> Optional[int]:
        """
        Args:
            elements: All elements
            group_indices: Indices of parent and children
        Returns:
            Index of best element to keep
        """
        if not group_indices:
            return None
        
        parent_idx = group_indices[0]
        parent = elements[parent_idx]
        
        if self._prefer_parent_when_clickable:
            if self._is_interactive(parent):
                return parent_idx
        
        best_idx = parent_idx
        best_score = self._get_relevance_score(parent)
        
        for idx in group_indices:
            elem = elements[idx]
            score = self._get_relevance_score(elem)
            
            if score > best_score:
                best_score = score
                best_idx = idx
        
        if best_score >= self._min_relevance_score:
            return best_idx
        
        return None
    
    def _is_interactive(self, elem: Dict[str, Any]) -> bool:
        """Check if element is interactive"""
        return (
            elem.get('clickable') == 'true' or
            elem.get('focusable') == 'true' or
            elem.get('long-clickable') == 'true'
        )
    
    def _get_relevance_score(self, elem: Dict[str, Any]) -> int:
        """
        Args:
            elem: Element dict
        Returns:
            Relevance score (higher = more relevant)
        """
        score = 0
        
        if elem.get('clickable') == 'true':
            score += 20
        if elem.get('focusable') == 'true':
            score += 15
        
        class_name = elem.get('class', '')
        if 'Button' in class_name or 'EditText' in class_name or 'ImageButton' in class_name:
            score += 10
        
        if elem.get('text', '').strip():
            score += 8
        if elem.get('content-desc', '').strip():
            score += 6
        if elem.get('resource-id', '').strip():
            score += 4
        
        if 'Layout' in class_name or 'ViewGroup' in class_name or 'FrameLayout' in class_name:
            score -= 10
        
        bbox = elem.get('bbox', {})
        if bbox:
            width = bbox.get('width', 0)
            height = bbox.get('height', 0)
            if width < 10 or height < 10:
                score -= 5
        
        return score

