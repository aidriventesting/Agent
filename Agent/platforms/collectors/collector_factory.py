"""
Factory and Registry for UI Collectors.
"""

from typing import Dict, List, Type
from robot.api import logger
from Agent.platforms.collectors.base_collector import BaseUICollector


class CollectorRegistry:
    """Registry for UI collector strategies."""
    
    _collectors: Dict[str, Type[BaseUICollector]] = {}
    
    @classmethod
    def register(cls, name: str, collector_class: Type[BaseUICollector]) -> None:
        if not issubclass(collector_class, BaseUICollector):
            raise TypeError(f"{collector_class} must inherit from BaseUICollector")
        cls._collectors[name] = collector_class
        logger.debug(f"Registered UI collector: '{name}' -> {collector_class.__name__}")
    
    @classmethod
    def create(cls, strategy: str) -> BaseUICollector:
        if strategy not in cls._collectors:
            available = cls.list_available()
            raise ValueError(f"Unknown strategy: '{strategy}'. Available: {available}")
        
        collector_class = cls._collectors[strategy]
        return collector_class()
    
    @classmethod
    def list_available(cls) -> List[str]:
        return list(cls._collectors.keys())
    
    @classmethod
    def is_registered(cls, strategy: str) -> bool:
        return strategy in cls._collectors


def _register_builtin_collectors():
    try:
        from Agent.platforms.collectors.xml_collector import XMLCollector
        CollectorRegistry.register("xml", XMLCollector)
    except ImportError as e:
        logger.warn(f"Could not register XMLCollector: {e}")


_register_builtin_collectors()
