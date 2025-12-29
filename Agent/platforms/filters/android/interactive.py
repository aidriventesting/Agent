from typing import Any, Dict, List, Set


class InteractiveFilter:
    """Keep Android elements that are likely interactive."""
    
    INTERACTIVE_CLASSES: Set[str] = {
        'Button', 'ImageButton', 'EditText', 'TextView', 'CheckBox',
        'RadioButton', 'Switch', 'ToggleButton', 'Spinner', 'SeekBar',
        'ImageView', 'FloatingActionButton', 'Chip', 'Tab',
    }
    
    def apply(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [e for e in elements if self._is_interactive(e)]
    
    def _is_interactive(self, e: Dict[str, Any]) -> bool:
        if e.get('clickable') == 'true':
            return True
        if e.get('focusable') == 'true':
            return True
        if e.get('scrollable') == 'true':
            return True
        
        text = e.get('text', '')
        if text and str(text).strip():
            return True
        
        content_desc = e.get('content-desc', '')
        if content_desc and str(content_desc).strip():
            return True
        
        resource_id = e.get('resource-id', '').strip()
        class_name = e.get('class', '')
        
        if resource_id:
            for interactive_class in self.INTERACTIVE_CLASSES:
                if interactive_class in class_name:
                    return True
        
        return False
