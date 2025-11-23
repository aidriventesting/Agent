from abc import ABC, abstractmethod
from typing import Any, Dict, Protocol
from enum import Enum


class ToolCategory(Enum):
    """Enum for tool categories - type-safe categories."""
    MOBILE = "mobile"
    WEB = "web"
    VISUAL = "visual"


class ExecutorProtocol(Protocol):
    """Protocol defining what an executor must implement for tool execution."""
    
    def run_keyword(self, keyword_name: str, *args: Any) -> Any:
        """Execute a platform-specific keyword/action."""
        ...
    
    def build_locator(self, element: Dict[str, Any]) -> str:
        """Build a locator string from element attributes."""
        ...


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
        """Tool category: ToolCategory.MOBILE, ToolCategory.WEB, or ToolCategory.VISUAL."""
        pass
    
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

