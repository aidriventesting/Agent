from typing import List, Dict, Optional, Any
from Agent.tools.registry import ToolRegistry
from Agent.tools.base import ToolCategory
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
        self._setup_log_dir()
    
    def _setup_log_dir(self) -> None:
        self.annotated_dir = os.path.join(os.getcwd(), "browser", "annotated")
        os.makedirs(self.annotated_dir, exist_ok=True)
    
    def _save_annotated_image(self, image_base64: str, source: str = "som") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"annotated_{source}_{timestamp}.png"
        filepath = os.path.join(self.annotated_dir, filename)
        
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
        element_source: str = "dom",
        llm_input_format: str = "text",
        screenshot_base64: Optional[str] = None,
        annotated_image_path: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Build DO action messages using tool calling approach.
        
        Args:
            instruction: User instruction
            ui_elements: List of UI elements (from DOM or OmniParser)
            platform: 'mobile' or 'web' - determines system prompt
            element_source: 'dom' or 'visual' - where elements come from
            llm_input_format: 'text' or 'som' - how to send elements to LLM
            screenshot_base64: Screenshot (required for DOM + SoM)
            annotated_image_path: Pre-annotated image from OmniParser (for Visual + SoM)
        """
        # Base system prompt
        is_mobile = platform in ("android", "ios")
        if is_mobile:
            system_content = (
                "You are a MOBILE app test automation engine (Appium).\n"
                "Your job: analyze the instruction and call the appropriate function to interact with the mobile UI.\n"
            )
            
            if element_source == "visual":
                system_content += (
                    "\nUSE VISUAL TOOLS:\n"
                    "- click_visual_element(description): Click element by visual description\n"
                    "- Elements were detected using computer vision (OmniParser)\n"
                )
            else:
                system_content += (
                    "\nUSE LOCATOR TOOLS:\n"
                    "1. FOR TEXT INPUT: input_text(element_index, text) - select from numbered list\n"
                    "2. FOR CLICKING: tap_element(index) - select from numbered list\n"
                    "3. OTHER: scroll_down(), swipe_left/right/up(), long_press(index), hide_keyboard(), go_back()\n"
                )
            
            system_content += (
                "\nIMPORTANT: You are working with MOBILE apps (Android/iOS), NOT web browsers."
            )
        else:
            system_content = (
                "You are a WEB test automation engine.\n"
                "Your job: analyze the instruction and call the appropriate function to interact with the web page.\n"
            )
            
            if element_source == "visual":
                system_content += (
                    "\nUSE VISUAL TOOLS:\n"
                    "- click_visual_element(description): Click by visual description\n"
                    "- input_text_visual(description, text): Input text by visual description\n"
                    "- hover_visual(description): Hover by visual description\n"
                    "- double_click_visual(description): Double click by visual description\n"
                    "- Elements were detected using computer vision (OmniParser)\n"
                )
            else:
                system_content += (
                    "\nUSE LOCATOR TOOLS:\n"
                    "1. FOR TEXT INPUT: input_text(index, text) for <input> or <textarea> elements\n"
                    "2. FOR CLICKING: click_element(index) for <button> or <a> elements\n"
                    "3. FOR DROPDOWN: select_option(index, value) for <select> elements\n"
                    "4. OTHER: scroll_down(), scroll_up(), press_key(), go_back(), hover(), double_click()\n"
                )

            system_content += (
                "\nCRITICAL: Pay attention to element tags when using standard tools:\n"
                "- <input> or <textarea> = text input fields (use input_text tool)\n"
                "- <button> or <a> = clickable elements (use click_element tool)\n"
                "- <select> = dropdown (use select_option tool)\n"
            )
        
        # Build user content based on llm_input_format
        ui_label = "Mobile UI Elements" if is_mobile else "Web Elements"
        
        if llm_input_format == "som" and ui_elements:
            source_info = "detected via computer vision" if element_source == "visual" else "from DOM/accessibility tree"
            
            legend_lines = []
            for idx, elem in enumerate(ui_elements, start=1):
                text = elem.get("text", "").replace("\n", " ").strip()[:40]
                tag = elem.get("class_name", "")
                desc = text if text else (elem.get("aria_label") or elem.get("placeholder") or "")
                legend_lines.append(f"[{idx}] <{tag}> {desc}".strip())
            legend_text = "\n".join(legend_lines)
            
            text_content = (
                f"Instruction: {instruction}\n\n"
                f"The screenshot shows numbered boxes on {ui_label.lower()} ({source_info}).\n"
                f"Use the element NUMBER from this list:\n{legend_text}\n\n"
                f"Select by NUMBER matching the instruction."
            )
            
            # Use pre-annotated image from OmniParser if available (Visual + SoM)
            if annotated_image_path:
                with open(annotated_image_path, "rb") as img_file:
                    annotated_base64 = base64.b64encode(img_file.read()).decode("utf-8")
                self._save_annotated_image(annotated_base64, source="omniparser")
                user_content = [
                    {"type": "text", "text": text_content},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{annotated_base64}"}}
                ]
            # Otherwise render SoM for DOM elements (DOM + SoM)
            elif screenshot_base64:
                from Agent.platforms.collectors.som_renderer import render_som
                annotated_screenshot = render_som(screenshot_base64, ui_elements)
                self._save_annotated_image(annotated_screenshot, source="dom")
                user_content = [
                    {"type": "text", "text": text_content},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{annotated_screenshot}"}}
                ]
            else:
                user_content = f"Instruction: {instruction}\n\nError: SoM mode requires screenshot"
        else:
            if self.platform and ui_elements:
                ui_text = self.platform.render_ui_for_prompt(ui_elements)
            else:
                ui_text = "(no UI elements found)"
            
            source_info = " (detected via OmniParser)" if element_source == "visual" else ""
            user_content = f"Instruction: {instruction}\n\n{ui_label}{source_info}:\n{ui_text}"
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def get_do_tools(
        self, 
        category: str = "mobile",
        element_source: str = "dom"
    ) -> List[Dict[str, Any]]:
        """Return tool definitions for DO actions from the registry.
        
        Returns tool specs in standard format (works with OpenAI, Anthropic, Gemini, etc.)
        
        Args:
            category: Tool category to retrieve ('mobile', 'web', or None for all)
            element_source: 'dom' or 'visual' - filters tools based on capabilities
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
            "Use the verify_visual_match function to report your findings."
        )
        user_content = [
            {"type": "text", "text": f"Verify: {instruction}"},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def get_visual_check_tools(self) -> List[Dict[str, Any]]:
        """Return tool definitions for visual check actions from the registry.
        
        Returns tool specs in standard format (works with OpenAI, Anthropic, Gemini, etc.)
        """
        return self.registry.get_tool_specs(category=ToolCategory.VISUAL)

    def compose_ask_messages(
        self,
        question: str,
        screenshot_base64: str,
        response_format: str = "text",
    ) -> List[Dict[str, Any]]:
        """Build messages for asking AI about current screen."""
        if response_format == "json":
            system_content = (
                "You are a screen analysis assistant. "
                "Answer questions about what you see in the screenshot. "
                "IMPORTANT: Always respond with valid JSON only, no markdown, no explanation outside JSON."
            )
        else:
            system_content = (
                "You are a screen analysis assistant. "
                "Answer questions about what you see in the screenshot. "
                "Be concise and direct."
            )
        
        user_content = [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"}}
        ]
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
