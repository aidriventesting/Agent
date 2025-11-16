from typing import List, Dict, Optional, Any
from Agent.platforms import DeviceConnector


class AgentPromptComposer:
    """Builds prompts for agent actions and visual checks."""

    def __init__(self) -> None:
        self.catalog = AgentKeywordCatalog()

    def compose_do_messages(
        self,
        instruction: str,
        ui_elements: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """Build DO action messages."""
        ui_text = self._render_ui_candidates(ui_elements)
        system_content = (
            "You are a MOBILE app test automation engine (Appium).\n"
            "Your job: pick the element number that matches the instruction.\n\n"
            f"{self.catalog._render_catalog_text()}\n\n"
            "IMPORTANT: You are working with MOBILE apps (Android/iOS), NOT web browsers.\n"
            "Just select the element index from the numbered list - we will build the locator."
        )
        user_content = (
            f"Instruction: {instruction}\n\n"
            f"Mobile UI Elements:\n{ui_text}\n\n"
            "Respond with JSON: {\"action\": \"tap|input|scroll_down\", \"element_index\": <number>, \"text\": \"...\" (only for input action)}"
        )
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def compose_visual_check_messages(
        self,
        instruction: str,
        image_url: str,
    ) -> List[Dict[str, Any]]:
        """Build visual check messages."""
        system_content = (
            "You are a mobile app visual verification engine. "
            "Analyze the screenshot and verify if it matches the instruction."
        )
        user_content = [
            {"type": "text", "text": f"Verify: {instruction}\n\nRespond with JSON: {{\"verification_result\": true/false, \"confidence_score\": 0.0-1.0, \"analysis\": \"...\"}}"},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]

    def _render_ui_candidates(self, ui_elements: Optional[List[Dict[str, Any]]]) -> str:
        if not ui_elements:
            return "(no UI elements found)"
        
        rendered = []
        for i, el in enumerate(ui_elements[:20], 1):
            parts = []
            if el.get("text"):
                parts.append(f"text='{el['text']}'")
            if el.get("resource_id"):
                parts.append(f"id='{el['resource_id']}'")
            if el.get("content_desc"):
                parts.append(f"desc='{el['content_desc']}'")
            
            rendered.append(f"{i}. {' | '.join(parts) if parts else el.get('class_name', 'unknown')}")
        
        return "\n".join(rendered)





class AgentKeywordCatalog:
    """Catalog of available mobile actions."""

    def __init__(self) -> None:
        self.actions = [
            ("tap", "Click Element", "Tap/click an element"),
            ("input", "Input Text", "Clear and type text into element"),
            ("scroll_down", "Swipe", "Scroll down the screen"),
        ]

    def _render_catalog_text(self) -> str:
        lines = ["Available actions:"]
        for action, rf_kw, desc in self.actions:
            lines.append(f"- {action}: {desc}")
        return "\n".join(lines)
