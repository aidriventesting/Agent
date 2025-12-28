from typing import Any, Dict, Optional
from robot.api import logger

from Agent.ai.llm.facade import UnifiedLLMFacade


class OmniParserElementSelector:
    def __init__(self, provider: str = "openai", model: str = "gpt-4o-mini") -> None:
        self.llm = UnifiedLLMFacade(provider=provider, model=model)
        logger.info(f"OmniParserElementSelector initialized with {provider}/{model}")

    def select_element(
        self,
        elements_data: Dict[str, Dict[str, Any]],
        element_description: str,
        temperature: float = 0.0,
        use_vision: bool = False,
        image_path: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Selects the GUI element that matches the description.
        
        Args:
            elements_data: Dictionary of elements (e.g., {'icon3': {'type': 'icon', ...}})
            element_description: Description of the element to find (e.g., "YouTube app")
            temperature: Temperature for generation (0.0 = deterministic)
            use_vision: If True, send annotated image to LLM (requires vision-capable model)
            image_path: Path to annotated image (required if use_vision=True)
            
        Returns:
            A dictionary with:
            - element_key: The key of the found element (e.g., 'icon3')
            - element_data: The element data
            - confidence: Confidence level (optional)
            - reason: Reason for the choice (optional)
            
            Returns None if no element is found.
        """
        logger.debug(f"Searching for element: '{element_description}'")
        logger.debug(f"Number of elements to analyze: {len(elements_data)}")

        # Build the prompt
        messages = self._build_prompt(elements_data, element_description, use_vision=use_vision, image_path=image_path)
        
        # Send to AI
        try:
            response = self.llm.send_ai_request_and_return_response(
                messages=messages,
                temperature=temperature
            )
            
            # Parse the response
            result = self._parse_response(response, elements_data)
            
            if result:
                logger.debug(f"✅ Element found: {result.get('element_key')}")
            else:
                logger.warn("❌ No matching element found")
                
            return result
            
        except Exception as e:
            logger.error(f"Error during selection: {str(e)}")
            return None

    def _build_prompt(
        self,
        elements_data: Dict[str, Dict[str, Any]],
        element_description: str,
        use_vision: bool = False,
        image_path: Optional[str] = None,
    ) -> list:
        # Format elements in a readable way
        elements_text = self._format_elements(elements_data)
        
        system_prompt = """You are an assistant specialized in GUI element selection.
Your task is to find the element that best matches the given description.

Analyze the available elements and return the one that matches best.
If no element matches, indicate 'element_key': null.

Respond ONLY in JSON with this structure:
{
    "element_key": "the element key (e.g., icon3) or null",
    "confidence": "high, medium or low",
    "reason": "brief explanation of your choice"
}"""

        user_text = f"""Available elements:
{elements_text}

Description of the element being searched for: "{element_description}"

Find the element that best matches this description."""

        # Build user message (text-only or multimodal)
        if use_vision and image_path:
            import base64
            import os
            
            # Read and encode the annotated image from OmniParser
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            # Determine image format from extension
            ext = os.path.splitext(image_path)[1].lower()
            media_type = "image/png" if ext == ".png" else "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/webp"
            
            # Send both text list AND annotated image to LLM
            user_content = [
                {
                    "type": "text", 
                    "text": f"{user_text}\n\nNOTE: The image shows the annotated screenshot with numbered bounding boxes corresponding to the element keys above."
                },
                {
                    "type": "image_url", 
                    "image_url": {"url": f"data:{media_type};base64,{image_base64}"}
                }
            ]
            logger.debug("Using vision mode: sending OmniParser annotated image to LLM")
        else:
            user_content = user_text

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]

    def _format_elements(self, elements_data: Dict[str, Dict[str, Any]]) -> str:
        lines = []
        for key, data in elements_data.items():
            content = data.get("content", "")
            element_type = data.get("type", "unknown")
            interactive = data.get("interactivity", False)
            
            lines.append(
                f"- {key}: type={element_type}, content='{content}', "
                f"interactive={interactive}"
            )
        
        return "\n".join(lines)

    def _parse_response(
        self,
        response: Dict[str, Any],
        elements_data: Dict[str, Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """
        Parses the AI response.
        
        Args:
            response: The JSON response from the AI
            elements_data: The original elements
            
        Returns:
            Dictionary with the found element or None
        """
        element_key = response.get("element_key")
        
        # If no element found
        if not element_key or element_key == "null":
            return None
        
        # Check that the element exists
        if element_key not in elements_data:
            logger.warn(f"The returned element '{element_key}' does not exist in the data")
            return None
        
        # Build the result
        return {
            "element_key": element_key,
            "element_data": elements_data[element_key],
            "confidence": response.get("confidence", "unknown"),
            "reason": response.get("reason", ""),
        }


if __name__ == "__main__":
    selector = OmniParserElementSelector()
    result = selector.select_element(
        elements_data={
            "icon3": {"type": "icon", "bbox": [0.419, 0.17, 0.574, 0.266], "interactivity": True, "content": "st"},
            "icon4": {"type": "icon", "bbox": [0.419, 0.17, 0.574, 0.266], "interactivity": False, "content": "st"},
            "icon5": {"type": "icon", "bbox": [0.419, 0.17, 0.574, 0.266], "interactivity": False, "content": "st"},
            "icon6": {"type": "icon", "bbox": [0.419, 0.17, 0.574, 0.266], "interactivity": False, "content": "st"},
            "icon7": {"type": "icon", "bbox": [0.419, 0.17, 0.574, 0.266], "interactivity": False, "content": "st"},
            "icon8": {"type": "icon", "bbox": [0.419, 0.17, 0.574, 0.266], "interactivity": False, "content": "YouTube"},
        },
        element_description="YouTube icon",
    )
    print(result)