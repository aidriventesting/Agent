from typing import Any, Dict, List
import base64
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from Agent.platforms.collectors.collector_factory import CollectorRegistry
from Agent.platforms.locators.web import WebLocatorBuilder
from Agent.ai.prompts.renderer import UIRenderer


class WebConnectorRF:
    """Playwright connector using Robot Framework Browser library keywords."""

    def __init__(self, collector_strategy: str = "js_query") -> None:
        """
        Args:
            collector_strategy: Name of the collector ("js_query")
        """
        self.collector_strategy = collector_strategy
        self.collector = CollectorRegistry.create(collector_strategy)
        self.locator_builder = WebLocatorBuilder()
        self._renderer = UIRenderer()
        logger.debug(f"WebConnectorRF initialized with collector: {collector_strategy}")

    def get_platform(self) -> str:
        return "web"

    def collect_ui_candidates(self, max_items: int = 500) -> List[Dict[str, Any]]:
        """Collect interactive web elements."""
        logger.debug(f"Collecting UI candidates using strategy: {self.collector_strategy}")
        return self.collector.collect_elements(max_items)

    def build_locator_from_element(self, element: Dict[str, Any]) -> str:
        """Build Playwright locator from element attributes."""
        return self.locator_builder.build(element)

    def get_screenshot_base64(self) -> str:
        """Capture screenshot as base64."""
        try:
            screenshot_bytes = BuiltIn().run_keyword('Take Screenshot', 'fullPage')
            if isinstance(screenshot_bytes, bytes):
                return base64.b64encode(screenshot_bytes).decode('utf-8')
            elif isinstance(screenshot_bytes, str):
                with open(screenshot_bytes, 'rb') as f:
                    return base64.b64encode(f.read()).decode('utf-8')
            else:
                logger.error(f"Unexpected screenshot type: {type(screenshot_bytes)}")
                return ""
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return ""

    def embed_image_to_log(self, base64_screenshot: str, width: int = 400) -> None:
        """Embed screenshot into Robot Framework log."""
        msg = f"</td></tr><tr><td colspan=\"3\"><img src=\"data:image/png;base64, {base64_screenshot}\" width=\"{width}\"></td></tr>"
        logger.info(msg, html=True, also_console=False)

    def render_ui_for_prompt(self, ui_elements: List[Dict[str, Any]]) -> str:
        """Render UI elements as text for AI prompt."""
        return self._renderer.render(ui_elements, platform="web")
