from typing import Any, Dict, List
import xml.etree.ElementTree as ET


class AndroidCollector:
    """Collects UI elements from Android XML page source."""
    
    def get_name(self) -> str:
        return "android"
    
    def parse_xml(self, xml_source: str) -> List[Dict[str, Any]]:
        """
        Args:
            xml_source: Appium page source XML
        Returns:
            List of element dicts with raw XML attributes + computed bbox
        """
        root = ET.fromstring(xml_source)
        elements = []
        
        def walk(node: Any) -> None:
            attrs = self._parse_node(node)
            elements.append(attrs)
            for child in node:
                walk(child)
        
        walk(root)
        return elements
    
    def _parse_node(self, node: Any) -> Dict[str, Any]:
        raw_attrs = dict(node.attrib)
        
        bounds_str = raw_attrs.get('bounds', '')
        bbox = self._parse_bounds(bounds_str)
        
        return {
            **raw_attrs,
            'bbox': bbox,
        }
    
    def _parse_bounds(self, bounds_str: str) -> Dict[str, int]:
        """
        Args:
            bounds_str: "[0,72][1080,200]"
        Returns:
            {'x': 0, 'y': 72, 'width': 1080, 'height': 128}
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
