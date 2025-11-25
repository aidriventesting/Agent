from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class InputTextTool(BaseTool):
    """Clear and input text into a web UI element."""
    
    @property
    def name(self) -> str:
        return "input_text"
    
    @property
    def description(self) -> str:
        return "REQUIRED for text input actions. Input text into a text field using element index. Use this tool when instruction contains 'input', 'type', 'enter text', or 'fill'"
    
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
                    "description": "The index number of the TEXT FIELD element from the UI elements list (1-based). Find the text field in the numbered list below.",
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
        
        class_name = element.get('class_name', '')
        elem_type = element.get('type', '')
        
        valid_input_elements = ['input', 'textarea']
        valid_input_types = ['text', 'search', 'email', 'password', 'tel', 'url', 'number', '']
        
        if class_name not in valid_input_elements:
            raise AssertionError(
                f"Cannot input text: element at index {element_index} is a '{class_name}', not a text input field. "
                f"Expected: input or textarea. Element: {element}"
            )
        
        if class_name == 'input' and elem_type and elem_type not in valid_input_types:
            raise AssertionError(
                f"Cannot input text: input element at index {element_index} has type '{elem_type}' which doesn't accept text. "
                f"Expected types: {valid_input_types}. Element: {element}"
            )
        
        locator = executor.build_locator(element)
        
        logger.info(f"⌨️ Inputting text into element at index {element_index}")
        logger.info(f"Built locator: {locator} from element: {element}")
        logger.info(f"Text to input: '{text}'")
        
        executor.run_keyword("Fill Text", locator, text)
        logger.info(f"✅ Input text completed")

