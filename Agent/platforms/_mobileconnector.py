from typing import Any, Dict, List
import xml.etree.ElementTree as ET
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class DeviceConnector:
    """Appium connector for UI operations (Android + iOS)."""

    def _get_driver(self) -> Any:
        appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        return appium_lib._current_application()

    def get_platform(self) -> str:
        """Detect platform from driver capabilities."""
        caps = self._get_driver().capabilities
        platform = caps.get('platformName', '').lower()
        return 'ios' if 'ios' in platform else 'android'

    def get_ui_xml(self) -> str:
        return self._get_driver().page_source

    def parse_ui(self, ui_xml: str, max_items: int = 20) -> List[Dict[str, Any]]:
        root = ET.fromstring(ui_xml)
        platform = self.get_platform()
        candidates = []

        def walk(node: Any) -> None:
            # Normalize attributes for both platforms
            if platform == 'ios':
                attrs = {
                    'text': node.get('value', '') or node.get('label', ''),
                    'resource_id': node.get('name', ''),
                    'class_name': node.get('type', ''),
                    'content_desc': node.get('label', ''),
                    'clickable': node.get('enabled', 'false') == 'true',
                    'enabled': node.get('enabled', 'false') == 'true',
                }
            else:  # android
                attrs = {
                    'text': node.get('text', ''),
                    'resource_id': node.get('resource-id', ''),
                    'class_name': node.get('class', ''),
                    'content_desc': node.get('content-desc', ''),
                    'clickable': node.get('clickable', 'false') == 'true',
                    'enabled': node.get('enabled', 'false') == 'true',
                }
            
            if attrs['clickable'] and attrs['enabled']:
                candidates.append(attrs)
            
            for child in node:
                walk(child)

        walk(root)
        
        candidates.sort(
            key=lambda x: (bool(x.get('text')), bool(x.get('content_desc')), bool(x.get('resource_id'))),
            reverse=True
        )
        logger.info(f"Platform: {platform}, Found {len(candidates)} interactive elements")
        return candidates[:max_items]

    def build_locator_from_element(self, element: Dict[str, Any]) -> str:
        """Build best locator from element attributes (priority: id > accessibility > text xpath)."""
        resource_id = element.get('resource_id')
        content_desc = element.get('content_desc')
        text = element.get('text')
        class_name = element.get('class_name')
        
        # Priority 1: resource_id (most reliable)
        if resource_id:
            return f"id={resource_id}"
        
        # Priority 2: accessibility id
        if content_desc:
            return f"accessibility_id={content_desc}"
        
        # Priority 3: text-based xpath (mobile-safe)
        if text:
            return f"//*[@text='{text}']"
        
        # Fallback: class name
        if class_name:
            return f"class={class_name}"
        
        raise AssertionError("Cannot build locator: element has no usable attributes")

    def to_rf_locator(self, locator: Dict[str, Any]) -> str:
        """Convert locator dict to RF format (legacy support)."""
        strategy = locator["strategy"]
        value = locator["value"]
        
        locator_map = {
            "id": f"id={value}",
            "accessibility_id": f"accessibility_id={value}",
            "xpath": value,
            "class_name": f"class={value}",
        }
        
        return locator_map.get(strategy, value)

    def collect_ui_candidates(self, max_items: int = 20) -> List[Dict[str, Any]]:
        xml = self.get_ui_xml()
        return self.parse_ui(xml, max_items=max_items)

    def get_screenshot_base64(self) -> str:
        return self._get_driver().get_screenshot_as_base64()

    def embed_image_to_log(self, base64_screenshot: str, width: int = 400) -> None:
        msg = f"</td></tr><tr><td colspan=\"3\"><img src=\"data:image/png;base64, {base64_screenshot}\" width=\"{width}\"></td></tr>"
        logger.info(msg, html=True, also_console=False)