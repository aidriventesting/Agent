from typing import Any, Dict


class IOSLocatorBuilder:
    """Builds Appium locators for iOS elements."""
    
    def build(self, element: Dict[str, Any], robust: bool = False) -> str:
        raise NotImplementedError("iOS locator builder not implemented yet")
    
    def build_priority(self, element: Dict[str, Any]) -> str:
        raise NotImplementedError("iOS locator builder not implemented yet")
    
    def build_robust(self, element: Dict[str, Any]) -> str:
        raise NotImplementedError("iOS locator builder not implemented yet")

