"""
Tests unitaires pour FreeImageHostUploader (_imghost.py)
Tests basiques : upload, gestion des erreurs
"""
import unittest
from unittest.mock import patch, MagicMock
from Agent.utilities.imguploader._imghost import FreeImageHostUploader


class TestFreeImageHostUploader(unittest.TestCase):
    """Tests basiques pour FreeImageHostUploader"""
    
    def setUp(self):
        self.base64_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    def test_successful_upload(self):
        """Test: Upload réussi retourne l'URL"""
        with patch('Agent.utilities.imguploader._imghost.Config') as MockConfig, \
             patch('Agent.utilities.imguploader._imghost.requests.post') as mock_post:
            
            MockConfig.return_value.FREEIMAGEHOST_API_KEY = "fake_api_key"
            
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "image": {"display_url": "https://freeimage.host/test456/image.png"}
            }
            mock_post.return_value = mock_response
            
            uploader = FreeImageHostUploader()
            result = uploader.upload_from_base64(self.base64_data)
            
            self.assertEqual(result, "https://freeimage.host/test456/image.png")
    
    def test_api_error_returns_none(self):
        """Test: Erreur API retourne None"""
        with patch('Agent.utilities.imguploader._imghost.Config') as MockConfig, \
             patch('Agent.utilities.imguploader._imghost.requests.post') as mock_post:
            
            MockConfig.return_value.FREEIMAGEHOST_API_KEY = "fake_api_key"
            mock_post.side_effect = Exception("Network timeout")
            
            uploader = FreeImageHostUploader()
            result = uploader.upload_from_base64(self.base64_data)
            
            self.assertIsNone(result)
    
    def test_url_fallback_to_url_field(self):
        """Test: Si display_url absent, utilise url"""
        with patch('Agent.utilities.imguploader._imghost.Config') as MockConfig, \
             patch('Agent.utilities.imguploader._imghost.requests.post') as mock_post:
            
            MockConfig.return_value.FREEIMAGEHOST_API_KEY = "fake_api_key"
            
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "image": {"url": "https://freeimage.host/fallback/image.png"}
            }
            mock_post.return_value = mock_response
            
            uploader = FreeImageHostUploader()
            result = uploader.upload_from_base64(self.base64_data)
            
            self.assertEqual(result, "https://freeimage.host/fallback/image.png")


if __name__ == '__main__':
    unittest.main()

