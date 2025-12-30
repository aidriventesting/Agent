from typing import Any, Dict, List


class IOSCollector:
    """Collects UI elements from iOS XML page source."""
    
    def get_name(self) -> str:
        return "ios"
    
    def parse_xml(self, xml_source: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("iOS collector not implemented yet")
