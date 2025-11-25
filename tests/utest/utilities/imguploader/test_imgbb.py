"""
Tests unitaires pour ImgBBUploader (_imgbb.py)
Tests basiques : upload, gestion des erreurs
"""
import unittest
from unittest.mock import patch, MagicMock
from Agent.utilities.imguploader._imgbb import ImgBBUploader


class TestImgBBUploader(unittest.TestCase):
    """Tests basiques pour ImgBBUploader"""
    
    def setUp(self):
        self.base64_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    def test_successful_upload(self):
        """Test: Upload réussi retourne l'URL"""
        with patch('Agent.utilities.imguploader._imgbb.Config') as MockConfig, \
             patch('Agent.utilities.imguploader._imgbb.requests.post') as mock_post:
            
            MockConfig.return_value.IMGBB_API_KEY = "fake_api_key"
            
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "data": {"display_url": "https://i.ibb.co/test123/image.png"}
            }
            mock_post.return_value = mock_response
            
            uploader = ImgBBUploader()
            result = uploader.upload_from_base64(self.base64_data)
            
            self.assertEqual(result, "https://i.ibb.co/test123/image.png")
    
    def test_api_error_returns_none(self):
        """Test: Erreur API retourne None"""
        with patch('Agent.utilities.imguploader._imgbb.Config') as MockConfig, \
             patch('Agent.utilities.imguploader._imgbb.requests.post') as mock_post:
            
            MockConfig.return_value.IMGBB_API_KEY = "fake_api_key"
            mock_post.side_effect = Exception("API Error")
            
            uploader = ImgBBUploader()
            result = uploader.upload_from_base64(self.base64_data)
            
            self.assertIsNone(result)
    
    def test_invalid_json_returns_none(self):
        """Test: JSON invalide retourne None"""
        with patch('Agent.utilities.imguploader._imgbb.Config') as MockConfig, \
             patch('Agent.utilities.imguploader._imgbb.requests.post') as mock_post:
            
            MockConfig.return_value.IMGBB_API_KEY = "fake_api_key"
            
            mock_response = MagicMock()
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_post.return_value = mock_response
            
            uploader = ImgBBUploader()
            result = uploader.upload_from_base64(self.base64_data)
            
            self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

