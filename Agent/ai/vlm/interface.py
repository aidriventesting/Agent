from typing import Any, Dict, List, Optional, Tuple
from robot.api import logger
from PIL import Image

from Agent.ai.vlm._client import OmniParserClient
from Agent.ai.vlm._parser import OmniParserResultProcessor
from Agent.ai.vlm._selector import OmniParserElementSelector


class OmniParserOrchestrator:
    """
    Main orchestrator for GUI element selection via OmniParser + LLM.
    
    This class coordinates:
    1. OmniParserClient - Analyzes the image via Hugging Face
    2. OmniParserResultProcessor - Parses and filters elements
    3. OmniParserElementSelector - Selects the element via LLM
    """

    def __init__(
        self,
        *,
        llm_provider: str = "openai",
        llm_model: str = "gpt-4o-mini",
        omniparser_space_id: Optional[str] = None,
        hf_token: Optional[str] = None,
    ) -> None:
        """
        Initializes the orchestrator with all necessary components.
        
        Args:
            llm_provider: LLM provider (openai, anthropic, etc.)
            llm_model: Model to use
            omniparser_space_id: OmniParser Hugging Face space ID (optional)
            hf_token: Hugging Face token (optional)
        """
        self.client = OmniParserClient(
            space_id=omniparser_space_id,
            hf_token=hf_token
        )
        self.selector = OmniParserElementSelector(
            provider=llm_provider,
            model=llm_model
        )
        logger.debug("OmniParserOrchestrator initialized successfully")

    def find_element(
        self,
        element_description: str,
        *,
        image_path: Optional[str] = None,
        image_url: Optional[str] = None,
        image_base64: Optional[str] = None,
        image_name: Optional[str] = None,
        element_type: str = "interactive",
        box_threshold: Optional[float] = None,
        iou_threshold: Optional[float] = None,
        use_paddleocr: Optional[bool] = None,
        imgsz: Optional[int] = None,
        temperature: float = 0.0,
        use_vision_for_selection: bool = False,
    ) -> Optional[Dict[str, Any]]:
        logger.debug(f"🔍 Searching for element: '{element_description}'")
        
        # Step 1: Analyze image with OmniParser
        logger.debug("📸 Step 1/3: Analyzing image with OmniParser...")
        image_temp_path, parsed_text = self.client.parse_image(
            image_path=image_path,
            image_url=image_url,
            image_base64=image_base64,
            image_name=image_name,
            box_threshold=box_threshold,
            iou_threshold=iou_threshold,
            use_paddleocr=use_paddleocr,
            imgsz=imgsz,
        )
        
        if not parsed_text:
            logger.debug("❌ OmniParser detected no elements")
            return None
        
        # Step 2: Parse and filter elements by type
        logger.debug(f"🔧 Step 2/3: Parsing and filtering elements (type={element_type})...")
        processor = OmniParserResultProcessor(
            response_text=parsed_text,
            image_temp_path=image_temp_path,
        )
        elements_data = processor.get_parsed_ui_elements(element_type=element_type)
        
        if not elements_data:
            logger.debug(f"❌ No elements of type '{element_type}' found")
            return None
         
        logger.debug(f"✓ {len(elements_data)} filtered elements")
        
        # Log all filtered elements for debugging
        logger.debug(f"Filtered elements ({element_type}):")
        for key, data in list(elements_data.items())[:20]:  # Limit to 20 for readability
            logger.debug(f"  - {key}: type={data['type']}, content='{data['content']}', interactive={data['interactivity']}")
        
        import os
        abs_image_path = os.path.abspath(image_temp_path)
        msg = f"</td></tr><tr><td colspan=\"3\"><img src=\"file://{abs_image_path}\" width=\"1200\"></td></tr>"
        logger.debug(msg, html=True)
        
        # Step 3: Select element via LLM
        logger.debug("🤖 Step 3/3: Selecting element via LLM...")
        result = self.selector.select_element(
            elements_data=elements_data,
            element_description=element_description,
            temperature=temperature,
            use_vision=use_vision_for_selection,
            image_path=image_temp_path if use_vision_for_selection else None,
        )
        
        if not result:
            logger.debug("❌ The LLM found no matching element")
            return None
        
        # Add temporary image to result
        result["image_temp_path"] = image_temp_path
        
        logger.debug(
            f"✅ Element found: {result['element_key']} "
            f"(confidence={result.get('confidence', 'unknown')})"
        )
        
        return result

    def detect_all_elements(
        self,
        image_base64: str,
        element_type: str = "interactive",
        box_threshold: Optional[float] = None,
        iou_threshold: Optional[float] = None,
        use_paddleocr: Optional[bool] = None,
        imgsz: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Detect all elements using OmniParser.
        
        Args:
            image_base64: Base64 encoded image
            element_type: Type filter ('interactive', 'text', 'icon', 'all')
            
        Returns:
            List of elements in standard format compatible with DOM elements
            Example: [{'text': 'Login', 'bbox': {'x': 10, 'y': 20, 'width': 100, 'height': 50}, 'source': 'omniparser'}, ...]
        """
        logger.debug(f"🔍 Detecting all elements with OmniParser (type={element_type})")
        
        image_temp_path, parsed_text = self.client.parse_image(
            image_base64=image_base64,
            box_threshold=box_threshold,
            iou_threshold=iou_threshold,
            use_paddleocr=use_paddleocr,
            imgsz=imgsz,
        )
        
        if not parsed_text:
            logger.debug("❌ OmniParser detected no elements")
            return []
        
        processor = OmniParserResultProcessor(
            response_text=parsed_text,
            image_temp_path=image_temp_path,
        )
        elements_data = processor.get_parsed_ui_elements(element_type=element_type)
        
        if not elements_data:
            logger.debug(f"❌ No elements of type '{element_type}' found")
            return []
        
        from PIL import Image
        with Image.open(image_temp_path) as img:
            width, height = img.size
        
        result = []
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
            result.append(element)
        
        logger.debug(f"✅ Detected {len(result)} visual elements")
        return result

    @staticmethod
    def get_element_center_coordinates(
        element_result: Dict[str, Any]
    ) -> Tuple[int, int]:
        """
        Calculate center coordinates from element result.
        
        Args:
            element_result: Result dict from find_element() containing
                          'element_data' with 'bbox' and 'image_temp_path'
        
        Returns:
            Tuple (x_center, y_center) in pixels
        """
        bbox_normalized = element_result["element_data"]["bbox"]
        image_temp_path = element_result["image_temp_path"]
        
        # Convert bbox to pixels
        x1, y1, x2, y2 = OmniParserOrchestrator.bbox_to_pixels_from_image(
            bbox_normalized=bbox_normalized,
            image_path=image_temp_path
        )
        
        # Calculate center
        x_center = (x1 + x2) // 2
        y_center = (y1 + y2) // 2
        
        logger.debug(f"Element center coordinates: ({x_center}, {y_center})")
        
        return x_center, y_center

    @staticmethod
    def bbox_to_pixels(
        bbox_normalized: List[float],
        image_width: int,
        image_height: int,
    ) -> Tuple[int, int, int, int]:
        if len(bbox_normalized) != 4:
            raise ValueError(f"bbox must contain 4 values, received {len(bbox_normalized)}")
        
        x1_norm, y1_norm, x2_norm, y2_norm = bbox_normalized
        
        # Convert to pixels
        x1 = int(x1_norm * image_width)
        y1 = int(y1_norm * image_height)
        x2 = int(x2_norm * image_width)
        y2 = int(y2_norm * image_height)
        
        logger.debug(
            f"Bbox conversion: [{x1_norm:.3f}, {y1_norm:.3f}, {x2_norm:.3f}, {y2_norm:.3f}] "
            f"-> [{x1}, {y1}, {x2}, {y2}] (image: {image_width}x{image_height})"
        )
        
        return (x1, y1, x2, y2)

    @staticmethod
    def bbox_to_pixels_from_image(
        bbox_normalized: List[float],
        image_path: str,
    ) -> Tuple[int, int, int, int]:
        """
        Converts normalized bbox to pixels by automatically reading dimensions.
        
        Args:
            bbox_normalized: List [x1, y1, x2, y2] with values between 0 and 1
            image_path: Path to the image to get dimensions
            
        Returns:
            Tuple (x1, y1, x2, y2) in integer pixel coordinates
            
        Example:
            >>> bbox = [0.419, 0.170, 0.574, 0.266]
            >>> pixels = OmniParserOrchestrator.bbox_to_pixels_from_image(
            ...     bbox, "screenshot.png"
            ... )
            >>> print(pixels)  # (452, 326, 620, 510)
        """
        try:
            with Image.open(image_path) as img:
                width, height = img.size
            logger.debug(f"Image dimensions '{image_path}': {width}x{height}")
        except Exception as e:
            logger.error(f"Unable to open image '{image_path}': {e}")
            raise
        
        return OmniParserOrchestrator.bbox_to_pixels(
            bbox_normalized=bbox_normalized,
            image_width=width,
            image_height=height,
        )


if __name__ == "__main__":
    orchestrator = OmniParserOrchestrator()
    result = orchestrator.find_element(
        element_description="YouTube icon",
        image_path="tests/_data/mobilescreenshots/screenshot-Google Pixel 5-11.0.png"
    )
    print(result)