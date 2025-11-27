from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from Agent.ai.vlm.interface import OmniParserOrchestrator
from robot.api import logger


class ClickVisualElementTool(BaseTool):
    """Click on element using visual detection (OmniParser).
    
    Alternative to tap_element when XML locators are unreliable or unavailable.
    Uses computer vision (OmniParser) to find elements by visual description.
    
    Use cases:
    - Elements without ID, text, or accessibility labels
    - Custom UI elements (canvas, images, icons)
    - Elements not appearing in XML hierarchy
    - Visual-based interactions
    """
    
    @property
    def name(self) -> str:
        return "click_visual_element"
    
    @property
    def description(self) -> str:
        return "Click element by VISUAL description using computer vision - USE ONLY for icons, images, or elements WITHOUT clear XML identifiers (no ID, no text)"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
    @property
    def works_on_locator(self) -> bool:
        return False  # Works with coordinates, not locators
    
    @property
    def works_on_visual(self) -> bool:
        return True  # Designed for visual detection
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "element_description": {
                    "type": "string",
                    "description": "Visual description of the element to click (e.g., 'blue login button', 'profile icon top right')"
                }
            },
            "required": ["element_description"]
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        element_description = arguments["element_description"]
        
        # Get screenshot from context
        screenshot_base64 = context.get("screenshot_base64")
        
        if not screenshot_base64:
            raise AssertionError("screenshot_base64 not provided in context for visual click")
        
        logger.debug(f"Visual click: '{element_description}'")
        
        orchestrator = OmniParserOrchestrator()
        result = orchestrator.find_element(
            element_description=element_description,
            image_base64=screenshot_base64
        )
        
        if not result:
            raise AssertionError(f"Element '{element_description}' not found")
        
        x_center, y_center = OmniParserOrchestrator.get_element_center_coordinates(result)
        
        logger.debug(f"Tapping at coordinates: ({x_center}, {y_center})")
        executor.run_keyword("Tap", [x_center, y_center])
