from Agent.platforms._webconnector import WebConnectorRF
from Agent.executors.base_executor import BaseExecutor


class WebExecutor(BaseExecutor):
    """Executor for web platform actions using Browser library.
    
    This class wraps Robot Framework Browser library keywords and provides
    a clean interface for tool execution.
    """
    
    def __init__(self, platform: WebConnectorRF) -> None:
        super().__init__(platform)

