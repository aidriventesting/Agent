from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from Agent.ai.vlm.interface import OmniParserOrchestrator
from robot.api import logger


class InputTextVisualTool(BaseTool):
    """Input text into element using visual detection (OmniParser) for WEB.
    
    Alternative to input_text when locators are unreliable.
    Uses computer vision to find the input field and types text.
    """
    
    @property
    def name(self) -> str:
        return "input_text_visual"
    
    @property
    def description(self) -> str:
        return "Input text into element by VISUAL description - USE ONLY when standard input_text fails or for elements without clear locators"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.WEB
    
    @property
    def works_on_locator(self) -> bool:
        return False
    
    @property
    def works_on_visual(self) -> bool:
        return True
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "element_description": {
                    "type": "string",
                    "description": "Visual description of the input field (e.g., 'search bar at top', 'email input field')"
                },
                "text": {
                    "type": "string",
                    "description": "The text to input"
                }
            },
            "required": ["element_description", "text"]
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        element_description = arguments["element_description"]
        text = arguments["text"]
        
        # Get screenshot from context
        screenshot_base64 = context.get("screenshot_base64")
        
        if not screenshot_base64:
            raise AssertionError("screenshot_base64 not provided in context for visual input")
        
        logger.debug(f"Visual input: '{element_description}' -> '{text}'")
        
        orchestrator = OmniParserOrchestrator()
        result = orchestrator.find_element(
            element_description=element_description,
            image_base64=screenshot_base64
        )
        
        if not result:
            raise AssertionError(f"Element '{element_description}' not found")
        
        x_center, y_center = OmniParserOrchestrator.get_element_center_coordinates(result)
        
        logger.debug(f"Clicking to focus at coordinates: ({x_center}, {y_center})")
        # Click to focus
        executor.run_keyword("Mouse Button", "click", x_center, y_center)
        
        # Type text
        logger.debug(f"Typing text: '{text}'")
        executor.run_keyword("Keyboard Input", "type", text)
