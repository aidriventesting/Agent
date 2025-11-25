from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class SwipeUpTool(BaseTool):
    """Swipe up on the mobile screen.
    
    Useful for scrolling up in lists, closing bottom sheets, or revealing content below.
    """
    
    @property
    def name(self) -> str:
        return "swipe_up"
    
    @property
    def description(self) -> str:
        return "Swipe up on the mobile screen (scroll up, close bottom sheet)"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
    @property
    def works_on_locator(self) -> bool:
        return False  # Global screen gesture
    
    @property
    def works_on_visual(self) -> bool:
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
        logger.info("👆 Swiping up...")
        # Swipe from bottom (80%) to top (20%) vertically, middle of screen horizontally
        executor.run_keyword("Swipe By Percent", 50, 80, 50, 20, "1s")
        logger.info("✅ Swipe up completed")

