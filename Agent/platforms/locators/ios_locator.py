from typing import Any, Dict


class IOSLocatorBuilder:
    """Builds Appium locators for iOS elements."""
    
    def build(self, element: Dict[str, Any], strategy: str = 'auto') -> str:
        raise NotImplementedError("iOS locator builder not implemented yet")
    
    #TODO: see if this should be private after adding locator strategies ( build )
    def build_identifiers_only(self, element: Dict[str, Any]) -> str:
        raise NotImplementedError("iOS locator builder not implemented yet")
    
    def build_by_bounds(self, element: Dict[str, Any]) -> str:
        raise NotImplementedError("iOS locator builder not implemented yet")
    
    def build_xpath_attributes(self, element: Dict[str, Any]) -> str:
        raise NotImplementedError("iOS locator builder not implemented yet")
    
    def build_xpath_all(self, element: Dict[str, Any]) -> str:
        raise NotImplementedError("iOS locator builder not implemented yet")

