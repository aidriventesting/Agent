"""
Tests unitaires pour ImageUploader (imghandler.py)
Tests basiques : fallback automatique entre providers
"""
import unittest
from unittest.mock import patch, MagicMock
from Agent.utilities.imguploader.imghandler import ImageUploader
from Agent.utilities.imguploader._imgbb import ImgBBUploader
from Agent.utilities.imguploader._imghost import FreeImageHostUploader


class TestImageUploaderBasics(unittest.TestCase):
    """Tests basiques du ImageUploader"""
    
    def setUp(self):
        self.base64_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    def test_no_provider_returns_base64(self):
        """Test: Aucun provider configuré → retourne base64"""
        with patch('Agent.utilities.imguploader.imghandler.Config') as MockConfig:
            MockConfig.return_value.IMGBB_API_KEY = None
            MockConfig.return_value.FREEIMAGEHOST_API_KEY = None
            
            uploader = ImageUploader(service="auto")
            result = uploader.upload_from_base64(self.base64_data)
            
            self.assertIn("data:image/png;base64,", result)
            self.assertIn(self.base64_data, result)
    
    def test_imgbb_success(self):
        """Test: Upload réussi avec imgbb"""
        with patch('Agent.utilities.imguploader.imghandler.Config') as MockConfig, \
             patch.object(ImgBBUploader, 'upload_from_base64') as mock_upload:
            
            MockConfig.return_value.IMGBB_API_KEY = "fake_key"
            MockConfig.return_value.FREEIMAGEHOST_API_KEY = None
            mock_upload.return_value = "https://i.ibb.co/test/image.png"
            
            uploader = ImageUploader(service="auto")
            result = uploader.upload_from_base64(self.base64_data)
            
            self.assertEqual(result, "https://i.ibb.co/test/image.png")
            mock_upload.assert_called_once()
    
    def test_freeimagehost_success(self):
        """Test: Upload réussi avec freeimagehost"""
        with patch('Agent.utilities.imguploader.imghandler.Config') as MockConfig, \
             patch.object(FreeImageHostUploader, 'upload_from_base64') as mock_upload:
            
            MockConfig.return_value.IMGBB_API_KEY = None
            MockConfig.return_value.FREEIMAGEHOST_API_KEY = "fake_key"
            mock_upload.return_value = "https://freeimage.host/test/image.png"
            
            uploader = ImageUploader(service="auto")
            result = uploader.upload_from_base64(self.base64_data)
            
            self.assertEqual(result, "https://freeimage.host/test/image.png")
            mock_upload.assert_called_once()
    
    def test_fallback_imgbb_to_freeimagehost(self):
        """Test: Fallback automatique de imgbb vers freeimagehost en mode auto"""
        with patch('Agent.utilities.imguploader.imghandler.Config') as MockConfig, \
             patch.object(ImgBBUploader, 'upload_from_base64') as mock_imgbb, \
             patch.object(FreeImageHostUploader, 'upload_from_base64') as mock_freeimage:
            
            MockConfig.return_value.IMGBB_API_KEY = "fake_imgbb_key"
            MockConfig.return_value.FREEIMAGEHOST_API_KEY = "fake_freeimage_key"
            
            # imgbb échoue, freeimagehost réussit
            mock_imgbb.return_value = None
            mock_freeimage.return_value = "https://freeimage.host/fallback/image.png"
            
            uploader = ImageUploader(service="auto")
            result = uploader.upload_from_base64(self.base64_data)
            
            # Vérifie que le résultat vient de freeimagehost
            self.assertEqual(result, "https://freeimage.host/fallback/image.png")
            # Vérifie que les deux ont été appelés
            mock_imgbb.assert_called_once()
            mock_freeimage.assert_called_once()
    
    def test_all_providers_fail_returns_base64(self):
        """Test: Tous les providers échouent → retourne base64"""
        with patch('Agent.utilities.imguploader.imghandler.Config') as MockConfig, \
             patch.object(ImgBBUploader, 'upload_from_base64') as mock_imgbb, \
             patch.object(FreeImageHostUploader, 'upload_from_base64') as mock_freeimage:
            
            MockConfig.return_value.IMGBB_API_KEY = "fake_imgbb_key"
            MockConfig.return_value.FREEIMAGEHOST_API_KEY = "fake_freeimage_key"
            
            # Les deux échouent
            mock_imgbb.return_value = None
            mock_freeimage.return_value = None
            
            uploader = ImageUploader(service="auto")
            result = uploader.upload_from_base64(self.base64_data)
            
            # Retourne base64
            self.assertIn("data:image/png;base64,", result)
            # Les deux ont été tentés
            mock_imgbb.assert_called_once()
            mock_freeimage.assert_called_once()
    
    def test_exception_triggers_fallback(self):
        """Test: Exception sur imgbb → fallback vers freeimagehost"""
        with patch('Agent.utilities.imguploader.imghandler.Config') as MockConfig, \
             patch.object(ImgBBUploader, 'upload_from_base64') as mock_imgbb, \
             patch.object(FreeImageHostUploader, 'upload_from_base64') as mock_freeimage:
            
            MockConfig.return_value.IMGBB_API_KEY = "fake_imgbb_key"
            MockConfig.return_value.FREEIMAGEHOST_API_KEY = "fake_freeimage_key"
            
            # imgbb lève une exception, freeimagehost réussit
            mock_imgbb.side_effect = Exception("Network error")
            mock_freeimage.return_value = "https://freeimage.host/rescued/image.png"
            
            uploader = ImageUploader(service="auto")
            result = uploader.upload_from_base64(self.base64_data)
            
            self.assertEqual(result, "https://freeimage.host/rescued/image.png")
    
    def test_explicit_service_no_fallback(self):
        """Test: Service explicite (imgbb) → pas de fallback vers freeimagehost"""
        with patch('Agent.utilities.imguploader.imghandler.Config') as MockConfig, \
             patch.object(ImgBBUploader, 'upload_from_base64') as mock_imgbb, \
             patch.object(FreeImageHostUploader, 'upload_from_base64') as mock_freeimage:
            
            MockConfig.return_value.IMGBB_API_KEY = "fake_imgbb_key"
            MockConfig.return_value.FREEIMAGEHOST_API_KEY = "fake_freeimage_key"
            
            mock_imgbb.return_value = None  # imgbb échoue
            
            uploader = ImageUploader(service="imgbb")  # Service explicite
            result = uploader.upload_from_base64(self.base64_data)
            
            # Retourne base64 sans tenter freeimagehost
            self.assertIn("data:image/png;base64,", result)
            mock_imgbb.assert_called_once()
            mock_freeimage.assert_not_called()  # Ne doit PAS être appelé


if __name__ == '__main__':
    unittest.main()

