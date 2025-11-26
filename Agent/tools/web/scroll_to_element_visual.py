from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from Agent.ai.vlm.interface import OmniParserOrchestrator
from robot.api import logger


class ScrollToElementVisualTool(BaseTool):
    """Scroll to element using visual detection (OmniParser) for WEB.
    
    Finds element coordinates and scrolls to it using JavaScript.
    """
    
    @property
    def name(self) -> str:
        return "scroll_to_element_visual"
    
    @property
    def description(self) -> str:
        return "Scroll to element by VISUAL description - USE ONLY when element is NOT in the list or has no clear locator"
    
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
                    "description": "Visual description of the element to scroll to"
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
            raise AssertionError("screenshot_base64 not provided in context for visual scroll")
        
        logger.debug(f"Visual scroll to: '{element_description}'")
        
        orchestrator = OmniParserOrchestrator()
        result = orchestrator.find_element(
            element_description=element_description,
            image_base64=screenshot_base64
        )
        
        if not result:
            raise AssertionError(f"Element '{element_description}' not found")
        
        x_center, y_center = OmniParserOrchestrator.get_element_center_coordinates(result)
        
        logger.debug(f"Scrolling to coordinates: ({x_center}, {y_center})")
        
        # Use JavaScript to scroll to coordinates
        scroll_js = f"window.scrollTo({{top: {y_center} - window.innerHeight / 2, behavior: 'smooth'}});"
        executor.run_keyword("Evaluate JavaScript", "body >> nth=0", scroll_js)
