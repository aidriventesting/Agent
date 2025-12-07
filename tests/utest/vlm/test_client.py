import unittest
from unittest.mock import Mock, patch, MagicMock
from Agent.ai.vlm._client import OmniParserClient, OmniParserError


class TestOmniParserClient(unittest.TestCase):
    @patch('Agent.ai.vlm._client.Client')
    def test_parse_image_with_local_path(self, mock_client_class):
        mock_client_instance = MagicMock()
        mock_client_instance.predict.return_value = ("/path/to/image.webp", "icon 0: {'type': 'icon'}")
        mock_client_class.return_value = mock_client_instance
        
        client = OmniParserClient()
        image_temp_path, response_text = client.parse_image(
            image_path="tests/_data/images/screenshots/screenshot-Google Pixel 5-11.0.png"
        )
        
        self.assertIsInstance(image_temp_path, str)
        self.assertIsInstance(response_text, str)
        mock_client_instance.predict.assert_called_once()


if __name__ == "__main__":
    unittest.main()

