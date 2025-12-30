from typing import Dict, List, Any, Optional, Union
from Agent.tools.base import BaseTool, ToolCategory
from robot.api import logger


class ToolRegistry:
    """Singleton registry for all available agent tools.
    
    Tools can be registered dynamically and retrieved by:
    - name
    - category (mobile, web, screen)
    - all tools
    - action-based selection (filters tools by parameters)
    """
    
    SCREEN_TOOL_SELECTION_RULES = {
        "ask": {
            "text": "answer_question",
            "json": "answer_question_json"
        },
        "visual_check": {
            "default": "assert_screen"
        }
    }
    
    _instance: Optional['ToolRegistry'] = None
    _tools: Dict[str, BaseTool] = {}
    
    def __new__(cls) -> 'ToolRegistry':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._tools = {}
        return cls._instance
    
    def register(self, tool: BaseTool) -> None:
        """Register a tool in the registry."""
        if tool.name in self._tools:
            existing_tool = self._tools[tool.name]
            # TODO: review currently silently overwriting
            if type(existing_tool) == type(tool):
                return
            logger.warn(f"Tool '{tool.name}' already registered with different class. Overwriting.")
        
        self._tools[tool.name] = tool
        logger.debug(f"Registered tool: {tool.name} ({tool.category})")
    
    def get(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)
    
    def get_all(self) -> List[BaseTool]:
        return list(self._tools.values())
    
    def get_by_category(self, category: Union[ToolCategory, str]) -> List[BaseTool]:
        """Get all tools for a specific category.
        
        Args:
            category: ToolCategory enum or string ('mobile', 'web', 'visual')
        """
        # Support both enum and string for convenience
        if isinstance(category, str):
            category_value = category
        else:
            category_value = category.value
        
        return [tool for tool in self._tools.values() if tool.category.value == category_value]
    
    def get_tool_specs(self, category: Optional[Union[ToolCategory, str]] = None) -> List[Dict[str, Any]]:
        """Get tool calling specs (standard format used by OpenAI/Anthropic/Gemini/etc).
        
        This returns tools in the standard function calling format that all major
        LLM providers now support (format originally from OpenAI, now industry standard).
        
        Args:
            category: Optional filter by ToolCategory or string
        """
        tools = self.get_by_category(category) if category else self.get_all()
        return [tool.to_tool_spec() for tool in tools]
    
    def get_tools_for_source(self, category: Union[ToolCategory, str], element_source: str) -> List[BaseTool]:
        """Get tools filtered by element source.
        
        Args:
            category: ToolCategory or string ('mobile')
            element_source: 'accessibility' or 'vision'
        """
        all_tools = self.get_by_category(category)
        
        if element_source == "vision":
            return [
                tool for tool in all_tools
                if not tool.has_coordinates_alternative
            ]
        
        else:
            return [
                tool for tool in all_tools 
                if not (tool.works_on_coordinates and not tool.works_on_locator)
            ]
    
    def get_tool_for_query(self, query_type: str, **kwargs) -> Optional[BaseTool]:
        """Get single tool based on query type and parameters.
        
        Args:
            query_type: Query type (e.g., "ask", "visual_check")
            **kwargs: Parameters to filter tool (e.g., response_format="json")
        
        Returns:
            Single tool matching criteria or None if not found
        
        Example:
            tool = registry.get_tool_for_query("ask", response_format="json")
            tool = registry.get_tool_for_query("visual_check")
        """
        rules = self.SCREEN_TOOL_SELECTION_RULES.get(query_type)
        if not rules:
            logger.warn(f"No selection rules found for query: {query_type}")
            return None
        
        if query_type == "ask":
            format_key = kwargs.get("response_format", "text")
            tool_name = rules.get(format_key)
        elif query_type == "visual_check":
            tool_name = rules.get("default")
        else:
            return None
        
        if not tool_name:
            logger.warn(f"No tool found for query: {query_type} with kwargs: {kwargs}")
            return None
        
        return self.get(tool_name)
    
    def clear(self) -> None:
        self._tools.clear()
    
    def list_tools(self) -> str:
        if not self._tools:
            return "No tools registered"
        
        lines = ["Registered Tools:"]
        for category in ToolCategory:
            category_tools = self.get_by_category(category)
            if category_tools:
                lines.append(f"\n{category.value.upper()}:")
                for tool in category_tools:
                    lines.append(f"  - {tool.name}: {tool.description}")
        
        return "\n".join(lines)

