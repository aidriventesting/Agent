from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class GoBackTool(BaseTool):
    """Navigate back one step in the app (like pressing back button).
    
    Works on both Android and iOS. Simulates pressing the system back button.
    """
    
    @property
    def name(self) -> str:
        return "go_back"
    
    @property
    def description(self) -> str:
        return "Go back one step in the app navigation (back button)"
    
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
        logger.info("◀️ Going back...")
        executor.run_keyword("Go Back")
        logger.info("✅ Back navigation completed")

