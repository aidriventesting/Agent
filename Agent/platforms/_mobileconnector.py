from typing import Any, Dict, List
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from Agent.platforms.collectors.xml_collector import XMLCollector
from Agent.platforms.locators.mobile import MobileLocatorBuilder
from Agent.ai.prompts.renderer import UIRenderer


class DeviceConnector:
    """Appium connector for UI operations (Android + iOS)."""
    
    def __init__(self):
        self._appium_lib = None
        self._driver = None
        self._session_id = None
        self._collector = XMLCollector()
        self.locator_builder = MobileLocatorBuilder()
        self._renderer = UIRenderer()

    def _get_driver(self) -> Any:
        """Get Appium driver instance."""
        if self._appium_lib is None:
            self._appium_lib = BuiltIn().get_library_instance('AppiumLibrary')
        
        current_driver = self._appium_lib._current_application()
        
        if current_driver is None:
            raise RuntimeError(
                "No Appium session available. Ensure 'Open Application' is called before using Agent keywords."
            )
        
        current_session_id = getattr(current_driver, 'session_id', None)
        
        if self._driver is not None:
            stored_session_id = getattr(self._driver, 'session_id', None)
            
            if current_session_id != stored_session_id:
                logger.debug(f"Session changed: {stored_session_id} -> {current_session_id}")
                self._driver = current_driver
                self._session_id = current_session_id
            else:
                try:
                    _ = self._driver.session_id
                    return self._driver
                except Exception:
                    logger.debug("Stored driver invalid, getting fresh driver")
                    self._driver = current_driver
                    self._session_id = current_session_id
        else:
            self._driver = current_driver
            self._session_id = current_session_id
            logger.debug(f"Driver captured (session: {current_session_id})")
        
        return self._driver

    def get_platform(self) -> str:
        """Detect platform from driver capabilities."""
        caps = self._get_driver().capabilities
        platform = caps.get('platformName', '').lower()
        return 'ios' if 'ios' in platform else 'android'

    def get_ui_xml(self) -> str:
        return self._get_driver().page_source

    def collect_ui_candidates(self, max_items: int = 50) -> List[Dict[str, Any]]:
        """Collect interactive UI elements from current screen."""
        xml = self.get_ui_xml()
        platform = self.get_platform()
        self._collector.set_platform(platform)
        return self._collector.parse_xml(xml, max_items=max_items)

    def build_locator_from_element(self, element: Dict[str, Any]) -> str:
        """Build Appium locator from element attributes."""
        platform = self.get_platform()
        self.locator_builder.set_platform(platform)
        return self.locator_builder.build(element)

    def render_ui_for_prompt(self, ui_elements: List[Dict[str, Any]]) -> str:
        """Render UI elements as text for AI prompt."""
        platform = self.get_platform()
        return self._renderer.render(ui_elements, platform=platform)

    def get_screenshot_base64(self) -> str:
        return self._get_driver().get_screenshot_as_base64()

    def embed_image_to_log(self, base64_screenshot: str, width: int = 400) -> None:
        msg = f"</td></tr><tr><td colspan=\"3\"><img src=\"data:image/png;base64, {base64_screenshot}\" width=\"{width}\"></td></tr>"
        logger.info(msg, html=True, also_console=False)

    def wait_for_page_stable(self, delay: float = 1.0) -> None:
        import time
        time.sleep(delay)
