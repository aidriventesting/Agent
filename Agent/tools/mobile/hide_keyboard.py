from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class HideKeyboardTool(BaseTool):
    """Hide the software keyboard on the mobile device.
    
    Works on both Android and iOS. No arguments needed for cross-platform compatibility.
    Very useful after inputting text to reveal UI elements hidden by the keyboard.
    """
    
    @property
    def name(self) -> str:
        return "hide_keyboard"
    
    @property
    def description(self) -> str:
        return "Hide the software keyboard on the mobile device"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.MOBILE
    
    @property
    def works_on_locator(self) -> bool:
        return False  # Global device action
    
    @property
    def works_on_coordinates(self) -> bool:
        return False  # System-level action
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Brief explanation (1 sentence) of WHY you chose this action"
                }
            },
            "required": []
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        reasoning = arguments.get("reasoning", "No reasoning provided")
        logger.info(f"🧠 AI reasoning: {reasoning}")
        # Hide Keyboard without arguments for iOS/Android compatibility
        executor.run_keyword("Hide Keyboard")

