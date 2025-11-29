from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from Agent.ai.vlm.interface import OmniParserOrchestrator
from robot.api import logger


class ClearTextVisualTool(BaseTool):
    """Clear text from input field using visual detection (OmniParser) for WEB.
    
    Finds input field, triple-clicks to select all, and clears.
    """
    
    @property
    def name(self) -> str:
        return "clear_text_visual"
    
    @property
    def description(self) -> str:
        return "Clear text from input field by VISUAL description - USE ONLY when field is NOT in the list or has no clear locator"
    
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
                    "description": "Visual description of the input field to clear"
                }
            },
            "required": ["element_description"]
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        element_description = arguments["element_description"]
        
        # Get screenshot from context
        screenshot_base64 = context.get("screenshot_base64")
        
        if not screenshot_base64:
            raise AssertionError("screenshot_base64 not provided in context for visual clear")
        
        logger.debug(f"Visual clear text: '{element_description}'")
        
        orchestrator = OmniParserOrchestrator()
        result = orchestrator.find_element(
            element_description=element_description,
            image_base64=screenshot_base64
        )
        
        if not result:
            raise AssertionError(f"Element '{element_description}' not found")
        
        x_center, y_center = OmniParserOrchestrator.get_element_center_coordinates(result)
        
        logger.debug(f"Clearing text at coordinates: ({x_center}, {y_center})")
        
        # Triple-click to select all text
        executor.run_keyword("Mouse Button", "click", x_center, y_center)
        executor.run_keyword("Mouse Button", "click", x_center, y_center)
        executor.run_keyword("Mouse Button", "click", x_center, y_center)
        
        # Clear with Backspace
        executor.run_keyword("Keyboard Input", "press", "Backspace")
