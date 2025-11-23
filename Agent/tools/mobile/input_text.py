from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class InputTextTool(BaseTool):
    """Clear and input text into a mobile UI element."""
    
    @property
    def name(self) -> str:
        return "input_text"
    
    @property
    def description(self) -> str:
        return "Clear and input text into a mobile UI element"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "element_index": {
                    "type": "integer",
                    "description": "The index number of the element from the UI elements list (1-based)",
                    "minimum": 1
                },
                "text": {
                    "type": "string",
                    "description": "The text to input into the element"
                }
            },
            "required": ["element_index", "text"]
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        element_index = arguments["element_index"]
        text = arguments["text"]
        ui_candidates = context.get("ui_candidates", [])
        
        if element_index < 1 or element_index > len(ui_candidates):
            raise AssertionError(
                f"Invalid element_index: {element_index}. Must be 1-{len(ui_candidates)}"
            )
        
        if not text:
            raise AssertionError("'input_text' requires text argument")
        
        element = ui_candidates[element_index - 1]
        locator = executor.build_locator(element)
        
        logger.info(f"⌨️ Inputting text into element at index {element_index}")
        logger.info(f"Built locator: {locator} from element: {element}")
        logger.info(f"Text to input: '{text}'")
        
        executor.run_keyword("Clear Text", locator)
        executor.run_keyword("Input Text", locator, text)
        logger.info(f"✅ Input text completed")

