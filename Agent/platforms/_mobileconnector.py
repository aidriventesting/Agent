from typing import Any, Dict, List
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from Agent.platforms.collectors.android_collector import AndroidCollector
from Agent.platforms.collectors.ios_collector import IOSCollector
from Agent.platforms.locators.mobile import MobileLocatorBuilder
from Agent.platforms.filters.android import AndroidFilterPipeline
from Agent.ai.prompts.renderer import UIRenderer


class DeviceConnector:
    """Appium connector for UI operations (Android + iOS)."""
    
    def __init__(self):
        self._appium_lib = None
        self._driver = None
        self._session_id = None
        self._android_collector = AndroidCollector()
        self._ios_collector = IOSCollector()
        self.locator_builder = MobileLocatorBuilder()
        self._renderer = UIRenderer()

    def _get_driver(self) -> Any:
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
        caps = self._get_driver().capabilities
        platform = caps.get('platformName', '').lower()
        return 'ios' if 'ios' in platform else 'android'

    def get_screen_size(self) -> Dict[str, int]:
        size = self._get_driver().get_window_size()
        return {'width': size.get('width', 0), 'height': size.get('height', 0)}

    def get_ui_xml(self) -> str:
        return self._get_driver().page_source

    def collect_ui_candidates(self, max_items: int = 50) -> List[Dict[str, Any]]:
        xml = self.get_ui_xml()
        platform = self.get_platform()
        
        if platform == 'ios':
            raise NotImplementedError("iOS not implemented yet")
        
        elements = self._android_collector.parse_xml(xml)
        pipeline = AndroidFilterPipeline(self.get_screen_size())
        filtered = pipeline.apply(elements)
        
        return filtered[:max_items]

    def collect_all_elements(self) -> List[Dict[str, Any]]:
        xml = self.get_ui_xml()
        platform = self.get_platform()
        
        if platform == 'ios':
            raise NotImplementedError("iOS not implemented yet")
        
        return self._android_collector.parse_xml(xml)

    def build_locator_from_element(self, element: Dict[str, Any], robust: bool = False) -> str:
        platform = self.get_platform()
        self.locator_builder.set_platform(platform)
        return self.locator_builder.build(element, robust=robust)

    def render_ui_for_prompt(self, ui_elements: List[Dict[str, Any]]) -> str:
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
