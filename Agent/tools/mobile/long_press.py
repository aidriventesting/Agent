from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class LongPressTool(BaseTool):
    """Long press on a mobile UI element.
    
    Uses Appium's Tap keyword with duration parameter to simulate long press.
    Works on both Android and iOS.
    """
    
    @property
    def name(self) -> str:
        return "long_press_element"
    
    @property
    def description(self) -> str:
        return "Long press on a mobile UI element (hold for 2 seconds)"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
    @property
    def works_on_locator(self) -> bool:
        return True  # Works with XML locator
    
    @property
    def works_on_visual(self) -> bool:
        return False  # AppiumLibrary keyword work on XML locator only
    
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
        
        logger.debug(f"Built locator: {locator}, long pressing for 2s")
        # Long press = Tap with duration parameter (count=1, duration=2s)
        executor.run_keyword("Tap", locator, 1, "2s")

