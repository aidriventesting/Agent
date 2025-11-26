from typing import List, Dict, Optional, Any
from Agent.tools.registry import ToolRegistry
from Agent.tools.base import ToolCategory


class AgentPromptComposer:
    """Builds prompts for agent actions and visual checks."""

    def __init__(
        self, 
        tool_registry: Optional[ToolRegistry] = None,
        platform_connector: Optional[Any] = None
    ) -> None:
        self.registry = tool_registry or ToolRegistry()
        self.platform = platform_connector

    def compose_do_messages(
        self,
        instruction: str,
        ui_elements: Optional[List[Dict[str, Any]]] = None,
        platform: str = "mobile",
        click_mode: str = "hybrid"
    ) -> List[Dict[str, Any]]:
        """Build DO action messages using tool calling approach.
        
        Args:
            instruction: User instruction
            ui_elements: List of UI elements
            platform: 'mobile' or 'web' - determines system prompt
            click_mode: 'xml', 'visual', or 'hybrid' - guides AI on click strategy
        """
        # Base system prompt
        if platform == "mobile":
            system_content = (
                "You are a MOBILE app test automation engine (Appium).\n"
                "Your job: analyze the instruction and call the appropriate function to interact with the mobile UI.\n"
            )
            
            # Add click guidance based on mode
            if click_mode == "xml":
                system_content += (
                    "\nFOR CLICKING: Use click_element(index) - select element by its index from the numbered list below.\n"
                )
            elif click_mode == "visual":
                system_content += (
                    "\nFOR CLICKING: Use click_visual_element(description) - describe the element visually.\n"
                    "You will receive a element list coordinates. return the coordinates of the element to interact with.\n"
                )
            else:  # hybrid
                system_content += (
                    "\nACTION SELECTION RULES:\n"
                    "1. FOR TEXT INPUT (instructions with 'input', 'type', 'enter', 'fill') → ALWAYS use input_text(element_index, text) with XML index\n"
                    "2. FOR CLICKING - You have TWO options:\n"
                    "   a. tap_element(index): Select from numbered list - USE when element has clear ID, resource-id, or unique text\n"
                    "   b. click_visual_element(description): Visual description - USE ONLY for icons, images, or elements WITHOUT clear XML identifiers\n"
                    "3. OTHER ACTIONS: scroll_down(), swipe_left/right/up(), long_press(index), hide_keyboard(), go_back()\n"
                    "\nCRITICAL: input_text REQUIRES XML locator (element_index). NEVER use click_visual_element for text input actions.\n"
                )
            
            system_content += (
                "\nIMPORTANT: You are working with MOBILE apps (Android/iOS), NOT web browsers."
            )
        else:
            system_content = (
                "You are a WEB test automation engine.\n"
                "Your job: analyze the instruction and call the appropriate function to interact with the web page.\n"
            )
            
            # Add click guidance based on mode
            if click_mode == "xml":
                system_content += (
                    "\nFOR INTERACTION: Use standard tools (click_element, input_text) with element index from the list.\n"
                )
            elif click_mode == "visual":
                system_content += (
                    "\nFOR INTERACTION: Use VISUAL tools:\n"
                    "- click_visual_element(description): Click element by visual description\n"
                    "- input_text_visual(description, text): Input text into element by visual description\n"
                    "- hover_visual(description): Hover over element by visual description\n"
                    "- double_click_visual(description): Double click element by visual description\n"
                    "You will receive a screenshot. Analyze it and use visual descriptions.\n"
                )
            else:  # hybrid
                system_content += (
                    "\nACTION SELECTION RULES:\n"
                    "1. FOR TEXT INPUT:\n"
                    "   a. input_text(index, text): USE DEFAULT when element is in the list (<input>, <textarea>)\n"
                    "   b. input_text_visual(description, text): USE ONLY when element is NOT in the list or has no clear locator\n"
                    "2. FOR CLICKING/HOVERING:\n"
                    "   a. Standard tools (click_element, hover, double_click): USE DEFAULT when element is in the list\n"
                    "   b. Visual tools (click_visual_element, hover_visual, double_click_visual): USE ONLY for icons, images, or elements NOT in the list\n"
                )

            system_content += (
                "\nCRITICAL: Pay attention to element tags when using standard tools:\n"
                "- <input> or <textarea> = text input fields (use input_text tool)\n"
                "- <button> or <a> = clickable elements (use click_element tool)\n"
                "- <select> = dropdown (use select_option tool)\n"
            )
        
        # Build user content based on mode
        if click_mode == "visual":
            # Mode visual: PAS de liste UI (confusant!)
            user_content = f"Instruction: {instruction}\n\nAnalyze the screenshot and use visual description."
        else:
            # Modes xml/hybrid: Envoyer la liste UI
            if self.platform and ui_elements:
                ui_text = self.platform.render_ui_for_prompt(ui_elements)
            else:
                ui_text = "(no UI elements found)"
            
            ui_label = "Mobile UI Elements" if platform == "mobile" else "Web Elements"
            user_content = f"Instruction: {instruction}\n\n{ui_label}:\n{ui_text}"
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def get_do_tools(
        self, 
        category: str = "mobile",
        click_mode: str = "hybrid"
    ) -> List[Dict[str, Any]]:
        """Return tool definitions for DO actions from the registry.
        
        Returns tool specs in standard format (works with OpenAI, Anthropic, Gemini, etc.)
        
        Args:
            category: Tool category to retrieve ('mobile', 'web', or None for all)
            click_mode: 'xml', 'visual', or 'hybrid' - filters tools based on capabilities
        """
        # Use registry's new filtering method
        filtered_tools = self.registry.get_tools_for_mode(category, click_mode)
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
