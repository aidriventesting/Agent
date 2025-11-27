from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class SelectOptionTool(BaseTool):
    """Select an option from a dropdown/select element."""
    
    @property
    def name(self) -> str:
        return "select_option"
    
    @property
    def description(self) -> str:
        return "Select an option from a dropdown/select element by index. Use this for <select> elements, dropdowns, or any element with selectable options"
    
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
                    "description": "The index number of the SELECT/DROPDOWN element from the UI elements list (1-based)",
                    "minimum": 1
                },
                "option_value": {
                    "type": "string",
                    "description": "The value or text of the option to select. Can be the option text or value attribute"
                }
            },
            "required": ["element_index", "option_value"]
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        element_index = arguments["element_index"]
        option_value = arguments["option_value"]
        ui_candidates = context.get("ui_candidates", [])
        
        if element_index < 1 or element_index > len(ui_candidates):
            raise AssertionError(
                f"Invalid element_index: {element_index}. Must be 1-{len(ui_candidates)}"
            )
        
        if not option_value:
            raise AssertionError("'select_option' requires option_value argument")
        
        element = ui_candidates[element_index - 1]
        locator = executor.build_locator(element)
        
        logger.debug(f"Built locator: {locator}, selecting option: {option_value}")
        executor.run_keyword("Select Options By", locator, "text", option_value)

