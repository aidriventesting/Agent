

from typing import Any, Dict, List
import xml.etree.ElementTree as ET
from robot.api import logger
from Agent.platforms.collectors.base_collector import BaseUICollector


class XMLCollector(BaseUICollector):
    """
    Collects UI elements by parsing Appium XML page source.
    
    Supports both Android and iOS XML formats.
    """
    
    def __init__(self, platform: str = "android"):
        self._platform = platform
    
    def get_name(self) -> str:
        return "xml"
    
    def set_platform(self, platform: str) -> None:
        self._platform = platform
    
    def collect_elements(self, max_items: int = 50) -> List[Dict[str, Any]]:
        raise NotImplementedError("Use parse_xml() with XML source instead")
    
    def parse_xml(self, xml_source: str, max_items: int = 50) -> List[Dict[str, Any]]:
        """
        Parse XML page source to extract interactive elements.
        
        Args:
            xml_source: Appium page source XML string
            max_items: Maximum elements to return
        Returns:
            List of element dictionaries
        """
        root = ET.fromstring(xml_source)
        candidates = []
        
        def walk(node: Any) -> None:
            if self._platform == 'ios':
                attrs = self._parse_ios_node(node)
            else:
                attrs = self._parse_android_node(node)
            
            if attrs['clickable'] and attrs['enabled']:
                candidates.append(attrs)
            
            for child in node:
                walk(child)
        
        walk(root)
        
        candidates.sort(
            key=lambda x: (
                bool(x.get('text')),
                bool(x.get('accessibility_label')),
                bool(x.get('resource_id'))
            ),
            reverse=True
        )
        
        logger.debug(f"[{self.get_name()}] Platform: {self._platform}, Found {len(candidates)} interactive elements")
        return candidates[:max_items]
    
    def _parse_android_node(self, node: Any) -> Dict[str, Any]:
        """Parse Android XML node to element dict."""
        bbox = self._parse_android_bounds(node.get('bounds', ''))
        content_desc = node.get('content-desc', '')
        return {
            'text': node.get('text', ''),
            'resource_id': node.get('resource-id', ''),
            'class_name': node.get('class', ''),
            'accessibility_label': content_desc,
            'content_desc': content_desc,  # backward compat
            'clickable': node.get('clickable', 'false') == 'true',
            'enabled': node.get('enabled', 'false') == 'true',
            'bbox': bbox,
        }
    
    def _parse_ios_node(self, node: Any) -> Dict[str, Any]:
        """Parse iOS XML node to element dict."""
        try:
            bbox = {
                'x': int(node.get('x', 0)),
                'y': int(node.get('y', 0)),
                'width': int(node.get('width', 0)),
                'height': int(node.get('height', 0)),
            }
        except (ValueError, TypeError):
            bbox = {}
        
        if bbox.get('width', 0) <= 0:
            bbox = {}
        
        label = node.get('label', '')
        return {
            'text': node.get('value', '') or label,
            'resource_id': node.get('name', ''),
            'class_name': node.get('type', ''),
            'accessibility_label': label,
            'label': label,  # iOS-specific
            'clickable': node.get('enabled', 'false') == 'true',
            'enabled': node.get('enabled', 'false') == 'true',
            'bbox': bbox,
        }
    
    def _parse_android_bounds(self, bounds_str: str) -> Dict[str, int]:
        """
        Parse Android bounds string to bbox dict.
        
        Format: "[0,72][1080,200]" -> {x, y, width, height}
        """
        if not bounds_str:
            return {}
        try:
            parts = bounds_str.replace('][', ',').strip('[]').split(',')
            if len(parts) == 4:
                x1, y1, x2, y2 = map(int, parts)
                return {'x': x1, 'y': y1, 'width': x2 - x1, 'height': y2 - y1}
        except (ValueError, AttributeError):
            pass
        return {}

