from typing import List, Dict, Optional, Any
from Agent.tools.registry import ToolRegistry
from Agent.tools.base import ToolCategory
from Agent.platforms.grounding import SomComposer
from robot.api import logger
import base64
import os
from datetime import datetime


class AgentPromptComposer:
    """Builds prompts for agent actions and visual checks."""

    def __init__(
        self, 
        tool_registry: Optional[ToolRegistry] = None,
        platform_connector: Optional[Any] = None
    ) -> None:
        self.registry = tool_registry or ToolRegistry()
        self.platform = platform_connector
        self._annotated_dir = None
    
    def _get_annotated_dir(self) -> str:
        if self._annotated_dir is None:
            from Agent.utilities._logdir import set_artifacts_subdir
            self._annotated_dir = set_artifacts_subdir("RF_Agent/Annotated")
        return self._annotated_dir
    
    def _save_annotated_image(self, image_base64: str, source: str = "som") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"annotated_{source}_{timestamp}.png"
        filepath = os.path.join(self._get_annotated_dir(), filename)
        
        image_bytes = base64.b64decode(image_base64)
        with open(filepath, "wb") as f:
            f.write(image_bytes)
        
        logger.info(f"📸 Saved annotated image: {filepath}")
        return filepath

    def compose_do_messages(
        self,
        instruction: str,
        ui_elements: Optional[List[Dict[str, Any]]] = None,
        platform: str = "mobile",
        element_source: str = "accessibility",
        llm_input_format: str = "text",
        screenshot_base64: Optional[str] = None,
        annotated_image_path: Optional[str] = None,
        som_config: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Build DO action messages using tool calling approach.
        
        Args:
            instruction: User instruction
            ui_elements: List of UI elements
            platform: 'android' or 'ios'
            element_source: 'accessibility' or 'vision'
            llm_input_format: 'text' or 'som'
            screenshot_base64: Screenshot (required for SoM mode)
            annotated_image_path: Pre-annotated image from OmniParser
            som_config: SoM configuration dict {
                'visual_annotation': True/False,
                'text_format': 'compact'/'detailed'/'minimal',
                'output_type': 'text'/'json',
                'include_screenshot': True/False
            }
        """
        # Base system prompt
        is_mobile = platform in ("android", "ios")
        if is_mobile:
            system_content = (
                "You are a MOBILE app test automation engine (Appium).\n"
                "Your job: analyze the instruction and call the appropriate function to interact with the mobile UI.\n"
                "\n⚠️ CRITICAL TOOL SELECTION:\n"
                "- IF instruction says 'click', 'tap', 'select', 'choose' → ALWAYS use tap_element(index)\n"
                "- scroll/swipe tools are ONLY for navigation - NEVER use them to click/tap\n"
                "\n⚠️ IMPORTANT:\n"
                "ALL tools have a 'reasoning' parameter. You MUST provide a brief explanation (1 sentence) of:\n"
                "- Which element you chose and why (for element-based actions)\n"
                "- Why this action matches the instruction (for all actions)\n"
                "Example: {\"element_index\": 5, \"reasoning\": \"Clicking the search icon at the top right to open search\"}\n"
            )
            
            if element_source == "vision":
                system_content += (
                    "\nELEMENTS DETECTED VIA COMPUTER VISION (OmniParser):\n"
                    "- tap_element(element_index): Click element by INDEX from numbered list\n"
                    "- input_text(element_index, text): Type text into element by INDEX\n"
                    "- The screenshot shows NUMBERED bounding boxes - use those numbers!\n"
                )
            else:
                system_content += (
                    "\n🎯 TOOL SELECTION RULES:\n"
                    "1. IF element is VISIBLE in the UI list → USE tap_element(index) to click it\n"
                    "2. IF you need to type text → USE input_text(index, text)\n"
                    "3. IF target element is NOT in the list → USE scroll_down/swipe_up to reveal it\n"
                    "4. NEVER use scroll/swipe when the target element is already visible!\n"
                    "5. scroll_down, swipe_up, swipe_left, swipe_right are ONLY for navigation - NOT for clicking!\n"
                    "6. To click ANY element from the list, ALWAYS use tap_element(index)\n"
                    "\nCRITICAL NOTES:\n"
                    "- The screenshot shows NUMBERED bounding boxes. Use what you SEE in the image!\n"
                    "- tap_element() clicks by COORDINATES - you CAN tap ANY visible element, even if not marked as clickable\n"
                    "- If you see the target element on screen, CLICK IT directly with tap_element()\n"
                    "- Search suggestions, list items, buttons = ALL require tap_element()\n"
                )
            
            system_content += (
                "\nIMPORTANT: You are working with MOBILE apps (Android/iOS), NOT web browsers."
            )
        # else:
        #     system_content = (
        #         "You are a WEB test automation engine.\n"
        #         "Your job: analyze the instruction and call the appropriate function to interact with the web page.\n"
        #     )
        #     
        #     if element_source == "vision":
        #         system_content += (
        #             "\nUSE VISUAL TOOLS:\n"
        #             "- click_visual_element(description): Click by visual description\n"
        #             "- input_text_visual(description, text): Input text by visual description\n"
        #             "- hover_visual(description): Hover by visual description\n"
        #             "- double_click_visual(description): Double click by visual description\n"
        #             "- Elements were detected using computer vision (OmniParser)\n"
        #         )
        #     else:
        #         system_content += (
        #             "\nUSE LOCATOR TOOLS:\n"
        #             "1. FOR TEXT INPUT: input_text(index, text) for <input> or <textarea> elements\n"
        #             "2. FOR CLICKING: click_element(index) for <button> or <a> elements\n"
        #             "3. FOR DROPDOWN: select_option(index, value) for <select> elements\n"
        #             "4. OTHER: scroll_down(), scroll_up(), press_key(), go_back(), hover(), double_click()\n"
        #         )
        # 
        #     system_content += (
        #         "\nCRITICAL: Pay attention to element tags when using standard tools:\n"
        #         "- <input> or <textarea> = text input fields (use input_text tool)\n"
        #         "- <button> or <a> = clickable elements (use click_element tool)\n"
        #         "- <select> = dropdown (use select_option tool)\n"
        #     )
        
        # Build user content based on llm_input_format
        # ui_label = "Mobile UI Elements" if is_mobile else "Web Elements"
        ui_label = "Mobile UI Elements"
        
        if llm_input_format == "som" and ui_elements:
            source_info = "detected via computer vision" if element_source == "vision" else "from accessibility tree"
            
            # Get screen dimensions
            screen_size = self.platform.get_screen_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']
            
            # Default SoM config
            if som_config is None:
                som_config = {
                    'visual_annotation': True,
                    'text_format': 'compact',
                    'output_type': 'text'
                }
            
            # Use SomComposer to generate SoM components
            som_composer = SomComposer(platform, screen_width, screen_height)
            
            # Use pre-annotated image from OmniParser if available (Visual + SoM)
            if annotated_image_path:
                with open(annotated_image_path, "rb") as img_file:
                    annotated_base64 = base64.b64encode(img_file.read()).decode("utf-8")
                self._save_annotated_image(annotated_base64, source="omniparser")
                
                # Generate text legend using SomComposer
                som_result = som_composer.compose(
                    screenshot_base64=None,
                    elements=ui_elements,
                    config={**som_config, 'visual_annotation': False}
                )
                
                if som_config.get('output_type') == 'json':
                    legend_text = som_result.get('elements_json', '')
                else:
                    legend_text = som_result.get('text_legend', '')
                
                text_content = (
                    f"Instruction: {instruction}\n\n"
                    f"ANNOTATED SCREENSHOT: Each UI element has a GREEN BOX with its ID NUMBER in a small rectangle at the top-left.\n"
                    f"ELEMENT LIST ({source_info}):\n{legend_text}\n\n"
                    f"IMPORTANT: Select the element by its ID NUMBER that best matches the instruction."
                )
                
                user_content = [
                    {"type": "text", "text": text_content},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{annotated_base64}"}}
                ]
            # Otherwise render SoM for DOM elements (DOM + SoM)
            elif screenshot_base64:
                som_result = som_composer.compose(
                    screenshot_base64=screenshot_base64,
                    elements=ui_elements,
                    config=som_config
                )
                
                annotated_screenshot = som_result.get('annotated_image_base64', '')
                
                if som_config.get('output_type') == 'json':
                    legend_text = som_result.get('elements_json', '')
                else:
                    legend_text = som_result.get('text_legend', '')
                
                if annotated_screenshot:
                    self._save_annotated_image(annotated_screenshot, source="dom")
                
                text_content = (
                    f"Instruction: {instruction}\n\n"
                    f"ANNOTATED SCREENSHOT: Each UI element has a GREEN BOX with its ID NUMBER in a small rectangle at the top-left.\n"
                    f"ELEMENT LIST ({source_info}):\n{legend_text}\n\n"
                    f"IMPORTANT: Select the element by its ID NUMBER that best matches the instruction."
                )
                
                if annotated_screenshot:
                    user_content = [
                        {"type": "text", "text": text_content},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{annotated_screenshot}"}}
                    ]
                else:
                    user_content = text_content
            else:
                user_content = f"Instruction: {instruction}\n\nError: SoM mode requires screenshot"
        else:
            if self.platform and ui_elements:
                ui_text = self.platform.render_ui_for_prompt(ui_elements)
            else:
                ui_text = "(no UI elements found)"
            
            source_info = " (detected via OmniParser)" if element_source == "vision" else ""
            user_content = f"Instruction: {instruction}\n\n{ui_label}{source_info}:\n{ui_text}"
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def get_do_tools(
        self, 
        category: str = "mobile",
        element_source: str = "accessibility"
    ) -> List[Dict[str, Any]]:
        """Return tool definitions for DO actions from the registry.
        
        Args:
            category: Tool category ('mobile')
            element_source: 'accessibility' or 'vision'
        """
        filtered_tools = self.registry.get_tools_for_source(category, element_source)
        return [tool.to_tool_spec() for tool in filtered_tools]

    def compose_visual_check_messages(
        self,
        instruction: str,
        image_url: str,
    ) -> List[Dict[str, Any]]:
        """Build visual check messages using tool calling approach."""
        system_content = (
            "You are a mobile app visual verification engine. "
            "Analyze the screenshot and verify if it matches the instruction. "
            "Use the assert_screen function to report your findings."
        )
        user_content = [
            {"type": "text", "text": f"Verify: {instruction}"},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]


    def compose_ask_messages(
        self,
        question: str,
        screenshot_base64: str,
        response_format: str = "text"
    ) -> List[Dict[str, Any]]:
        """Build messages for asking AI about current screen using tool calling."""
        if response_format == "json":
            instruction = "Use the answer_question_json function to provide your answer as a JSON object."
        else:
            instruction = "Use the answer_question function to provide your answer as text."
        
        system_content = (
            "You are a screen analysis assistant. "
            "Answer questions about what you see in the screenshot. "
            f"{instruction}"
        )
        
        user_content = [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"}}
        ]
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
