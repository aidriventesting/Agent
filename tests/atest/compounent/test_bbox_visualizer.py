#!/usr/bin/env python
"""
Unit tests for BBoxVisualizer library.

These tests verify the BBoxVisualizer functionality without requiring
a browser or real screenshots.
"""

import unittest
import os
import tempfile
from PIL import Image
from tests.atest.compounent.BBoxVisualizer import BBoxVisualizer


class TestBBoxVisualizerUnit(unittest.TestCase):
    """Unit tests for BBoxVisualizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.visualizer = BBoxVisualizer()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a simple test image (white background)
        self.test_image_path = os.path.join(self.temp_dir, "test.png")
        img = Image.new('RGB', (800, 600), 'white')
        img.save(self.test_image_path)
        
        # Sample elements with bbox
        self.sample_elements = [
            {
                'text': 'Username',
                'resource_id': 'username',
                'class_name': 'input',
                'bbox': {'x': 155, 'y': 202, 'width': 470, 'height': 32}
            },
            {
                'text': 'Password',
                'resource_id': 'password',
                'class_name': 'input',
                'bbox': {'x': 155, 'y': 265, 'width': 470, 'height': 32}
            },
            {
                'text': 'Login',
                'class_name': 'button',
                'bbox': {'x': 155, 'y': 312, 'width': 162, 'height': 59}
            }
        ]
    
    def test_library_initialization(self):
        """Test that BBoxVisualizer can be initialized."""
        visualizer = BBoxVisualizer()
        self.assertIsNotNone(visualizer)
        self.assertEqual(visualizer.default_color, 'red')
        self.assertEqual(visualizer.default_width, 3)
    
    def test_draw_bbox_on_screenshot_returns_path(self):
        """Test that draw_bbox_on_screenshot returns a valid path."""
        output_path = self.visualizer.draw_bbox_on_screenshot(
            self.test_image_path,
            self.sample_elements
        )
        
        self.assertIsNotNone(output_path)
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('_annotated.png'))
    
    def test_draw_bbox_creates_valid_image(self):
        """Test that the annotated image is valid."""
        output_path = self.visualizer.draw_bbox_on_screenshot(
            self.test_image_path,
            self.sample_elements
        )
        
        # Verify we can open the annotated image
        img = Image.open(output_path)
        self.assertEqual(img.size, (800, 600))
        self.assertEqual(img.mode, 'RGB')
    
    def test_draw_bbox_with_custom_output_path(self):
        """Test draw_bbox with custom output path."""
        custom_output = os.path.join(self.temp_dir, 'custom_annotated.png')
        
        output_path = self.visualizer.draw_bbox_on_screenshot(
            self.test_image_path,
            self.sample_elements,
            output_path=custom_output
        )
        
        self.assertEqual(output_path, custom_output)
        self.assertTrue(os.path.exists(custom_output))
    
    def test_draw_bbox_with_empty_elements(self):
        """Test draw_bbox with no elements."""
        output_path = self.visualizer.draw_bbox_on_screenshot(
            self.test_image_path,
            []
        )
        
        # Should still create an image (just no annotations)
        self.assertTrue(os.path.exists(output_path))
    
    def test_draw_bbox_with_missing_bbox(self):
        """Test draw_bbox with elements missing bbox."""
        elements_no_bbox = [
            {'text': 'Element without bbox', 'class_name': 'button'}
        ]
        
        output_path = self.visualizer.draw_bbox_on_screenshot(
            self.test_image_path,
            elements_no_bbox
        )
        
        # Should handle gracefully
        self.assertTrue(os.path.exists(output_path))
    
    def test_draw_bbox_with_custom_color(self):
        """Test draw_bbox with custom color."""
        output_path = self.visualizer.draw_bbox_on_screenshot(
            self.test_image_path,
            self.sample_elements,
            color='blue'
        )
        
        self.assertTrue(os.path.exists(output_path))
    
    def test_annotate_elements_creates_timestamped_file(self):
        """Test that annotate_elements creates a timestamped file."""
        output_dir = os.path.join(self.temp_dir, 'annotated')
        
        output_path = self.visualizer.annotate_elements(
            self.sample_elements,
            self.test_image_path,
            output_dir=output_dir
        )
        
        # Verify output directory was created
        self.assertTrue(os.path.exists(output_dir))
        
        # Verify file has timestamp
        self.assertTrue('_annotated_' in output_path)
        self.assertTrue(os.path.exists(output_path))
    
    def test_library_metadata(self):
        """Test that library metadata is correct."""
        self.assertEqual(BBoxVisualizer.ROBOT_LIBRARY_SCOPE, 'GLOBAL')
        self.assertIsNotNone(BBoxVisualizer.ROBOT_LIBRARY_VERSION)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


class TestBBoxVisualizerIntegration(unittest.TestCase):
    """Integration tests for BBoxVisualizer with real bbox data."""
    
    def test_visualize_login_form(self):
        """Test visualizing a login form (from actual collector output)."""
        visualizer = BBoxVisualizer()
        
        # Real data from collector output (from user's example)
        elements = [
            {
                'text': '',
                'resource_id': 'username',
                'content_desc': '',
                'label': 'Username',
                'class_name': 'input',
                'role': '',
                'name': 'username',
                'type': 'text',
                'href': '',
                'clickable': True,
                'enabled': True,
                'bbox': {'x': 155, 'y': 202, 'width': 470, 'height': 32}
            },
            {
                'text': '',
                'resource_id': 'password',
                'content_desc': '',
                'label': 'Password',
                'class_name': 'input',
                'role': '',
                'name': 'password',
                'type': 'password',
                'href': '',
                'clickable': True,
                'enabled': True,
                'bbox': {'x': 155, 'y': 265, 'width': 470, 'height': 32}
            },
            {
                'text': 'Login',
                'resource_id': '',
                'content_desc': '',
                'label': '',
                'class_name': 'button',
                'role': '',
                'name': '',
                'type': 'submit',
                'href': '',
                'clickable': True,
                'enabled': True,
                'bbox': {'x': 155, 'y': 312, 'width': 162, 'height': 59}
            },
            {
                'text': 'Elemental Selenium',
                'resource_id': '',
                'content_desc': '',
                'label': '',
                'class_name': 'a',
                'role': '',
                'name': '',
                'type': '',
                'href': 'http://elementalselenium.com/',
                'clickable': True,
                'enabled': True,
                'bbox': {'x': 614, 'y': 446, 'width': 141, 'height': 18}
            }
        ]
        
        # Create a mock screenshot
        temp_dir = tempfile.mkdtemp()
        screenshot_path = os.path.join(temp_dir, 'login_page.png')
        img = Image.new('RGB', (1024, 768), 'white')
        img.save(screenshot_path)
        
        # Annotate
        output_path = visualizer.draw_bbox_on_screenshot(
            screenshot_path,
            elements
        )
        
        # Verify
        self.assertTrue(os.path.exists(output_path))
        
        # Verify all 4 elements were annotated
        annotated_img = Image.open(output_path)
        self.assertIsNotNone(annotated_img)
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    print("=" * 60)
    print("Testing BBoxVisualizer Library")
    print("=" * 60)
    print()
    
    # Run tests
    unittest.main(verbosity=2)






