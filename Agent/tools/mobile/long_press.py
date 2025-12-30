from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from Agent.tools.mobile.click_element import get_element_center
from robot.api import logger


class LongPressTool(BaseTool):
    """Long press on a mobile UI element using coordinates."""
    
    @property
    def name(self) -> str:
        return "long_press_element"
    
    @property
    def description(self) -> str:
        return "Long press on element by INDEX (hold for 2 seconds)"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
    @property
    def works_on_locator(self) -> bool:
        return True
    
    @property
    def works_on_coordinates(self) -> bool:
        return True
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "element_index": {
                    "type": "integer",
                    "description": "The index number of the element from the UI elements list (1-based)",
                    "minimum": 1
                },
                "reasoning": {
                    "type": "string",
                    "description": "Brief explanation (1 sentence) of WHY you chose this element and action"
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
        reasoning = arguments.get("reasoning", "No reasoning provided")
        ui_candidates = context.get("ui_candidates", [])
        
        if element_index < 1 or element_index > len(ui_candidates):
            raise AssertionError(
                f"Invalid element_index: {element_index}. Must be 1-{len(ui_candidates)}"
            )
        
        element = ui_candidates[element_index - 1]
        x, y = get_element_center(element)
        
        logger.info(f"🧠 AI reasoning: {reasoning}")
        logger.debug(f"Long pressing at ({x}, {y}) for 2s")
        executor.run_keyword("Tap", [x, y], 1, "2s")

