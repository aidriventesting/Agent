from typing import Any, Dict, List, Optional
from Agent.platforms.grounding.som.serializer import SomSerializer
from Agent.platforms.grounding.som.annotator import annotate_screenshot


class SomComposer:
    """
    Orchestrates SoM components (visual annotation + text legend).
    
    Args:
        platform: "android" (implemented), "ios"/"web" (future)
        screen_width: Screen width in pixels
        screen_height: Screen height in pixels
    """
    
    def __init__(
        self, 
        platform: str = "android",
        screen_width: int = 1080,
        screen_height: int = 1920
    ):
        self.platform = platform
        self.serializer = SomSerializer(platform, screen_width, screen_height)
    
    def compose(
        self,
        screenshot_base64: Optional[str],
        elements: List[Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Args:
            screenshot_base64: Base64 screenshot (required if visual_annotation=True)
            elements: List of UI elements
            config: {visual_annotation, text_format, output_type, include_screenshot}
        Returns:
            {annotated_image_base64, elements_json, text_legend}
        """
        if config is None:
            config = {}
        
        visual_annotation = config.get('visual_annotation', True)
        text_format = config.get('text_format', 'compact')
        output_type = config.get('output_type', 'text')
        include_screenshot = config.get('include_screenshot', True)
        
        result = {}
        
        if visual_annotation:
            if not screenshot_base64:
                raise ValueError("screenshot_base64 required when visual_annotation=True")
            
            annotated_image = annotate_screenshot(screenshot_base64, elements)
            if include_screenshot:
                result['annotated_image_base64'] = annotated_image
        
        if output_type == 'json':
            result['elements_json'] = self.serializer.serialize(elements, output_type='json')
        elif output_type == 'text':
            result['text_legend'] = self.serializer.serialize(elements, format=text_format, output_type='text')
        
        return result

