from typing import Any, Dict, List, Optional, Union

from Agent.platforms import DeviceConnector, WebConnectorRF, create_platform
from Agent.ai.llm.facade import UnifiedLLMFacade
from Agent.ai._promptcomposer import AgentPromptComposer
from Agent.utilities.imguploader.imghandler import ImageUploader
from Agent.tools.registry import ToolRegistry
from Agent.tools.base import ToolCategory
from Agent.core.keyword_runner import KeywordRunner
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
        element_source: str = "dom",
        llm_input_format: str = "text",
    ) -> None:
        # Platform connector - create or use provided
        if platform is None:
            self.platform = create_platform(platform_type)
        else:
            self.platform = platform
        
        # Detect platform type from class (no driver access needed)
        self._is_web = isinstance(self.platform, WebConnectorRF)
        platform_name = "web" if self._is_web else "mobile"
        logger.info(f"🌐 Platform: {platform_name}")
        
        # AI components
        self.llm = UnifiedLLMFacade(provider=llm_client, model=llm_model)
        self.image_uploader = ImageUploader(service="auto")
        
        # Tool execution components
        self.tool_registry = ToolRegistry()
        self.executor = KeywordRunner(self.platform)
        
        # Register tools based on platform
        if self._is_web:
            self._register_web_tools()
        else:
            self._register_mobile_tools()
        self._register_visual_tools()
        
        # Create prompt composer with registry (after tools are registered)
        self.prompt_composer = AgentPromptComposer(
            tool_registry=self.tool_registry,
            platform_connector=self.platform
        )
        
        # Element source and LLM input format
        self.element_source = element_source
        self.llm_input_format = llm_input_format
        logger.info(f"🎯 Element source: {element_source}, LLM input format: {llm_input_format}")
    
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
    
    def set_element_source(self, source: str) -> None:
        """Change element source dynamically.
        
        Args:
            source: 'dom' or 'visual'
        """
        if source not in ["dom", "visual"]:
            raise ValueError(f"Invalid element_source: {source}. Choose: dom, visual")
        
        self.element_source = source
        logger.info(f"🔧 Element source changed to: {source}")
    
    def set_llm_input_format(self, format: str) -> None:
        """Change LLM input format dynamically.
        
        Args:
            format: 'text' or 'som'
        """
        if format not in ["text", "som"]:
            raise ValueError(f"Invalid llm_input_format: {format}. Choose: text, som")
        
        self.llm_input_format = format
        logger.info(f"🔧 LLM input format changed to: {format}")
    
    def do(self, instruction: str) -> None:
        """Execute AI-driven action based on natural language instruction.
        
        Args:
            instruction: Natural language instruction (e.g., "tap on login button")
        """
        logger.info(f"🚀 Starting Agent.Do: '{instruction}'")

        if hasattr(self.platform, 'wait_for_page_stable'):
            self.platform.wait_for_page_stable()

        screenshot_base64 = None
        ui_candidates = []
        annotated_image_path = None
        
        # Collect UI elements based on element source
        if self.element_source == "dom":
            ui_candidates = self.platform.collect_ui_candidates()
            logger.debug(f"📋 Collected {len(ui_candidates)} DOM elements")
        elif self.element_source == "visual":
            screenshot_base64 = self.platform.get_screenshot_base64()
            from Agent.ai.vlm._client import OmniParserClient
            from Agent.ai.vlm._parser import OmniParserResultProcessor
            from PIL import Image
            
            client = OmniParserClient()
            image_temp_path, parsed_text = client.parse_image(image_base64=screenshot_base64)
            annotated_image_path = image_temp_path
            
            if parsed_text:
                processor = OmniParserResultProcessor(
                    response_text=parsed_text,
                    image_temp_path=image_temp_path,
                )
                elements_data = processor.get_parsed_ui_elements(element_type="interactive")
                
                with Image.open(image_temp_path) as img:
                    width, height = img.size
                
                for key, data in elements_data.items():
                    bbox_norm = data.get("bbox", [0, 0, 0, 0])
                    x1 = int(bbox_norm[0] * width)
                    y1 = int(bbox_norm[1] * height)
                    x2 = int(bbox_norm[2] * width)
                    y2 = int(bbox_norm[3] * height)
                    
                    element = {
                        "text": data.get("content", ""),
                        "class_name": data.get("type", "unknown"),
                        "bbox": {
                            "x": x1,
                            "y": y1,
                            "width": x2 - x1,
                            "height": y2 - y1
                        },
                        "source": "omniparser",
                        "interactivity": data.get("interactivity", "unknown")
                    }
                    ui_candidates.append(element)
                
            logger.debug(f"👁️ Detected {len(ui_candidates)} visual elements")
        
        # Capture screenshot if needed for SoM mode and not already captured
        if self.llm_input_format == "som" and not screenshot_base64:
            screenshot_base64 = self.platform.get_screenshot_base64()
            logger.debug("📸 Screenshot captured for SoM mode")
        
        # Prepare context for tool execution
        context = {
            "ui_candidates": ui_candidates,
            "instruction": instruction
        }
        
        if screenshot_base64:
            context["screenshot_base64"] = screenshot_base64
        
        # Prepare AI request
        platform_name = self.platform.get_platform()
        tool_category = "web" if self._is_web else "mobile"
        messages = self.prompt_composer.compose_do_messages(
            instruction=instruction,
            ui_elements=ui_candidates,
            platform=platform_name,
            element_source=self.element_source,
            llm_input_format=self.llm_input_format,
            screenshot_base64=screenshot_base64,
            annotated_image_path=annotated_image_path,
        )
        tools = self.prompt_composer.get_do_tools(category=tool_category, element_source=self.element_source)
        logger.debug(f"Tools for {tool_category}: {len(tools)} tools")
        
        if not tools:
            raise RuntimeError(f"No tools registered for platform '{platform_name}'. Check tool registration.")
        
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

        if hasattr(self.platform, 'wait_for_page_stable'):
            self.platform.wait_for_page_stable()

        screenshot_base64 = self.platform.get_screenshot_base64()
        
        # Embed screenshot to Robot Framework log
        self.platform.embed_image_to_log(screenshot_base64)
        logger.debug("Screenshot captured and sent to AI for analysis")
        image_url = self.image_uploader.upload_from_base64(screenshot_base64)

        # Prepare AI request
        messages = self.prompt_composer.compose_visual_check_messages(instruction, image_url)
        tools = self.prompt_composer.get_visual_check_tools()
        logger.debug(f"Visual check tools: {len(tools)} tools")
        
        if not tools:
            raise RuntimeError("No visual tools registered. Check tool registration.")
        
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

    def ask(self, question: str, response_format: str = "text") -> str:
        """Ask AI a question about the current screen.
        
        Args:
            question: Question about what's displayed
            response_format: 'text' or 'json'
        
        Returns:
            AI response as string (or JSON string if format=json)
        """
        import json
        logger.info(f"❓ Agent.Ask: '{question}'")
        screenshot_base64 = self.platform.get_screenshot_base64()
        self.platform.embed_image_to_log(screenshot_base64)
        
        messages = self.prompt_composer.compose_ask_messages(
            question, screenshot_base64, response_format
        )
        
        if response_format == "json":
            response_dict = self.llm.send_ai_request_and_return_response(messages=messages, temperature=0)
            response = json.dumps(response_dict, ensure_ascii=False)
        else:
            response = self.llm.send_ai_request(messages=messages, temperature=0)
        
        logger.info(f"💬 Response: {response[:100]}..." if len(response) > 100 else f"💬 Response: {response}")
        return response

    def find_visual_element(self, description: str, format: str = "center") -> Dict[str, Any]:
        """Find element visually using OmniParser and return bbox.
        
        Args:
            description: Element description (e.g., "Login button")
            format: 'normalized' (0-1), 'pixels', or 'center'
        
        Returns:
            Dict with coordinates based on format
        """
        from Agent.ai.vlm.interface import OmniParserOrchestrator
        
        logger.info(f"🔍 Agent.Find Visual Element: '{description}'")
        screenshot_base64 = self.platform.get_screenshot_base64()
        self.platform.embed_image_to_log(screenshot_base64)
        
        orchestrator = OmniParserOrchestrator(
            llm_provider="openai",
            llm_model="gpt-4o-mini"
        )
        
        result = orchestrator.find_element(
            element_description=description,
            image_base64=screenshot_base64,
            element_type="interactive"
        )
        
        if not result:
            raise AssertionError(f"Element not found: {description}")
        
        bbox_normalized = result["element_data"]["bbox"]
        image_path = result["image_temp_path"]
        
        if format == "normalized":
            response = {
                "x1": bbox_normalized[0],
                "y1": bbox_normalized[1],
                "x2": bbox_normalized[2],
                "y2": bbox_normalized[3]
            }
        elif format == "pixels":
            x1, y1, x2, y2 = orchestrator.bbox_to_pixels_from_image(bbox_normalized, image_path)
            response = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
        else:  # center
            x_center, y_center = orchestrator.get_element_center_coordinates(result)
            response = {"x": x_center, "y": y_center}
        
        logger.info(f"📍 Found: {response}")
        return response

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

