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
        return "Scroll content UP (reveal content above)"
    
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
            "properties": {},
            "required": []
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        # Swipe from top (20%) to bottom (80%) vertically - scrolls content UP
        executor.run_keyword("Swipe By Percent", 50, 20, 50, 80, "1s")

