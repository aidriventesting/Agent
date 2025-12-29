from typing import Any, Dict
from Agent.platforms.locators.android_locator import AndroidLocatorBuilder
from Agent.platforms.locators.ios_locator import IOSLocatorBuilder


class MobileLocatorBuilder:
    """Facade that dispatches to platform-specific locator builders."""
    
    def __init__(self, platform: str = "android"):
        self._platform = platform
        self._android_builder = AndroidLocatorBuilder()
        self._ios_builder = IOSLocatorBuilder()
    
    def set_platform(self, platform: str) -> None:
        self._platform = platform
    
    def build(self, element: Dict[str, Any], robust: bool = False) -> str:
        if self._platform == "ios":
            return self._ios_builder.build(element, robust=robust)
        return self._android_builder.build(element, robust=robust)
    
    def build_priority(self, element: Dict[str, Any]) -> str:
        if self._platform == "ios":
            return self._ios_builder.build_priority(element)
        return self._android_builder.build_priority(element)
    
    def build_robust(self, element: Dict[str, Any]) -> str:
        if self._platform == "ios":
            return self._ios_builder.build_robust(element)
        return self._android_builder.build_robust(element)
