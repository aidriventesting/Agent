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
        return "Swipe right on the mobile screen (for carousel, tabs, horizontal scrolling)"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
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
        logger.info("👉 Swiping right...")
        # Swipe from left (20%) to right (80%) horizontally, middle of screen vertically
        executor.run_keyword("Swipe By Percent", 20, 50, 80, 50, "1s")
        logger.info("✅ Swipe right completed")

