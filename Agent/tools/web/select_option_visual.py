from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from Agent.ai.vlm.interface import OmniParserOrchestrator
from robot.api import logger


class SelectOptionVisualTool(BaseTool):
    """Select option from dropdown using visual detection (OmniParser) for WEB.
    
    Two-step process:
    1. Click dropdown by visual description
    2. Click option by visual description
    """
    
    @property
    def name(self) -> str:
        return "select_option_visual"
    
    @property
    def description(self) -> str:
        return "Select option from dropdown by VISUAL description - USE ONLY when dropdown is NOT in the list or has no clear locator"
    
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
                "dropdown_description": {
                    "type": "string",
                    "description": "Visual description of the dropdown/select element"
                },
                "option_description": {
                    "type": "string",
                    "description": "Visual description of the option to select"
                }
            },
            "required": ["dropdown_description", "option_description"]
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        dropdown_description = arguments["dropdown_description"]
        option_description = arguments["option_description"]
        
        # Get screenshot from context
        screenshot_base64 = context.get("screenshot_base64")
        
        if not screenshot_base64:
            raise AssertionError("screenshot_base64 not provided in context for visual select")
        
        logger.debug(f"Visual select: dropdown='{dropdown_description}', option='{option_description}'")
        
        orchestrator = OmniParserOrchestrator()
        
        # Step 1: Find and click dropdown
        result = orchestrator.find_element(
            element_description=dropdown_description,
            image_base64=screenshot_base64
        )
        
        if not result:
            raise AssertionError(f"Dropdown '{dropdown_description}' not found")
        
        x_center, y_center = OmniParserOrchestrator.get_element_center_coordinates(result)
        
        logger.debug(f"Clicking dropdown at coordinates: ({x_center}, {y_center})")
        executor.run_keyword("Mouse Button", "click", x_center, y_center)
        
        # Wait for dropdown to open
        executor.run_keyword("Sleep", "0.5s")
        
        # Step 2: Capture new screenshot and find option
        screenshot_base64_2 = executor.platform.get_screenshot_base64()
        
        result_option = orchestrator.find_element(
            element_description=option_description,
            image_base64=screenshot_base64_2
        )
        
        if not result_option:
            raise AssertionError(f"Option '{option_description}' not found")
        
        x_opt, y_opt = OmniParserOrchestrator.get_element_center_coordinates(result_option)
        
        logger.debug(f"Clicking option at coordinates: ({x_opt}, {y_opt})")
        executor.run_keyword("Mouse Button", "click", x_opt, y_opt)
