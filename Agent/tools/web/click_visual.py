from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from Agent.ai.vlm.interface import OmniParserOrchestrator
from robot.api import logger


class ClickVisualElementTool(BaseTool):
    """Click on element using visual detection (OmniParser) for WEB.
    
    Alternative to click_element when locators are unreliable or unavailable.
    Uses computer vision (OmniParser) to find elements by visual description.
    """
    
    @property
    def name(self) -> str:
        return "click_visual_element"
    
    @property
    def description(self) -> str:
        return "Click element by VISUAL description using computer vision - USE ONLY for icons, images, or elements WITHOUT clear locators (no ID, no text)"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.WEB
    
    @property
    def works_on_locator(self) -> bool:
        return False  # Works with coordinates
    
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
        
        logger.debug(f"Clicking at coordinates: ({x_center}, {y_center})")
        # Use 'Click With Options' or 'Mouse Button' - Click With Options is more versatile
        # We need to pass coordinates. Browser library 'Click' takes a selector.
        # To click at coordinates, we use 'Mouse Button' or 'Click' with position.
        # Actually, 'Click' keyword in Browser library takes a selector.
        # To click at coordinates, we can use 'Mouse Button' keyword with x, y arguments if available,
        # OR we can use 'Click' on 'body' with offset.
        # Let's check 'Click With Options' documentation or usage in other tools.
        # Wait, 'Click' in Playwright/Browser usually targets an element.
        # To click at x,y, we usually do: page.mouse.click(x, y).
        # In Robot Framework Browser library:
        # 'Mouse Button' keyword: Mouse Button    action=click    x=100    y=200
        
        executor.run_keyword("Mouse Button", "click", x_center, y_center)
