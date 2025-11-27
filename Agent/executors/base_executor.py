from typing import Any, Dict
from robot.libraries.BuiltIn import BuiltIn


class BaseExecutor:
    """Base executor class for both mobile and web platforms.
    
    Provides shared functionality for executing Robot Framework keywords
    and building locators from element attributes.
    """
    
    def __init__(self, platform) -> None:
        """Initialize executor with platform connector.
        
        Args:
            platform: Platform connector (DeviceConnector or WebConnectorRF)
        """
        self.platform = platform
    
    def run_keyword(self, keyword_name: str, *args: Any) -> Any:
        """Execute a Robot Framework keyword.
        
        Args:
            keyword_name: Name of the RF keyword to execute
            *args: Arguments to pass to the keyword
            
        Returns:
            Result from the keyword execution
            
        Raises:
            Exception: If keyword execution fails
        """
        # No logging here - Robot Framework keywords already log their execution
        return BuiltIn().run_keyword(keyword_name, *args)
    
    def build_locator(self, element: Dict[str, Any]) -> str:
        """Build locator from element attributes using platform connector.
        
        Args:
            element: Element dictionary with attributes
            
        Returns:
            Locator string appropriate for the platform
        """
        return self.platform.build_locator_from_element(element)
