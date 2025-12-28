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
        return "Scroll down the mobile screen"
    
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
            "properties": {},
            "required": []
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        executor.run_keyword("Swipe By Percent", 50, 80, 50, 20, "1s")

