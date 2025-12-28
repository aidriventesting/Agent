from Agent.platforms._mobileconnector import DeviceConnector
from Agent.platforms._platformfactory import create_platform
from Agent.platforms.locators import MobileLocatorBuilder
from Agent.platforms.collectors import XMLCollector

# Placeholder for future web support
WebConnectorRF = None

__all__ = [
    "DeviceConnector",
    "WebConnectorRF",
    "create_platform",
    "MobileLocatorBuilder",
    "XMLCollector",
]
