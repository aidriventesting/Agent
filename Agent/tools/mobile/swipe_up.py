from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class SwipeUpTool(BaseTool):
    """Scroll content up on the mobile screen (reveal content above)."""
    
    @property
    def name(self) -> str:
        return "swipe_up"
    
    @property
    def description(self) -> str:
        return "NAVIGATION ONLY: Scroll content UP to reveal elements ABOVE. NOT for clicking visible elements - use tap_element to click."
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
    @property
    def works_on_locator(self) -> bool:
        return False  # Global screen gesture
    
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
        # Swipe from top (20%) to bottom (80%) vertically - scrolls content UP
        executor.run_keyword("Swipe By Percent", 50, 20, 50, 80, "1s")

