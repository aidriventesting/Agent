from typing import Any, Dict, List
import xml.etree.ElementTree as ET
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class DeviceConnector:
    """Appium connector for UI operations (Android + iOS)."""
    
    def __init__(self):
        """Initialize connector, caching AppiumLibrary instance for reuse."""
        self._appium_lib = None
        self._driver = None
        self._session_id = None

    def _get_driver(self) -> Any:
        """Get Appium driver instance, maintaining it within our library.
        
        Captures and maintains the driver to avoid issues when mixing Agent keywords
        with AppiumLibrary keywords (Open Application, Close Application, Sleep, etc.).
        """
        # Get AppiumLibrary instance (cached, doesn't change)
        if self._appium_lib is None:
            self._appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        
        # Get current driver from AppiumLibrary
        current_driver = self._appium_lib._current_application()
        
        # If no current driver exists, return None (should not happen if Open Application was called)
        if current_driver is None:
            raise RuntimeError(
                "No Appium session available. Ensure 'Open Application' is called before using Agent keywords."
            )
        
        # Get current session ID
        current_session_id = getattr(current_driver, 'session_id', None)
        
        # If we have a stored driver, check if it's still the same session
        if self._driver is not None:
            stored_session_id = getattr(self._driver, 'session_id', None)
            
            # If session changed (new test opened new session), update our reference
            if current_session_id != stored_session_id:
                logger.debug(f"Session changed: {stored_session_id} -> {current_session_id}. Updating driver reference.")
                self._driver = current_driver
                self._session_id = current_session_id
            else:
                # Same session, verify it's still valid by checking a lightweight property
                try:
                    _ = self._driver.current_activity
                    return self._driver
                except Exception:
                    # Driver invalid, get fresh one
                    logger.debug("Stored driver invalid, getting fresh driver")
                    self._driver = current_driver
                    self._session_id = current_session_id
        else:
            # First call, capture and store the driver
            self._driver = current_driver
            self._session_id = current_session_id
            logger.debug(f"Driver captured and maintained (session: {current_session_id})")
        
        return self._driver

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
        logger.debug(f"Platform: {platform}, Found {len(candidates)} interactive elements")
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

    def collect_ui_candidates(self, max_items: int = 20) -> List[Dict[str, Any]]:
        xml = self.get_ui_xml()
        return self.parse_ui(xml, max_items=max_items)
    
    def render_ui_for_prompt(self, ui_elements: List[Dict[str, Any]]) -> str:
        """Render UI elements as numbered text list for AI prompt.
    
        Args:
            ui_elements: List of UI element dicts from collect_ui_candidates()
            
        Returns:
            Formatted string like:
            1. text='Login' | id='com.app:id/login_btn'
            2. text='Sign Up' | desc='Sign up button'
        """
        if not ui_elements:
            return "(no UI elements found)"
        
        rendered = []
        for i, el in enumerate(ui_elements[:20], 1):
            parts = []
            if el.get("text"):
                parts.append(f"text='{el['text']}'")
            if el.get("resource_id"):
                parts.append(f"id='{el['resource_id']}'")
            if el.get("content_desc"):
                parts.append(f"desc='{el['content_desc']}'")
            
            line = f"{i}. {' | '.join(parts) if parts else el.get('class_name', 'unknown')}"
            rendered.append(line)
        
        return "\n".join(rendered)

    def get_screenshot_base64(self) -> str:
        return self._get_driver().get_screenshot_as_base64()

    def embed_image_to_log(self, base64_screenshot: str, width: int = 400) -> None:
        msg = f"</td></tr><tr><td colspan=\"3\"><img src=\"data:image/png;base64, {base64_screenshot}\" width=\"{width}\"></td></tr>"
        logger.info(msg, html=True, also_console=False)