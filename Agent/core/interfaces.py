from typing import Any, Dict, List, Protocol, runtime_checkable
#TODO: review and plug

@runtime_checkable
class PlatformProtocol(Protocol):
    """Protocol for platform connectors (web/mobile)."""
    
    def get_platform(self) -> str:
        """Return platform name ('web', 'android', 'ios')."""
        ...
    
    def get_screenshot_base64(self) -> str:
        """Capture screenshot as base64 string."""
        ...
    
    def collect_ui_candidates(self, max_items: int = 500) -> List[Dict[str, Any]]:
        """Collect interactive UI elements."""
        ...
    
    def embed_image_to_log(self, base64_screenshot: str, width: int = 400) -> None:
        """Embed image into Robot Framework log."""
        ...


@runtime_checkable
class CollectorProtocol(Protocol):
    """Protocol for UI element collectors."""
    
    def collect_elements(self, max_items: int = 500) -> List[Dict[str, Any]]:
        """Collect interactive UI elements from current screen/page."""
        ...
    
    def get_name(self) -> str:
        """Return collector strategy name."""
        ...


@runtime_checkable
class LocatorProtocol(Protocol):
    """Protocol for locator builders."""
    
    def build(self, element: Dict[str, Any]) -> str:
        """Build locator string from element attributes."""
        ...


@runtime_checkable
class ExecutorProtocol(Protocol):
    """Protocol for action executors."""
    
    def run_keyword(self, keyword_name: str, *args: Any) -> Any:
        """Execute a Robot Framework keyword."""
        ...
    
    def build_locator(self, element: Dict[str, Any]) -> str:
        """Build locator from element attributes."""
        ...

