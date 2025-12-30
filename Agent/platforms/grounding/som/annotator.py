"""
SoM Visual Annotator.

Draws numbered bounding boxes on screenshots for visual grounding.
"""

import base64
import io
from typing import Any, Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont


COLOR_DOM = (34, 197, 94)
COLOR_OMNIPARSER = (249, 115, 22)
COLOR_DEFAULT = (59, 130, 246)


def annotate_screenshot(
    screenshot_base64: str,
    elements: List[Dict[str, Any]],
    source_key: str = "source",
) -> str:
    """
    Args:
        screenshot_base64: Base64 encoded PNG/JPEG
        elements: List with 'bbox' key {x, y, width, height}
        source_key: Key to check for source type
    Returns:
        Base64 of annotated image
    """
    img_bytes = base64.b64decode(screenshot_base64)
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        import platform
        system = platform.system()
        
        if system == "Darwin":
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
            font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        elif system == "Windows":
            font = ImageFont.truetype("arial.ttf", 14)
            font_large = ImageFont.truetype("arial.ttf", 24)
        else:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except Exception:
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
        
        margin = 4
        if w <= 2 * margin:
            margin = max(0, w // 2 - 1)
        if h <= 2 * margin:
            margin = min(margin, max(0, h // 2 - 1))
        
        box_x1 = x + margin
        box_y1 = y + margin
        box_x2 = x + w - margin
        box_y2 = y + h - margin
        
        if box_x2 <= box_x1:
            box_x2 = box_x1 + 1
        if box_y2 <= box_y1:
            box_y2 = box_y1 + 1
        
        draw.rectangle(
            [box_x1, box_y1, box_x2, box_y2],
            outline=color + (255,),
            width=2
        )
        
        label = str(idx)
        label_bbox = draw.textbbox((0, 0), label, font=font_large)
        label_w = label_bbox[2] - label_bbox[0] + 12
        label_h = label_bbox[3] - label_bbox[1] + 8
        
        label_x = box_x1 + 5
        label_y = box_y1 + 5
        
        draw.rectangle(
            [label_x, label_y, label_x + label_w, label_y + label_h],
            fill=color + (230,)
        )
        
        draw.text(
            (label_x + 6, label_y + 4),
            label,
            fill=(255, 255, 255, 255),
            font=font_large,
            stroke_width=2,
            stroke_fill=(0, 0, 0, 255)
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

