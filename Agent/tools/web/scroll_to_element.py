from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class ScrollToElementTool(BaseTool):
    """Scroll to a specific element on the page."""
    
    @property
    def name(self) -> str:
        return "scroll_to_element"
    
    @property
    def description(self) -> str:
        return "Scroll the page to bring a specific element into view by index. Use this when you need to scroll to a specific element like footer, header, button, or any other named element. Examples: 'scroll to footer', 'scroll to submit button', 'scroll to contact section'"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.WEB
    
    @property
    def works_on_locator(self) -> bool:
        return True
    
    @property
    def works_on_visual(self) -> bool:
        return False
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "element_index": {
                    "type": "integer",
                    "description": "The index number of the element to scroll to from the UI elements list (1-based)",
                    "minimum": 1
                }
            },
            "required": ["element_index"]
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        element_index = arguments["element_index"]
        ui_candidates = context.get("ui_candidates", [])
        
        if element_index < 1 or element_index > len(ui_candidates):
            raise AssertionError(
                f"Invalid element_index: {element_index}. Must be 1-{len(ui_candidates)}"
            )
        
        element = ui_candidates[element_index - 1]
        locator = executor.build_locator(element)
        
        logger.info(f"📜 Scrolling to element at index {element_index}")
        logger.info(f"Built locator: {locator} from element: {element}")
        
        executor.run_keyword("Scroll To Element", locator)
        logger.info(f"✅ Scrolled to element")

