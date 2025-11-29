from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class HoverTool(BaseTool):
    """Hover over an element."""
    
    @property
    def name(self) -> str:
        return "hover"
    
    @property
    def description(self) -> str:
        return "Hover over an element by index. Use this to reveal hidden menus, tooltips, or trigger hover effects"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.WEB
    
    @property
    def works_on_locator(self) -> bool:
        return True
    
    @property
    def works_on_visual(self) -> bool:
        return False
    
    @property
    def has_visual_equivalent(self) -> bool:
        return True
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "element_index": {
                    "type": "integer",
                    "description": "The index number of the element to hover over from the UI elements list (1-based)",
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
        
        logger.debug(f"Built locator: {locator}")
        executor.run_keyword("Hover", locator)

