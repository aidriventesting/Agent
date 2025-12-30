from typing import Any, Dict, Tuple
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


def get_element_center(element: Dict[str, Any]) -> Tuple[int, int]:
    bbox = element.get("bbox", {})
    x = bbox.get("x", 0) + bbox.get("width", 0) // 2
    y = bbox.get("y", 0) + bbox.get("height", 0) // 2
    return x, y


class ClickElementTool(BaseTool):
    """Click on a mobile UI element using coordinates."""
    
    @property
    def name(self) -> str:
        return "click_element"
    
    @property
    def description(self) -> str:
        return "CLICK/TAP on visible elements. PREFER elements that contains/englobes CLEAR TEXT/LABELS over icons when possible. Choose the most explicit element (e.g., text suggestions, labeled buttons) rather than ambiguous icons."
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
    @property
    def works_on_locator(self) -> bool:
        return False
    
    @property
    def works_on_coordinates(self) -> bool:
        return True
    
    @property
    def has_coordinates_alternative(self) -> bool:
        return False
    
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
        logger.debug(f"Tapping at ({x}, {y}) for element: {element.get('text', '')}")
        executor.run_keyword("Tap", [x, y])

