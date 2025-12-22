from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from Agent.tools.mobile.click_element import get_element_center
from robot.api import logger


class InputTextTool(BaseTool):
    """Input text into a mobile UI element using coordinates."""
    
    @property
    def name(self) -> str:
        return "input_text"
    
    @property
    def description(self) -> str:
        return "USE THIS when instruction contains 'input', 'type', 'enter', 'fill', 'write', 'saisir', 'taper' or mentions entering text. Types text into a text field."
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
    @property
    def works_on_locator(self) -> bool:
        return True
    
    @property
    def works_on_coordinates(self) -> bool:
        return True
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "element_index": {
                    "type": "integer",
                    "description": "The index number of the TEXT FIELD element from the UI elements list (1-based)",
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
        x, y = get_element_center(element)
        
        logger.debug(f"Tapping at ({x}, {y}) to focus, then input: '{text}'")
        executor.run_keyword("Tap", [x, y])
        executor.run_keyword("Sleep", "1s")
        executor.run_keyword("Input Text Into Current Element", text)
