from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class ClickElementTool(BaseTool):
    """Click on a mobile UI element."""
    
    @property
    def name(self) -> str:
        return "tap_element"
    
    @property
    def description(self) -> str:
        return "Click on element by selecting its index from the numbered XML element list (requires element to have ID or text)"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "element_index": {
                    "type": "integer",
                    "description": "The index number of the element from the UI elements list (1-based)",
                    "minimum": 1
                }
            },
            "required": ["element_index"]
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        element_index = arguments["element_index"]
        ui_candidates = context.get("ui_candidates", [])
        
        if element_index < 1 or element_index > len(ui_candidates):
            raise AssertionError(
                f"Invalid element_index: {element_index}. Must be 1-{len(ui_candidates)}"
            )
        
        element = ui_candidates[element_index - 1]
        locator = executor.build_locator(element)
        
        logger.info(f"🎯 Tapping element at index {element_index}")
        logger.info(f"Built locator: {locator} from element: {element}")
        
        executor.run_keyword("Click Element", locator)
        logger.info(f"✅ Tap completed")

