from typing import Any, Dict, Literal

StrategyType = Literal['auto', 'id_only', 'bounds', 'xpath_attrs', 'xpath_all']


class MobileLocatorBuilder:
    """Facade that dispatches to platform-specific locator builders with lazy init and flexible platform."""
    
    def __init__(self, platform: str = None):
        self._platform = platform
        self._builder = None
    
    def set_platform(self, platform: str):
        if self._platform != platform:
            self._platform = platform
            self._builder = None
    
    def _get_builder(self):
        if self._builder is None:
            if self._platform == 'ios':
                from Agent.platforms.locators.ios_locator import IOSLocatorBuilder
                self._builder = IOSLocatorBuilder()
            else:
                from Agent.platforms.locators.android_locator import AndroidLocatorBuilder
                self._builder = AndroidLocatorBuilder()
        return self._builder
    
    def build(self, element: Dict[str, Any], strategy: StrategyType = 'auto') -> str:
        """
        Args:
            element: Dict with raw XML attributes
            strategy: 'auto' | 'id_only' | 'bounds' | 'xpath_attrs' | 'xpath_all'
        Returns:
            Appium locator string
        Example: build(elem, 'id_only') -> 'id=com.android:id/button'
        """
        return self._get_builder().build(element, strategy=strategy)

