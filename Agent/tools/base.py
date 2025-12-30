from abc import ABC, abstractmethod
from typing import Any, Dict
from enum import Enum
from Agent.core.interfaces import ExecutorProtocol


class ToolCategory(Enum):
    MOBILE = "mobile"
    WEB = "web"
    SCREEN = "screen"


class BaseTool(ABC):
    """Base class for all agent tools (mobile and web).
    
    Each tool defines:
    - name: The function name for LLM tool calling
    - description: What the tool does (for LLM understanding)
    - parameters_schema: OpenAI function calling parameter schema
    - execute: How to execute the tool action
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name used in LLM function calling."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this tool does."""
        pass
    
    @property
    @abstractmethod
    def category(self) -> ToolCategory:
        """Tool category: ToolCategory.MOBILE, ToolCategory.WEB, or ToolCategory.SCREEN."""
        pass
    
    @property
    def works_on_locator(self) -> bool:
        """Does this tool work with XML locator?
        
        Returns:
            True: Tool can work with XML element locator
            False: Tool doesn't work with XML locators
        
        Default: False (only action tools need to override)
        """
        return False
    
    @property
    def works_on_coordinates(self) -> bool:
        """Can this tool work with coordinates (x, y)?
        
        Returns:
            True: Tool can use coordinates from bounding box
            False: Tool cannot work with coordinates
        
        Default: False (only action tools need to override)
        """
        return False
    
    @property
    def has_coordinates_alternative(self) -> bool:
        """Does this tool have a coordinates-based alternative?
        
        Returns:
            True: This tool has a coordinates-based alternative
            False: This tool has no coordinates alternative
        
        Default: False
        
        Used for filtering in coordinates mode.
        """
        return False
    
    @abstractmethod
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Return OpenAI function calling parameter schema."""
        pass
    
    @abstractmethod
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        """Execute the tool action.
        
        Args:
            executor: Platform executor (mobile/web)
            arguments: Parsed arguments from LLM tool call
            context: Additional context (ui_candidates, instruction, etc.)
        """
        pass
    
    def to_tool_spec(self) -> Dict[str, Any]:
        """Convert tool to standard function calling format.
        
        Returns tool spec in the standard format used by OpenAI/Anthropic/etc.
        All major LLM providers now support this format (originated from OpenAI).
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.get_parameters_schema()
            }
        }

