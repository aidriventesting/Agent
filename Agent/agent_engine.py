from typing import Any, Dict, List, Optional

from Agent.platforms import DeviceConnector, create_platform
from Agent.ai.llm.facade import UnifiedLLMFacade
from Agent.ai._promptcomposer import AgentPromptComposer
from Agent.utilities.imguploader.imghandler import ImageUploader
from Agent.tools.registry import ToolRegistry
from Agent.tools.base import ToolCategory
from Agent.core.keyword_runner import KeywordRunner
from Agent.tools.mobile import MOBILE_TOOLS
from Agent.tools.screen.answer_text import AnswerTextTool
from Agent.tools.screen.answer_json import AnswerJsonTool
from Agent.tools.screen.assert_screen import AssertScreenTool
from robot.api import logger


class AgentEngine:
    """Core engine for AI-driven Android test automation."""

    SOM_CONFIG = {
        'visual_annotation': True,
        'text_format': 'compact',
        'output_type': 'text'
    }

    def __init__(
        self, 
        llm_client: str = "openai", 
        llm_model: str = "gpt-4o-mini",
        platform: Optional[DeviceConnector] = None,
        platform_type: str = "auto",
        element_source: str = "accessibility",
        llm_input_format: str = "text",
    ) -> None:
        if platform is None:
            self.platform = create_platform(platform_type)
        else:
            self.platform = platform
        
        logger.info("📱 Platform: mobile")
        
        self.llm = UnifiedLLMFacade(provider=llm_client, model=llm_model)
        self.image_uploader = ImageUploader(service="auto")
        
        self.tool_registry = ToolRegistry()
        self.executor = KeywordRunner(self.platform)
        
        self._register_mobile_tools()
        
        self.prompt_composer = AgentPromptComposer(
            tool_registry=self.tool_registry,
            platform_connector=self.platform
        )
        
        self.tool_registry.register(AnswerTextTool())
        self.tool_registry.register(AnswerJsonTool())
        self.tool_registry.register(AssertScreenTool())
        
        self.element_source = element_source
        self.llm_input_format = llm_input_format
        logger.info(f"🎯 Element source: {element_source}, LLM input format: {llm_input_format}")
    
    def _register_mobile_tools(self) -> None:
        for ToolClass in MOBILE_TOOLS:
            self.tool_registry.register(ToolClass())
        mobile_tools_count = len(self.tool_registry.get_by_category(ToolCategory.MOBILE))
        logger.debug(f"📱 Registered {mobile_tools_count} mobile tools")
    
    # ----------------------- Public API -----------------------
    
    def set_element_source(self, source: str) -> None:
        """Change element source dynamically.
        
        Args:
            source: 'accessibility' or 'vision'
        """
        if source not in ["accessibility", "vision"]:
            raise ValueError(f"Invalid element_source: {source}. Choose: accessibility, vision")
        
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
        if self.element_source == "accessibility":
            ui_candidates = self.platform.collect_ui_candidates()
            logger.debug(f"📋 Collected {len(ui_candidates)} accessibility elements")
        elif self.element_source == "vision":
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
                elements_data = processor.get_parsed_ui_elements(element_type="all")
                
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
        
        logger.info(f"Elements sent to AI: {ui_candidates}")
        
        # Prepare AI request
        platform_name = self.platform.get_platform()
        tool_category = "mobile"
        messages = self.prompt_composer.compose_do_messages(
            instruction=instruction,
            ui_elements=ui_candidates,
            platform=platform_name,
            element_source=self.element_source,
            llm_input_format=self.llm_input_format,
            screenshot_base64=screenshot_base64,
            annotated_image_path=annotated_image_path,
            som_config=self.SOM_CONFIG if self.llm_input_format == "som" else None,
        )
        if annotated_image_path:
            logger.info(f"Annotated image: {annotated_image_path}")
        
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
        
        tool_call = result.get("tool_calls", [{}])[0]
        tool_name = tool_call.get("function", {}).get("name", "unknown")
        tool_args = tool_call.get("function", {}).get("arguments", {})
        logger.info(f"🤖 AI chose: {tool_name}({tool_args})")
        
        # Execute tool
        self._execute_do_from_tool_calls(result, context, instruction)
        logger.info("Agent.Do completed")

    def visual_check(self, instruction: str, min_confidence: float = 0.7) -> None:
        """Execute visual verification based on natural language instruction.
        
        Args:
            instruction: Natural language verification instruction 
                        (e.g., "verify the home screen is displayed")
            min_confidence: Minimum confidence score required (0.0-1.0, default 0.7)
        """
        logger.info(f"👁️ Starting Agent.VisualCheck: '{instruction}' (min_confidence={min_confidence})")

        if hasattr(self.platform, 'wait_for_page_stable'):
            self.platform.wait_for_page_stable()

        screenshot_base64 = self.platform.get_screenshot_base64()
        self.platform.embed_image_to_log(screenshot_base64)
        
        image_url = self.image_uploader.upload_from_base64(screenshot_base64)
        
        tool = self.tool_registry.get_tool_for_query("visual_check")
        if not tool:
            raise AssertionError("visual_check tool not found")
        
        messages = self.prompt_composer.compose_visual_check_messages(instruction, image_url)
        
        result = self.llm.send_ai_request_with_tools(
            messages=messages,
            tools=[tool.to_tool_spec()],
            tool_choice="required",
            temperature=0
        )

        tool_call = result.get("tool_calls", [{}])[0]
        arguments = tool_call.get("function", {}).get("arguments", {})
        
        context = {"min_confidence": min_confidence}
        tool.execute(self.executor, arguments, context)
        
        logger.info("Agent.VisualCheck completed")

    def ask(self, question: str, response_format: str = "text") -> str:
        """Ask AI a question about the current screen.
        
        Args:
            question: Question about what's displayed
            response_format: 'text' or 'json'
        
        Returns:
            AI response as string (or JSON string if format=json)
        """
        logger.info(f"❓ Starting Agent.Ask: '{question}' (format: {response_format})")
        
        if hasattr(self.platform, 'wait_for_page_stable'):
            self.platform.wait_for_page_stable()
        
        screenshot_base64 = self.platform.get_screenshot_base64()
        self.platform.embed_image_to_log(screenshot_base64)
        
        tool = self.tool_registry.get_tool_for_query("ask", response_format=response_format)
        if not tool:
            raise AssertionError(f"No tool found for response_format: {response_format}")
        
        messages = self.prompt_composer.compose_ask_messages(question, screenshot_base64, response_format)
        
        result = self.llm.send_ai_request_with_tools(
            messages=messages,
            tools=[tool.to_tool_spec()],
            tool_choice="required",
            temperature=0
        )
        
        tool_call = result.get("tool_calls", [{}])[0]
        arguments = tool_call.get("function", {}).get("arguments", {})
        
        answer = tool.execute(self.executor, arguments, {})
        logger.info("Agent.Ask completed")
        return answer

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
        
        if hasattr(self.platform, 'wait_for_page_stable'):
            self.platform.wait_for_page_stable()
        
        screenshot_base64 = self.platform.get_screenshot_base64()
        self.platform.embed_image_to_log(screenshot_base64)
        
        orchestrator = OmniParserOrchestrator(
            llm_provider="openai",
            llm_model="gpt-4o-mini"
        )
        
        result = orchestrator.find_element(
            element_description=description,
            image_base64=screenshot_base64,
            element_type="all"
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


