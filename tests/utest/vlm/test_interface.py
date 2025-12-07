import unittest
from unittest.mock import Mock, patch, MagicMock
from Agent.ai.vlm.interface import OmniParserOrchestrator


class TestOmniParserOrchestrator(unittest.TestCase):
    @patch('Agent.ai.vlm.interface.OmniParserElementSelector')
    @patch('Agent.ai.vlm.interface.OmniParserClient')
    def test_find_element_success(self, mock_client_class, mock_selector_class):
        mock_client_instance = MagicMock()
        mock_client_instance.parse_image.return_value = (
            "/tmp/image.webp",
            "icon 3: {'type': 'icon', 'bbox': [0.41, 0.17, 0.57, 0.26], 'interactivity': True, 'content': 'YouTube '}"
        )
        mock_client_class.return_value = mock_client_instance
        
        mock_selector_instance = MagicMock()
        mock_selector_instance.select_element.return_value = {
            "element_key": "icon3",
            "element_data": {
                'type': 'icon',
                'bbox': [0.41, 0.17, 0.57, 0.26],
                'interactivity': True,
                'content': 'YouTube '
            },
            "confidence": "high",
            "reason": "Matches YouTube"
        }
        mock_selector_class.return_value = mock_selector_instance
        
        orchestrator = OmniParserOrchestrator()
        result = orchestrator.find_element(
            element_description="YouTube icon",
            image_path="test.png",
            element_type="interactive"
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result['element_key'], 'icon3')
        self.assertIn('image_temp_path', result)
    
    @patch('Agent.ai.vlm.interface.OmniParserElementSelector')
    @patch('Agent.ai.vlm.interface.OmniParserClient')
    def test_find_element_no_elements(self, mock_client_class, mock_selector_class):
        mock_client_instance = MagicMock()
        mock_client_instance.parse_image.return_value = ("/tmp/image.webp", "")
        mock_client_class.return_value = mock_client_instance
        
        orchestrator = OmniParserOrchestrator()
        result = orchestrator.find_element(
            element_description="YouTube icon",
            image_path="test.png"
        )
        
        self.assertIsNone(result)
    
    def test_bbox_to_pixels(self):
        bbox_normalized = [0.419, 0.170, 0.574, 0.266]
        image_width = 1080
        image_height = 1920
        
        pixels = OmniParserOrchestrator.bbox_to_pixels(
            bbox_normalized, image_width, image_height
        )
        
        self.assertEqual(len(pixels), 4)
        self.assertIsInstance(pixels[0], int)
        self.assertIsInstance(pixels[1], int)
        self.assertIsInstance(pixels[2], int)
        self.assertIsInstance(pixels[3], int)
        
        x1, y1, x2, y2 = pixels
        self.assertGreater(x2, x1)
        self.assertGreater(y2, y1)
    
    @patch('Agent.ai.vlm.interface.Image')
    def test_bbox_to_pixels_from_image(self, mock_image):
        mock_img = MagicMock()
        mock_img.size = (1080, 1920)
        mock_image.open.return_value.__enter__.return_value = mock_img
        
        bbox_normalized = [0.419, 0.170, 0.574, 0.266]
        
        pixels = OmniParserOrchestrator.bbox_to_pixels_from_image(
            bbox_normalized, "test.png"
        )
        
        self.assertEqual(len(pixels), 4)
        x1, y1, x2, y2 = pixels
        self.assertGreater(x2, x1)
        self.assertGreater(y2, y1)
    
    def test_get_element_center_coordinates(self):
        element_result = {
            "element_key": "icon3",
            "element_data": {
                "bbox": [0.0, 0.0, 0.5, 0.5]
            },
            "image_temp_path": "test.png"
        }
        
        with patch.object(OmniParserOrchestrator, 'bbox_to_pixels_from_image', return_value=(0, 0, 100, 100)):
            x_center, y_center = OmniParserOrchestrator.get_element_center_coordinates(element_result)
            
            self.assertEqual(x_center, 50)
            self.assertEqual(y_center, 50)


if __name__ == "__main__":
    unittest.main()

