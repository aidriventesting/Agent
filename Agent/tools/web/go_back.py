from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class GoBackTool(BaseTool):
    """Navigate back in browser history (like pressing browser back button)."""
    
    @property
    def name(self) -> str:
        return "go_back"
    
    @property
    def description(self) -> str:
        return "Go back one step in browser history (back button). Use this to navigate to the previous page"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.WEB
    
    @property
    def works_on_locator(self) -> bool:
        return False
    
    @property
    def works_on_visual(self) -> bool:
        return False
    
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
        executor.run_keyword("Go Back")

