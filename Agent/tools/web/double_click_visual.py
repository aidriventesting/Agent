from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from Agent.ai.vlm.interface import OmniParserOrchestrator
from robot.api import logger


class DoubleClickVisualTool(BaseTool):
    """Double click on element using visual detection (OmniParser) for WEB.
    
    Alternative to double_click when locators are unreliable.
    Uses computer vision to find the element and double clicks it.
    """
    
    @property
    def name(self) -> str:
        return "double_click_visual"
    
    @property
    def description(self) -> str:
        return "Double click element by VISUAL description - USE ONLY when standard double_click fails or for elements without clear locators"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.WEB
    
    @property
    def works_on_locator(self) -> bool:
        return False
    
    @property
    def works_on_visual(self) -> bool:
        return True
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "element_description": {
                    "type": "string",
                    "description": "Visual description of the element to double click"
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
        
        screenshot_base64 = context.get("screenshot_base64")
        
        if not screenshot_base64:
            raise AssertionError("screenshot_base64 not provided in context for visual double click")
        
        logger.debug(f"Visual double click: '{element_description}'")
        
        orchestrator = OmniParserOrchestrator()
        result = orchestrator.find_element(
            element_description=element_description,
            image_base64=screenshot_base64
        )
        
        if not result:
            raise AssertionError(f"Element '{element_description}' not found")
        
        x_center, y_center = OmniParserOrchestrator.get_element_center_coordinates(result)
        
        logger.debug(f"Double clicking at coordinates: ({x_center}, {y_center})")
        
        executor.run_keyword("Mouse Button", "click", x_center, y_center, "clickCount=2")
