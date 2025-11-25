from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class PressKeyTool(BaseTool):
    """Press a keyboard key (Enter, Escape, Tab, Arrow keys, etc.)."""
    
    @property
    def name(self) -> str:
        return "press_key"
    
    @property
    def description(self) -> str:
        return "Press a keyboard key. Common keys: Enter, Escape, Tab, ArrowUp, ArrowDown, ArrowLeft, ArrowRight, Backspace, Delete. Use this to submit forms (Enter), close modals (Escape), navigate (Arrow keys), or clear input (Backspace)"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.WEB
    
    @property
    def works_on_locator(self) -> bool:
        return False
    
    @property
    def works_on_visual(self) -> bool:
        return False
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "The key to press. Common values: Enter, Escape, Tab, ArrowUp, ArrowDown, ArrowLeft, ArrowRight, Backspace, Delete, Space",
                    "enum": ["Enter", "Escape", "Tab", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Backspace", "Delete", "Space"]
                }
            },
            "required": ["key"]
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        key = arguments["key"]
        
        logger.info(f"⌨️ Pressing key: {key}")
        
        # Browser library: Press Keys selector *keys
        executor.run_keyword("Press Keys", "body", key)
        logger.info(f"✅ Key pressed")

