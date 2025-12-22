from typing import Any, Dict
from Agent.tools.base import BaseTool, ExecutorProtocol, ToolCategory
from robot.api import logger


class ClickElementTool(BaseTool):
    """Click on a web UI element."""
    
    @property
    def name(self) -> str:
        return "click_element"
    
    @property
    def description(self) -> str:
        return "Click element by INDEX from numbered list - USE ONLY when element has clear ID, resource-id, or unique text"
    
    @property
    def category(self) -> ToolCategory:
        return ToolCategory.WEB
    
    @property
    def works_on_locator(self) -> bool:
        return True
    
    @property
    def works_on_visual(self) -> bool:
        return False
    
    @property
    def has_visual_equivalent(self) -> bool:
        return True
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "element_index": {
                    "type": "integer",
                    "description": "The index number of the element from the UI elements list (1-based)",
                    "minimum": 1
                }
            },
            "required": ["element_index"]
        }
    
    def execute(
        self, 
        executor: ExecutorProtocol, 
        arguments: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> None:
        element_index = arguments["element_index"]
        element_source = context.get("element_source", "tree")
        
        if element_source == "visual":
            # Visual mode: use coordinates from OmniParser results
            visual_elements = context.get("visual_elements", {})
            keys = list(visual_elements.keys())
            
            if element_index < 1 or element_index > len(keys):
                raise AssertionError(
                    f"Invalid element_index: {element_index}. Must be 1-{len(keys)}"
                )
            
            element_key = keys[element_index - 1]
            element = visual_elements[element_key]
            bbox = element.get("bbox", [])
            
            if len(bbox) != 4:
                raise AssertionError(f"Invalid bbox for element {element_key}")
            
            # Get screenshot dimensions from context or use default viewport
            screenshot_base64 = context.get("screenshot_base64")
            if screenshot_base64:
                import base64
                from PIL import Image
                import io
                img_bytes = base64.b64decode(screenshot_base64)
                img = Image.open(io.BytesIO(img_bytes))
                img_width, img_height = img.size
            else:
                img_width, img_height = 1920, 1080
            
            # Convert normalized bbox to pixel coordinates
            x1 = int(bbox[0] * img_width)
            y1 = int(bbox[1] * img_height)
            x2 = int(bbox[2] * img_width)
            y2 = int(bbox[3] * img_height)
            
            x_center = (x1 + x2) // 2
            y_center = (y1 + y2) // 2
            
            logger.debug(f"Visual click on element {element_index} at ({x_center}, {y_center})")
            executor.run_keyword("Mouse Button", "click", x_center, y_center)
        else:
            # Tree mode: use locator from DOM/XML
            ui_candidates = context.get("ui_candidates", [])
            
            if element_index < 1 or element_index > len(ui_candidates):
                raise AssertionError(
                    f"Invalid element_index: {element_index}. Must be 1-{len(ui_candidates)}"
                )
            
            element = ui_candidates[element_index - 1]
            locator = executor.build_locator(element)
            
            logger.debug(f"Built locator: {locator} from element: {element}")
            
            try:
                executor.run_keyword("Click with options", locator, "force=True")
            except Exception as e:
                # #region agent log
                import json; open('/Users/abdelkader/Documents/agent/.cursor/debug.log', 'a').write(json.dumps({'sessionId':'debug-session','runId':'click-fallback','hypothesisId':'STRICT','location':'click_element.py:111','message':'Exception caught','data':{'exception_type':type(e).__name__,'exception_msg':str(e)[:200],'has_strict':('strict mode violation' in str(e))},'timestamp':__import__('time').time()*1000})+'\n')
                # #endregion
                if "strict mode violation" in str(e):
                    bbox = element.get("bbox", {})
                    # #region agent log
                    import json; open('/Users/abdelkader/Documents/agent/.cursor/debug.log', 'a').write(json.dumps({'sessionId':'debug-session','runId':'click-fallback','hypothesisId':'BBOX','location':'click_element.py:117','message':'Checking bbox','data':{'bbox':bbox,'has_keys':bool(bbox and all(k in bbox for k in ("x", "y", "width", "height")))},'timestamp':__import__('time').time()*1000})+'\n')
                    # #endregion
                    if bbox and all(k in bbox for k in ("x", "y", "width", "height")):
                        x_center = bbox["x"] + bbox["width"] / 2
                        y_center = bbox["y"] + bbox["height"] / 2
                        logger.debug(f"Strict mode fallback: clicking at ({x_center}, {y_center})")
                        executor.run_keyword("Mouse Button", "click", x_center, y_center)
                    else:
                        logger.debug(f"Strict mode fallback: using nth=0")
                        executor.run_keyword("Click", f"{locator} >> nth=0")
                else:
                    raise

