from typing import Any, Dict
from robot.libraries.BuiltIn import BuiltIn


class KeywordRunner:
    """Runs Robot Framework keywords and builds locators for tools."""
    
    def __init__(self, platform) -> None:
        self.platform = platform
    
    def run_keyword(self, keyword_name: str, *args: Any) -> Any:
        return BuiltIn().run_keyword(keyword_name, *args)
    
    def build_locator(self, element: Dict[str, Any]) -> str:
        return self.platform.build_locator_from_element(element)
