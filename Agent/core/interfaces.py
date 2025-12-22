from typing import Any, Dict, Protocol, runtime_checkable


@runtime_checkable
class ExecutorProtocol(Protocol):
    """Protocol for action executors."""
    
    def run_keyword(self, keyword_name: str, *args: Any) -> Any:
        ...
    
    def build_locator(self, element: Dict[str, Any]) -> str:
        ...
