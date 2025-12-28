from typing import Optional
from Agent.config.config import Config
from Agent.utilities.imguploader._imgbb import ImgBBUploader
from Agent.utilities.imguploader._imghost import FreeImageHostUploader
from Agent.utilities.imguploader._imgbase import BaseImageUploader
from robot.api import logger

class ImageUploader:
    """
    Handles multiple fallback cases:
    ✅ No provider configured → returns base64 + warning
    ✅ Upload fails (returns None) → tries alternative provider if in auto mode, then returns base64
    ✅ Exception raised → tries alternative provider if in auto mode, then returns base64
    """
    def __init__(self, service: str = "auto"):
        self.config = Config()
        self.service = service
        self.uploaders = self._build_uploaders_list(service)

    def upload_from_base64(self, base64_data: str) -> Optional[str]:
        """
        Attempts to upload the image with available providers.
        In auto mode, falls back to alternative providers if one fails.
        Returns base64 if all providers fail or none configured.
        """
        if not self.uploaders:
            logger.debug("No upload provider configured, using base64")
            return f"data:image/png;base64,{base64_data}"
        
        for uploader in self.uploaders:
            provider_name = type(uploader).__name__
            try:
                result = uploader.upload_from_base64(base64_data)
                if result:
                    logger.debug(f"Image uploaded via {provider_name}")
                    return result
            except Exception:
                pass
        
        logger.debug("Upload failed, using base64 fallback")
        return f"data:image/png;base64,{base64_data}"

    def _build_uploaders_list(self, service: str) -> list[BaseImageUploader]:
        uploaders = []
        
        if service == "imgbb" and self.config.IMGBB_API_KEY:
            uploaders.append(ImgBBUploader())
        elif service == "freeimagehost" and self.config.FREEIMAGEHOST_API_KEY:
            uploaders.append(FreeImageHostUploader())
        elif service == "auto":
            if self.config.IMGBB_API_KEY:
                uploaders.append(ImgBBUploader())
            if self.config.FREEIMAGEHOST_API_KEY:
                uploaders.append(FreeImageHostUploader())
        
        return uploaders

