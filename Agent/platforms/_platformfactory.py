from typing import Union
from Agent.platforms._mobileconnector import DeviceConnector
from Agent.platforms._webconnector import WebConnectorRF
from robot.api import logger

try:
    from Browser import Browser
    _has_browser = True
except ImportError:
    _has_browser = False

try:
    from AppiumLibrary import AppiumLibrary
    _has_appium = True
except ImportError:
    _has_appium = False


def create_platform(platform_type: str = "auto") -> Union[DeviceConnector, WebConnectorRF]:
    """
    Factory function to create the appropriate platform connector.
    
    Args:
        platform_type: "auto", "web", or "mobile"
        
    Returns:
        Platform connector instance (DeviceConnector or WebConnectorRF)
    """
    if platform_type == "web":
        logger.info("Creating WebConnectorRF for web automation")
        return WebConnectorRF()
    
    elif platform_type == "mobile":
        logger.info("Creating DeviceConnector for mobile automation")
        return DeviceConnector()
    
    else:  # auto - check which library is ACTIVE in Robot Framework
        from robot.libraries.BuiltIn import BuiltIn
        
        # Check if Browser is active
        try:
            BuiltIn().get_library_instance('Browser')
            logger.info("Browser library active - using WebConnectorRF")
            return WebConnectorRF()
        except Exception:
            pass
        
        # Check if AppiumLibrary is active
        try:
            BuiltIn().get_library_instance('AppiumLibrary')
            logger.info("AppiumLibrary active - using DeviceConnector")
            return DeviceConnector()
        except Exception:
            pass
        
        # Fallback to import check
        if _has_browser:
            logger.info("Fallback: Browser installed - using WebConnectorRF")
            return WebConnectorRF()
        
        if _has_appium:
            logger.info("Fallback: AppiumLibrary installed - using DeviceConnector")
            return DeviceConnector()
        
        logger.warn("No platform library detected, defaulting to DeviceConnector")
        return DeviceConnector()

