from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class ScrollDownTool(BaseTool):
    """Scroll down the web page."""
    
    @property
    def name(self) -> str:
        return "scroll_down"
    
    @property
    def description(self) -> str:
        return "Scroll down the web page by one viewport height. Use this for general scrolling down to see more content. For scrolling to a specific element (like footer, button, etc.), use scroll_to_element instead"
    
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
        logger.info("📜 Scrolling down...")
        executor.run_keyword("Scroll By", None, "height")
        logger.info("✅ Scroll down completed")

