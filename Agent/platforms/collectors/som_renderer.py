"""
Set-of-Mark (SoM) Renderer.

Draws numbered bounding boxes on screenshots for visual grounding.
"""

import base64
import io
from typing import Any, Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont


# Colors for different sources
COLOR_DOM = (34, 197, 94)        # Green for DOM elements (has locator)
COLOR_OMNIPARSER = (249, 115, 22)  # Orange for OmniParser (click-only)
COLOR_DEFAULT = (59, 130, 246)   # Blue default


def render_som(
    screenshot_base64: str,
    elements: List[Dict[str, Any]],
    source_key: str = "source",
) -> str:
    """
    Draw numbered bounding boxes on screenshot.
    
    Args:
        screenshot_base64: Base64 encoded PNG/JPEG
        elements: List with 'bbox' key {x, y, width, height} and optional source
        source_key: Key to check for source type ("dom" or "omniparser")
    
    Returns:
        Base64 of annotated image
    
    Example:
        >>> elements = [{'text': 'Search', 'bbox': {'x': 10, 'y': 20, 'width': 100, 'height': 30}, 'source': 'dom'}]
        >>> annotated = render_som(screenshot_b64, elements)
    """
    img_bytes = base64.b64decode(screenshot_base64)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        font = ImageFont.load_default()
        font_large = font
    
    for idx, element in enumerate(elements, start=1):
        bbox = element.get("bbox")
        if not bbox:
            continue
        
        x = bbox.get("x", 0)
        y = bbox.get("y", 0)
        w = bbox.get("width", 0)
        h = bbox.get("height", 0)
        
        if w <= 0 or h <= 0:
            continue
        
        source = element.get(source_key, "dom")
        color = COLOR_DOM if source == "dom" else COLOR_OMNIPARSER if source == "omniparser" else COLOR_DEFAULT
        
        # Draw box with transparency
        draw.rectangle(
            [x, y, x + w, y + h],
            outline=color + (255,),
            width=2
        )
        
        # Draw label background
        label = str(idx)
        label_bbox = draw.textbbox((0, 0), label, font=font_large)
        label_w = label_bbox[2] - label_bbox[0] + 8
        label_h = label_bbox[3] - label_bbox[1] + 4
        
        label_x = x
        label_y = y - label_h - 2
        if label_y < 0:
            label_y = y + 2
        
        draw.rectangle(
            [label_x, label_y, label_x + label_w, label_y + label_h],
            fill=color + (230,)
        )
        
        # Draw label text
        draw.text(
            (label_x + 4, label_y + 2),
            label,
            fill=(255, 255, 255, 255),
            font=font_large
        )
    
    result = Image.alpha_composite(img, overlay).convert("RGB")
    
    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def bbox_center(bbox: Dict[str, int]) -> Tuple[int, int]:
    if not bbox:
        return (0, 0)
    x = bbox.get("x", 0)
    y = bbox.get("y", 0)
    w = bbox.get("width", 0)
    h = bbox.get("height", 0)
    return (x + w // 2, y + h // 2)





