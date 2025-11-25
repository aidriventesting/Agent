from typing import Any, Dict
from Agent.platforms import DeviceConnector
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger


class MobileExecutor:
    """Executor for mobile platform actions using AppiumLibrary.
    
    This class wraps Robot Framework AppiumLibrary keywords and provides
    a clean interface for tool execution.
    """
    
    def __init__(self, platform: DeviceConnector) -> None:
        self.platform = platform
    
    def run_keyword(self, keyword_name: str, *args: Any) -> Any:
        """Execute a Robot Framework keyword."""
        try:
            args_str = " ".join([str(a) for a in args]) if args else ""
            logger.debug(f"EXECUTING: {keyword_name} {args_str}".strip())
            logger.info(f"▶️ RF: {keyword_name} {args_str}")

            result = BuiltIn().run_keyword(keyword_name, *args)

            logger.info(f"SUCCESS: {keyword_name} executed successfully")
            return result
        except Exception as exc:
            raise
    
    def build_locator(self, element: Dict[str, Any]) -> str:
        """Build locator from element attributes using platform connector."""
        return self.platform.build_locator_from_element(element)

