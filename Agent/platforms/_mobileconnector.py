from typing import Any, Dict, List
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
# Lazy import in methods for collectors, renderer, and locator builder


class DeviceConnector:
    """Appium connector for UI operations (Android + iOS)."""
    
    def __init__(self):
        self._appium_lib = None
        self._driver = None
        self._session_id = None
        self._platform = None
        self._collector = None  # Lazy init
        self._filter_pipeline = None  # Lazy init
        self._locator_builder = None  # Lazy init
        self._renderer = None  # Lazy init

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
        if self._platform is None:
            caps = self._get_driver().capabilities
            platform = caps.get('platformName', '').lower()
            self._platform = 'ios' if 'ios' in platform else 'android'
        return self._platform

    def get_screen_size(self) -> Dict[str, int]:
        try:
            size = self._get_driver().get_window_size()
            return {'width': size.get('width', 0), 'height': size.get('height', 0)}
            #TODO: see if this is really needed and if there is better fallback
        except Exception:
            logger.warn("⚠️ Could not get screen size, using fallback 1080x1920")
            return {'width': 1080, 'height': 1920}

    def get_ui_xml(self) -> str:
        return self._get_driver().page_source

    def collect_ui_candidates(self, max_items: int = 50) -> List[Dict[str, Any]]:
        xml = self.get_ui_xml()
        collector = self._get_collector()
        pipeline = self._get_filter_pipeline()
        
        elements = collector.parse_xml(xml)
        filtered = pipeline.apply(elements)
        
        screen_size = self.get_screen_size()
        self._add_normalized_bbox(filtered, screen_size)
        
        filtered.sort(
            key=lambda e: (
                bool(e.get('resource-id', '').strip()),
                bool(e.get('content-desc', '').strip()),
                bool(e.get('text', '').strip()),
                e.get('clickable') == 'true',
            ),
            reverse=True
        )
        
        return filtered[:max_items]

    def collect_all_elements(self) -> List[Dict[str, Any]]:
        xml = self.get_ui_xml()
        collector = self._get_collector()
        elements = collector.parse_xml(xml)
        
        screen_size = self.get_screen_size()
        self._add_normalized_bbox(elements, screen_size)
        
        return elements
    
    def _add_normalized_bbox(self, elements: List[Dict[str, Any]], screen_size: Dict[str, int]) -> None:
        """Add bbox_normalized to each element."""
        sw = screen_size.get('width', 0)
        sh = screen_size.get('height', 0)
        
        if sw <= 0 or sh <= 0:
            return
        
        for elem in elements:
            bbox = elem.get('bbox', {})
            if bbox:
                elem['bbox_normalized'] = {
                    'x': round(bbox.get('x', 0) / sw, 4),
                    'y': round(bbox.get('y', 0) / sh, 4),
                    'width': round(bbox.get('width', 0) / sw, 4),
                    'height': round(bbox.get('height', 0) / sh, 4),
                }

    def build_locator_from_element(self, element: Dict[str, Any], strategy: str = 'auto') -> str:
        """
        Args:
            element: Dict with raw XML attributes
            strategy: 'auto' | 'id_only' | 'bounds' | 'xpath_attrs' | 'xpath_all'
        Returns:
            Appium locator string
        Example: build_locator_from_element(elem, 'id_only') -> 'id=com.android:id/button'
        """
        return self._get_locator_builder().build(element, strategy=strategy)

    def render_ui_for_prompt(self, ui_elements: List[Dict[str, Any]]) -> str:
        platform = self.get_platform()
        return self._get_renderer().serialize(ui_elements, platform=platform)

    def get_screenshot_base64(self) -> str:
        return self._get_driver().get_screenshot_as_base64()

    def embed_image_to_log(self, base64_screenshot: str, width: int = 400) -> None:
        msg = f"</td></tr><tr><td colspan=\"3\"><img src=\"data:image/png;base64, {base64_screenshot}\" width=\"{width}\"></td></tr>"
        logger.info(msg, html=True, also_console=False)

    def wait_for_page_stable(self, delay: float = 1.0) -> None:
        import time
        time.sleep(delay)
    
    def _get_locator_builder(self):
        if self._locator_builder is None:
            from Agent.platforms.locators import MobileLocatorBuilder
            platform = self.get_platform()
            self._locator_builder = MobileLocatorBuilder(platform=platform)
        return self._locator_builder
    
    def _get_collector(self):
        if self._collector is None:
            platform = self.get_platform()
            if platform == 'ios':
                from Agent.platforms.collectors import IOSCollector
                self._collector = IOSCollector()
            else:
                from Agent.platforms.collectors import AndroidCollector
                self._collector = AndroidCollector()
        return self._collector
    
    def _get_filter_pipeline(self):
        if self._filter_pipeline is None:
            platform = self.get_platform()
            if platform == 'ios':
                from Agent.platforms.filters.pipeline import FilterPipeline
                self._filter_pipeline = FilterPipeline()
            else:
                from Agent.platforms.filters.android import AndroidFilterPipeline
                self._filter_pipeline = AndroidFilterPipeline()
        return self._filter_pipeline
    
    def _get_renderer(self):
        if self._renderer is None:
            from Agent.platforms.grounding.text.serializer import TextSerializer
            self._renderer = TextSerializer()
        return self._renderer
