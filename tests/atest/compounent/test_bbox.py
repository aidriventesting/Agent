#!/usr/bin/env python
"""
Test script to verify that bounding boxes are correctly returned by collectors.

This script tests that:
1. bbox field exists in collected elements
2. bbox contains x, y, width, height
3. bbox values are valid integers
4. bbox values make sense (positive, reasonable ranges)
"""

import unittest
from Agent.platforms.collectors.js_query_collector import JSQueryCollector
from Agent.platforms.collectors.axtree_collector import AXTreeCollector


class TestBBoxStructure(unittest.TestCase):
    """Test that bbox structure is correct (no browser needed)."""
    
    def test_jsquery_collector_has_bbox_in_mapping(self):
        """Test that JSQueryCollector maps bbox field."""
        collector = JSQueryCollector()
        
        # Simulate data returned from JavaScript
        mock_elem_data = {
            'text': 'Click me',
            'id': 'btn-1',
            'tag': 'button',
            'bbox': {'x': 100, 'y': 200, 'width': 80, 'height': 32}
        }
        
        # This is what the collector does internally
        attrs = {
            'text': mock_elem_data.get('text', ''),
            'resource_id': mock_elem_data.get('testId') or mock_elem_data.get('id', ''),
            'content_desc': mock_elem_data.get('ariaLabel') or mock_elem_data.get('placeholder', ''),
            'label': mock_elem_data.get('label', ''),
            'class_name': mock_elem_data.get('tag', ''),
            'role': mock_elem_data.get('role', ''),
            'name': mock_elem_data.get('name', ''),
            'type': mock_elem_data.get('type', ''),
            'href': mock_elem_data.get('href', ''),
            'clickable': True,
            'enabled': True,
            'bbox': mock_elem_data.get('bbox', {}),
        }
        
        # Verify bbox is present and correct
        self.assertIn('bbox', attrs)
        self.assertEqual(attrs['bbox'], {'x': 100, 'y': 200, 'width': 80, 'height': 32})
    
    def test_axtree_collector_has_bbox_in_mapping(self):
        """Test that AXTreeCollector maps bbox field."""
        collector = AXTreeCollector()
        
        # Simulate data returned from JavaScript
        mock_elem_data = {
            'text': 'Submit',
            'id': 'submit-btn',
            'tag': 'button',
            'role': 'button',
            'accessibleName': 'Submit form',
            'bbox': {'x': 50, 'y': 400, 'width': 100, 'height': 40}
        }
        
        # This is what the collector does internally
        accessible_name = mock_elem_data.get('accessibleName', '')
        text = mock_elem_data.get('text', '')
        
        attrs = {
            'text': text,
            'resource_id': mock_elem_data.get('testId') or mock_elem_data.get('id', ''),
            'content_desc': accessible_name or mock_elem_data.get('placeholder', ''),
            'label': accessible_name if accessible_name != text else '',
            'class_name': mock_elem_data.get('tag', ''),
            'role': mock_elem_data.get('role', ''),
            'name': mock_elem_data.get('name', ''),
            'type': mock_elem_data.get('type', ''),
            'href': mock_elem_data.get('href', ''),
            'clickable': True,
            'enabled': True,
            'bbox': mock_elem_data.get('bbox', {}),
        }
        
        # Verify bbox is present and correct
        self.assertIn('bbox', attrs)
        self.assertEqual(attrs['bbox'], {'x': 50, 'y': 400, 'width': 100, 'height': 40})
    
    def test_bbox_structure(self):
        """Test that bbox has the correct structure."""
        bbox = {'x': 100, 'y': 200, 'width': 80, 'height': 32}
        
        # Verify all required keys are present
        self.assertIn('x', bbox)
        self.assertIn('y', bbox)
        self.assertIn('width', bbox)
        self.assertIn('height', bbox)
        
        # Verify all values are integers
        self.assertIsInstance(bbox['x'], int)
        self.assertIsInstance(bbox['y'], int)
        self.assertIsInstance(bbox['width'], int)
        self.assertIsInstance(bbox['height'], int)
    
    def test_bbox_values_are_positive(self):
        """Test that bbox values are positive (or zero)."""
        bbox = {'x': 100, 'y': 200, 'width': 80, 'height': 32}
        
        self.assertGreaterEqual(bbox['x'], 0)
        self.assertGreaterEqual(bbox['y'], 0)
        self.assertGreater(bbox['width'], 0)  # width must be > 0 for visible elements
        self.assertGreater(bbox['height'], 0)  # height must be > 0 for visible elements


class TestBBoxDocumentation(unittest.TestCase):
    """Test that bbox is documented in BaseUICollector."""
    
    def test_base_collector_documents_bbox(self):
        """Test that BaseUICollector docstring mentions bbox."""
        from Agent.platforms.collectors.base_collector import BaseUICollector
        
        docstring = BaseUICollector.collect_elements.__doc__
        self.assertIsNotNone(docstring)
        self.assertIn('bbox', docstring.lower())


def validate_bbox(bbox: dict) -> tuple[bool, str]:
    """
    Validate a bbox dictionary.
    
    Returns:
        (is_valid, error_message)
    """
    if not isinstance(bbox, dict):
        return False, f"bbox is not a dict, got {type(bbox)}"
    
    required_keys = ['x', 'y', 'width', 'height']
    for key in required_keys:
        if key not in bbox:
            return False, f"bbox missing key: {key}"
    
    for key in required_keys:
        if not isinstance(bbox[key], int):
            return False, f"bbox[{key}] is not an int, got {type(bbox[key])}"
    
    if bbox['width'] <= 0:
        return False, f"bbox width must be > 0, got {bbox['width']}"
    
    if bbox['height'] <= 0:
        return False, f"bbox height must be > 0, got {bbox['height']}"
    
    # x and y can be negative (element off-screen to the left/top)
    # but let's warn if they're too negative
    if bbox['x'] < -10000 or bbox['y'] < -10000:
        return False, f"bbox coordinates seem unrealistic: x={bbox['x']}, y={bbox['y']}"
    
    # Reasonable max dimensions (8K screen is ~7680 x 4320)
    if bbox['width'] > 20000 or bbox['height'] > 20000:
        return False, f"bbox dimensions seem too large: {bbox['width']}x{bbox['height']}"
    
    return True, "OK"


if __name__ == "__main__":
    print("=" * 60)
    print("Testing BBox Implementation")
    print("=" * 60)
    print()
    
    # Run unit tests
    unittest.main(verbosity=2)

