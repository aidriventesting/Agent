"""
BBoxVisualizer - Robot Framework Library for visualizing bounding boxes.

This library provides keywords to draw bounding boxes on screenshots,
making it easy to visualize which elements were detected by UI collectors.

Usage:
    Library    tests/atest/compounent/BBoxVisualizer.py
    
    ${annotated}=    Draw And Log Elements    ${elements}    screenshot.png
"""

import os
import base64
from datetime import datetime
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class BBoxVisualizer:
    """
    Robot Framework library for visualizing bounding boxes on screenshots.
    
    This library helps debug and visualize UI element detection by drawing
    rectangles around detected elements with numbers and labels.
    """
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.0'
    
    def __init__(self):
        """Initialize the BBoxVisualizer library."""
        self.default_color = 'red'
        self.default_width = 3
        self.default_text_color = 'white'
        self.default_label_color = 'blue'
        self.builtin = BuiltIn()
    
    def _resolve_path(self, path: str) -> str:
        """
        Resolve a path that might be relative to Robot Framework directories.
        
        Tries in order:
        1. Path as-is (if absolute or exists)
        2. Relative to OUTPUT_DIR
        3. Relative to EXECDIR
        4. Relative to current working directory
        
        Args:
            path: Path to resolve
            
        Returns:
            Resolved absolute path
            
        Raises:
            FileNotFoundError: If path cannot be resolved
        """
        # If already absolute and exists, return it
        if os.path.isabs(path) and os.path.exists(path):
            return path
        
        # If relative path exists from current location, return it
        if os.path.exists(path):
            return os.path.abspath(path)
        
        # Try to get Robot Framework variables
        try:
            output_dir = self.builtin.get_variable_value("${OUTPUT DIR}")
            if output_dir:
                resolved = os.path.join(output_dir, path)
                if os.path.exists(resolved):
                    logger.debug(f"Resolved path using OUTPUT_DIR: {resolved}")
                    return resolved
        except:
            pass
        
        try:
            execdir = self.builtin.get_variable_value("${EXECDIR}")
            if execdir:
                resolved = os.path.join(execdir, path)
                if os.path.exists(resolved):
                    logger.debug(f"Resolved path using EXECDIR: {resolved}")
                    return resolved
        except:
            pass
        
        # Try current working directory
        resolved = os.path.abspath(path)
        if os.path.exists(resolved):
            logger.debug(f"Resolved path using CWD: {resolved}")
            return resolved
        
        # If still not found, raise error with helpful message
        logger.error(f"Could not resolve path: {path}")
        logger.error(f"Tried:")
        logger.error(f"  - As-is: {path}")
        logger.error(f"  - CWD: {os.path.abspath(path)}")
        try:
            output_dir = self.builtin.get_variable_value("${OUTPUT DIR}")
            if output_dir:
                logger.error(f"  - OUTPUT_DIR: {os.path.join(output_dir, path)}")
        except:
            pass
        
        raise FileNotFoundError(f"Could not find file: {path}")
    
    def draw_bbox_on_screenshot(
        self, 
        screenshot_path: str, 
        elements: List[Dict[str, Any]], 
        output_path: Optional[str] = None,
        color: str = 'red',
        width: int = 3,
        show_numbers: bool = True,
        show_labels: bool = True
    ) -> str:
        """
        Draw bounding boxes on a screenshot.
        
        Args:
            screenshot_path: Path to the original image
            elements: List of elements with bbox information
            output_path: Output path (optional, auto-generated if None)
            color: Color of the rectangles (default: red)
            width: Width of the rectangle lines (default: 3)
            show_numbers: Whether to show element numbers (default: True)
            show_labels: Whether to show element labels (default: True)
        
        Returns:
            Path to the annotated image file
        
        Example:
            ${annotated}=    Draw BBox On Screenshot    screenshot.png    ${elements}
        """
        logger.info(f"Drawing bounding boxes on {screenshot_path}")
        logger.info(f"Number of elements to annotate: {len(elements)}")
        
        # Resolve path (handle Robot Framework relative paths)
        screenshot_path = self._resolve_path(screenshot_path)
        logger.debug(f"Resolved screenshot path: {screenshot_path}")
        
        # Load image
        try:
            img = Image.open(screenshot_path)
        except Exception as e:
            logger.error(f"Failed to open screenshot: {e}")
            raise
        
        draw = ImageDraw.Draw(img)
        
        # Try to load a font, fallback to default if not available
        try:
            font_size = 16
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
            font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
                font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
            except:
                font = ImageFont.load_default()
                font_large = ImageFont.load_default()
        
        # Draw each bounding box
        annotated_count = 0
        for i, elem in enumerate(elements, 1):
            bbox = elem.get('bbox', {})
            if not bbox or not all(k in bbox for k in ['x', 'y', 'width', 'height']):
                logger.warn(f"Element {i} missing valid bbox: {bbox}")
                continue
            
            x = bbox['x']
            y = bbox['y']
            w = bbox['width']
            h = bbox['height']
            
            # Draw rectangle
            draw.rectangle(
                [x, y, x + w, y + h],
                outline=color,
                width=width
            )
            
            # Draw number badge (top-left corner)
            if show_numbers:
                number_text = str(i)
                
                # Calculate text size
                bbox_text = draw.textbbox((0, 0), number_text, font=font_large)
                text_width = bbox_text[2] - bbox_text[0]
                text_height = bbox_text[3] - bbox_text[1]
                
                # Position for number (above the element)
                number_x = x
                number_y = max(0, y - text_height - 8)
                
                # Draw white background for number
                padding = 4
                draw.rectangle(
                    [number_x - padding, number_y - padding,
                     number_x + text_width + padding, number_y + text_height + padding],
                    fill='white',
                    outline=color,
                    width=2
                )
                
                # Draw number
                draw.text((number_x, number_y), number_text, fill=color, font=font_large)
            
            # Draw label (inside the box, top-left)
            if show_labels:
                label = elem.get('text') or elem.get('content_desc') or elem.get('name', '')
                if label:
                    # Truncate long labels
                    label = label[:30]
                    
                    # Draw semi-transparent background for label
                    label_x = x + 5
                    label_y = y + 5
                    
                    bbox_label = draw.textbbox((0, 0), label, font=font)
                    label_width = bbox_label[2] - bbox_label[0]
                    label_height = bbox_label[3] - bbox_label[1]
                    
                    # Only draw if it fits inside the box
                    if label_y + label_height < y + h:
                        draw.rectangle(
                            [label_x - 2, label_y - 2,
                             label_x + label_width + 2, label_y + label_height + 2],
                            fill='white',
                            outline=None
                        )
                        draw.text((label_x, label_y), label, fill=self.default_label_color, font=font)
            
            annotated_count += 1
        
        # Generate output path if not provided
        if not output_path:
            base, ext = os.path.splitext(screenshot_path)
            output_path = f"{base}_annotated{ext}"
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            logger.debug(f"Created output directory: {output_dir}")
        
        # Save annotated image
        img.save(output_path)
        logger.info(f"Annotated {annotated_count} elements, saved to: {output_path}")
        
        return output_path
    
    def annotate_elements(
        self, 
        elements: List[Dict[str, Any]], 
        screenshot_path: str, 
        output_dir: str = "browser/annotated"
    ) -> str:
        """
        Annotate elements on a screenshot with timestamp.
        
        Args:
            elements: List of elements with bbox
            screenshot_path: Path to original screenshot
            output_dir: Directory for output (default: browser/annotated)
        
        Returns:
            Path to the annotated image
        
        Example:
            ${annotated}=    Annotate Elements    ${elements}    screenshot.png
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(screenshot_path)
        name, ext = os.path.splitext(base_name)
        output_path = os.path.join(output_dir, f"{name}_annotated_{timestamp}{ext}")
        
        return self.draw_bbox_on_screenshot(screenshot_path, elements, output_path)
    
    def draw_and_log_elements(
        self, 
        elements: List[Dict[str, Any]], 
        screenshot_path: str,
        width: int = 800
    ) -> str:
        """
        Draw bounding boxes AND embed the annotated image in Robot Framework log.
        
        This is the most convenient method for Robot Framework tests as it
        both creates the annotated image and displays it in the HTML log.
        
        Args:
            elements: List of elements with bbox
            screenshot_path: Path to original screenshot
            width: Width for embedded image in log (default: 800)
        
        Returns:
            Path to the annotated image
        
        Example:
            ${annotated}=    Draw And Log Elements    ${elements}    screenshot.png
        """
        # Annotate the screenshot
        annotated_path = self.annotate_elements(elements, screenshot_path)
        
        # Embed in Robot Framework log
        try:
            with open(annotated_path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode()
            
            msg = f'</td></tr><tr><td colspan="3"><img src="data:image/png;base64,{img_data}" width="{width}"></td></tr>'
            logger.info(msg, html=True, also_console=False)
            logger.info(f"✅ Annotated screenshot embedded in log: {annotated_path}")
        except Exception as e:
            logger.warn(f"Failed to embed image in log: {e}")
        
        logger.info(f"Elements annotated:")
        for i, element in enumerate(elements):
            logger.info(f"Element {i}: {element}")
        return annotated_path
    
    def create_comparison_image(
        self,
        screenshot_path: str,
        elements_list1: List[Dict[str, Any]],
        elements_list2: List[Dict[str, Any]],
        label1: str = "Collector 1",
        label2: str = "Collector 2",
        output_path: Optional[str] = None
    ) -> str:
        """
        Create a side-by-side comparison of two collectors.
        
        Args:
            screenshot_path: Path to original screenshot
            elements_list1: Elements from first collector
            elements_list2: Elements from second collector
            label1: Label for first collector
            label2: Label for second collector
            output_path: Output path (optional)
        
        Returns:
            Path to comparison image
        
        Example:
            ${comparison}=    Create Comparison Image    screenshot.png    ${js_elements}    ${ax_elements}    JSQuery    AXTree
        """
        # Annotate with first collector (red)
        temp1 = self.draw_bbox_on_screenshot(
            screenshot_path, 
            elements_list1, 
            screenshot_path.replace('.png', '_temp1.png'),
            color='red'
        )
        
        # Annotate with second collector (blue)
        temp2 = self.draw_bbox_on_screenshot(
            screenshot_path,
            elements_list2,
            screenshot_path.replace('.png', '_temp2.png'),
            color='blue'
        )
        
        # Load both images
        img1 = Image.open(temp1)
        img2 = Image.open(temp2)
        
        # Create side-by-side image
        width = img1.width + img2.width
        height = max(img1.height, img2.height) + 40  # +40 for labels
        
        combined = Image.new('RGB', (width, height), 'white')
        
        # Paste images
        combined.paste(img1, (0, 40))
        combined.paste(img2, (img1.width, 40))
        
        # Add labels
        draw = ImageDraw.Draw(combined)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 10), f"{label1} ({len(elements_list1)} elements)", fill='red', font=font)
        draw.text((img1.width + 10, 10), f"{label2} ({len(elements_list2)} elements)", fill='blue', font=font)
        
        # Save
        if not output_path:
            output_path = screenshot_path.replace('.png', '_comparison.png')
        
        combined.save(output_path)
        
        # Cleanup temp files
        os.remove(temp1)
        os.remove(temp2)
        
        logger.info(f"Comparison image saved: {output_path}")
        return output_path


if __name__ == "__main__":
    # Quick test
    print("BBoxVisualizer library loaded")
    print("Version:", BBoxVisualizer.ROBOT_LIBRARY_VERSION)

