from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class ScrollDownTool(BaseTool):
    """Scroll down the mobile screen."""
    
    @property
    def name(self) -> str:
        return "scroll_down"
    
    @property
    def description(self) -> str:
        return "NAVIGATION ONLY: Scroll content DOWN to reveal elements BELOW. NOT for clicking visible elements - use tap_element to click."
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
    @property
    def works_on_locator(self) -> bool:
        return False  # Global screen action
    
    @property
    def works_on_coordinates(self) -> bool:
        return False  # Works on viewport, not specific element
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Brief explanation (1 sentence) of WHY you chose this action"
                }
            },
            "required": []
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        reasoning = arguments.get("reasoning", "No reasoning provided")
        logger.info(f"🧠 AI reasoning: {reasoning}")
        executor.run_keyword("Swipe By Percent", 50, 80, 50, 20, "1s")

