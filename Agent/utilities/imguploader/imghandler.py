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
            logger.warn("Fallback: returning the image in base64 (no provider configured)")
            return f"data:image/png;base64,{base64_data}"
        
        # Try each provider in order
        for idx, uploader in enumerate(self.uploaders):
            provider_name = type(uploader).__name__
            logger.debug(f"Attempting upload with {provider_name} ({idx+1}/{len(self.uploaders)})")
            try:
                result = uploader.upload_from_base64(base64_data)
                
                if result:
                    logger.info(f"Image uploaded successfully with {provider_name}")
                    return result
                else:
                    logger.warn(f"{provider_name} failed to upload (returned None)")
                    
            except Exception as e:
                logger.warn(f"{provider_name} raised an error: {str(e)}")
        
        logger.warn("Fallback: returning the image in base64 (all providers failed)")
        return f"data:image/png;base64,{base64_data}"

    def _build_uploaders_list(self, service: str) -> list[BaseImageUploader]:
        """
        Builds list of uploaders based on service selection.
        In auto mode, adds all available providers (imgbb has priority).
        """
        uploaders = []
        
        # Debug config loading
        has_imgbb = bool(self.config.IMGBB_API_KEY)
        has_freeimage = bool(self.config.FREEIMAGEHOST_API_KEY)
        logger.debug(f"ImageUploader init: service={service}, has_imgbb={has_imgbb}, has_freeimage={has_freeimage}")
        
        if service == "imgbb" and self.config.IMGBB_API_KEY:
            uploaders.append(ImgBBUploader())
        elif service == "freeimagehost" and self.config.FREEIMAGEHOST_API_KEY:
            uploaders.append(FreeImageHostUploader())
        elif service == "auto":
            # Priority order: imgbb first, then freeimagehost as fallback
            if self.config.IMGBB_API_KEY:
                uploaders.append(ImgBBUploader())
            if self.config.FREEIMAGEHOST_API_KEY:
                uploaders.append(FreeImageHostUploader())
        
        if not uploaders:
            logger.warn("No upload service configured. Images will be returned in base64.")
        else:
            logger.debug(f"Configured uploaders: {[type(u).__name__ for u in uploaders]}")
        
        return uploaders

