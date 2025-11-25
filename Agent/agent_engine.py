from typing import Any, Dict, List, Optional, Union

from Agent.platforms import DeviceConnector, WebConnectorRF, create_platform
from Agent.ai.llm.facade import UnifiedLLMFacade
from Agent.ai._promptcomposer import AgentPromptComposer
from Agent.utilities.imguploader.imghandler import ImageUploader
from Agent.tools.registry import ToolRegistry
from Agent.tools.base import ToolCategory
from Agent.executors.mobile_executor import MobileExecutor
from Agent.executors.web_executor import WebExecutor
from Agent.tools.mobile import MOBILE_TOOLS
from Agent.tools.web import WEB_TOOLS
from Agent.tools.visual import VISUAL_TOOLS
from robot.api import logger


class AgentEngine:
    """Core engine for AI-driven test automation.
    
    Orchestrates the complete Agent.Do and Agent.VisualCheck flows:
    - Capturing UI context and screenshots
    - Composing AI prompts and calling LLMs
    - Tool-based action execution and visual verification
    
    This is the main orchestrator that coordinates platform connectors,
    AI services, tool registry, and executors.
    """

    def __init__(
        self, 
        llm_client: str = "openai", 
        llm_model: str = "gpt-4o-mini",
        platform: Optional[Union[DeviceConnector, WebConnectorRF]] = None,
        platform_type: str = "auto",
        click_mode: str = "hybrid"
    ) -> None:
        # Platform connector - create or use provided
        if platform is None:
            self.platform = create_platform(platform_type)
        else:
            self.platform = platform
        
        # Detect platform type
        platform_name = self.platform.get_platform()
        logger.info(f"🌐 Platform detected: {platform_name}")
        
        # AI components
        self.llm = UnifiedLLMFacade(provider=llm_client, model=llm_model)
        self.prompt_composer = AgentPromptComposer(
            platform_connector=self.platform
        )
        self.image_uploader = ImageUploader(service="auto")
        
        # Tool execution components - create appropriate executor
        self.tool_registry = ToolRegistry()
        if platform_name == "web":
            self.executor = WebExecutor(self.platform)
        else:
            self.executor = MobileExecutor(self.platform)
        
        # Register tools based on platform
        if platform_name == "web":
            self._register_web_tools()
        else:
            self._register_mobile_tools()
        self._register_visual_tools()
        
        # Click strategy
        self.click_mode = click_mode
        logger.info(f"🎯 Click mode: {click_mode}")
    
    def _register_mobile_tools(self) -> None:
        """Register all mobile tools in the registry."""
        for ToolClass in MOBILE_TOOLS:
            self.tool_registry.register(ToolClass())
        
        mobile_tools_count = len(self.tool_registry.get_by_category(ToolCategory.MOBILE))
        logger.debug(f"📱 Registered {mobile_tools_count} mobile tools")
    
    def _register_web_tools(self) -> None:
        """Register all web tools in the registry."""
        for ToolClass in WEB_TOOLS:
            self.tool_registry.register(ToolClass())
        
        web_tools_count = len(self.tool_registry.get_by_category(ToolCategory.WEB))
        logger.debug(f"🌐 Registered {web_tools_count} web tools")
    
    def _register_visual_tools(self) -> None:
        """Register all visual verification tools in the registry."""
        for ToolClass in VISUAL_TOOLS:
            self.tool_registry.register(ToolClass())
        
        visual_tools_count = len(self.tool_registry.get_by_category(ToolCategory.VISUAL))
        logger.debug(f"👁️ Registered {visual_tools_count} visual tools")
    
    # ----------------------- Public API -----------------------
    
    def set_click_mode(self, mode: str) -> None:
        """Change click mode dynamically during test execution.
        
        Args:
            mode: 'xml', 'visual', or 'hybrid'
        """
        if mode not in ["xml", "visual", "hybrid"]:
            raise ValueError(f"Invalid click_mode: {mode}. Choose: xml, visual, hybrid")
        
        self.click_mode = mode
        logger.info(f"🔧 Click mode changed to: {mode}")
    
    def do(self, instruction: str) -> None:
        """Execute AI-driven action based on natural language instruction.
        
        Args:
            instruction: Natural language instruction (e.g., "tap on login button")
        """
        logger.info(f"🚀 Starting Agent.Do: '{instruction}'")

        # Collect UI context
        ui_candidates = self.platform.collect_ui_candidates()
        
        # Capture screenshot if needed (based on click_mode)
        screenshot_base64 = None
        if self.click_mode in ["visual", "hybrid"]:
            screenshot_base64 = self.platform.get_screenshot_base64()
            logger.debug(f"📸 Screenshot captured (mode: {self.click_mode})")
        else:
            logger.debug(f"⚡ Screenshot skipped (mode: {self.click_mode})")
        
        # Prepare context for tool execution
        context = {
            "ui_candidates": ui_candidates,
            "instruction": instruction
        }
        
        if screenshot_base64:
            context["screenshot_base64"] = screenshot_base64
        
        # Prepare AI request
        platform_name = self.platform.get_platform()
        messages = self.prompt_composer.compose_do_messages(
            instruction=instruction,
            ui_elements=ui_candidates,
            platform=platform_name,
            click_mode=self.click_mode
        )
        tools = self.prompt_composer.get_do_tools(category=platform_name, click_mode=self.click_mode)
        
        # Call AI
        result = self.llm.send_ai_request_with_tools(
            messages=messages,
            tools=tools,
            tool_choice="required",
            temperature=0
        )

        logger.debug(f"AI response: {result}")
        
        # Execute tool
        self._execute_do_from_tool_calls(result, context, instruction)
        logger.info("✅ Agent.Do completed")

    def visual_check(self, instruction: str) -> None:
        """Execute visual verification based on natural language instruction.
        
        Args:
            instruction: Natural language verification instruction 
                        (e.g., "verify the home screen is displayed")
        """
        logger.info(f"👁️ Starting Agent.VisualCheck: '{instruction}'")
        screenshot_base64 = self.platform.get_screenshot_base64()
        
        # Embed screenshot to Robot Framework log
        self.platform.embed_image_to_log(screenshot_base64)
        logger.debug("Screenshot captured and sent to AI for analysis")
        image_url = self.image_uploader.upload_from_base64(screenshot_base64)

        # Prepare AI request
        messages = self.prompt_composer.compose_visual_check_messages(instruction, image_url)
        tools = self.prompt_composer.get_visual_check_tools()
        
        # Call AI
        result = self.llm.send_ai_request_with_tools(
            messages=messages,
            tools=tools,
            tool_choice="required",
            temperature=0
        )

        logger.debug("Executing visual verification...")
        self._execute_visual_check_from_tool_calls(result)
        logger.debug("Agent.VisualCheck completed successfully")

    # ----------------------- Internals -----------------------
    
    def _execute_do_from_tool_calls(
        self, 
        result: Dict[str, Any],
        context: Dict[str, Any],
        instruction: str
    ) -> None:
        """Execute actions from tool calls returned by the LLM using the tool registry."""
        tool_calls = result.get("tool_calls", [])
        
        if not tool_calls:
            logger.error("No tool calls in response")
            raise AssertionError("AI did not return any tool calls")
        
        # Execute the first tool call (typically there's only one for DO actions)
        tool_call = tool_calls[0]
        function_name = tool_call["function"]["name"]
        arguments = tool_call["function"]["arguments"]
        
        logger.debug(f"⚙️ Executing tool: {function_name} with args: {arguments}")
        
        # Get tool from registry
        tool = self.tool_registry.get(function_name)
        if not tool:
            raise AssertionError(f"Unknown tool: {function_name}")
        
        # Execute the tool
        tool.execute(self.executor, arguments, context)

    def _execute_visual_check_from_tool_calls(self, result: Dict[str, Any]) -> None:
        """Execute visual check from tool calls returned by the LLM using the tool registry."""
        tool_calls = result.get("tool_calls", [])
        
        if not tool_calls:
            logger.error("No tool calls in visual check response")
            raise AssertionError("AI did not return any tool calls for visual verification")
        
        # Extract the first tool call (typically verify_visual_match)
        tool_call = tool_calls[0]
        function_name = tool_call["function"]["name"]
        arguments = tool_call["function"]["arguments"]
        
        logger.debug(f"⚙️ Executing visual tool: {function_name}")
        
        # Get tool from registry
        tool = self.tool_registry.get(function_name)
        if not tool:
            raise AssertionError(f"Unknown visual tool: {function_name}")
        
        # Prepare context for tool execution (visual tools don't need ui_candidates)
        context = {}
        
        # Execute the visual tool (will handle logging and assertions)
        tool.execute(self.executor, arguments, context)

