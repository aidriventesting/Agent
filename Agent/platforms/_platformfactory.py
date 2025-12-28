from Agent.platforms._mobileconnector import DeviceConnector
from robot.api import logger


def create_platform(platform_type: str = "auto") -> DeviceConnector:
    """
    Factory function to create the platform connector.
    Currently Android-only, web support coming later.
    """
    if platform_type == "mobile" or platform_type == "auto":
        logger.info("Creating DeviceConnector for mobile automation")
        return DeviceConnector()
    
    raise ValueError(f"Platform '{platform_type}' not supported. Use 'mobile' or 'auto'.")
