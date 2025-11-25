from Agent.platforms import DeviceConnector
from Agent.executors.base_executor import BaseExecutor


class MobileExecutor(BaseExecutor):
    """Executor for mobile platform actions using AppiumLibrary.
    
    This class wraps Robot Framework AppiumLibrary keywords and provides
    a clean interface for tool execution.
    """
    
    def __init__(self, platform: DeviceConnector) -> None:
        super().__init__(platform)

