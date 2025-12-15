"""
Factory and Registry for UI Collectors.

This module provides a registry pattern to manage different UI collection
strategies and switch between them dynamically.
"""

from typing import Dict, List, Type
from robot.api import logger
from Agent.platforms.collectors.base_collector import BaseUICollector


class CollectorRegistry:
    """
    Registry for UI collector strategies.
    
    Provides a centralized way to:
    - Register new collector strategies
    - Create collector instances by name
    - List available strategies
    """
    
    _collectors: Dict[str, Type[BaseUICollector]] = {}
    
    @classmethod
    def register(cls, name: str, collector_class: Type[BaseUICollector]) -> None:
        """
        Register a new collector strategy.
        
        Args:
            name: Unique identifier for the strategy (e.g., "js_query")
            collector_class: Class implementing BaseUICollector
        """
        if not issubclass(collector_class, BaseUICollector):
            raise TypeError(f"{collector_class} must inherit from BaseUICollector")
        
        cls._collectors[name] = collector_class
        logger.debug(f"Registered UI collector: '{name}' -> {collector_class.__name__}")
    
    @classmethod
    def create(cls, strategy: str) -> BaseUICollector:
        """
        Create a collector instance by strategy name.
        
        Args:
            strategy: Name of the registered strategy
            
        Returns:
            Instance of the requested collector
            
        Raises:
            ValueError: If strategy is not registered
        """
        if strategy not in cls._collectors:
            available = cls.list_available()
            raise ValueError(
                f"Unknown collector strategy: '{strategy}'. "
                f"Available strategies: {available}"
            )
        
        collector_class = cls._collectors[strategy]
        instance = collector_class()
        logger.debug(f"Created collector instance: {strategy} ({collector_class.__name__})")
        return instance
    
    @classmethod
    def list_available(cls) -> List[str]:
        """
        List all registered collector strategies.
        
        Returns:
            List of strategy names
        """
        return list(cls._collectors.keys())
    
    @classmethod
    def is_registered(cls, strategy: str) -> bool:
        """
        Check if a strategy is registered.
        
        Args:
            strategy: Name of the strategy
            
        Returns:
            True if registered, False otherwise
        """
        return strategy in cls._collectors


# Auto-register built-in collectors
def _register_builtin_collectors():
    """Register all built-in collector strategies."""
    try:
        from Agent.platforms.collectors.js_query_collector import JSQueryCollector
        CollectorRegistry.register("js_query", JSQueryCollector)
    except ImportError as e:
        logger.warn(f"Could not register JSQueryCollector: {e}")
    
    try:
        from Agent.platforms.collectors.xml_collector import XMLCollector
        CollectorRegistry.register("xml", XMLCollector)
    except ImportError as e:
        logger.warn(f"Could not register XMLCollector: {e}")


# Auto-register on module import
_register_builtin_collectors()

