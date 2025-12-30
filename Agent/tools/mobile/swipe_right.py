from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class SwipeRightTool(BaseTool):
    """Swipe right on the mobile screen.
    
    Useful for navigating carousels, image galleries, tabs, or horizontal scrolling.
    """
    
    @property
    def name(self) -> str:
        return "swipe_right"
    
    @property
    def description(self) -> str:
        return "USE THIS ONLY for horizontal navigation: carousels, image galleries, tabs. Do NOT use to click on visible elements - use tap_element instead."
    
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
        # Swipe from left (20%) to right (80%) horizontally, middle of screen vertically
        executor.run_keyword("Swipe By Percent", 20, 50, 80, 50, "1s")

