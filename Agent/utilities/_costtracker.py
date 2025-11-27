"""
Cost Tracker Utility
Tracks and accumulates API costs across test execution.
"""
from typing import Dict, Optional
from threading import Lock
from robot.api import logger


class CostTracker:
    """
    Singleton class to track API costs during test execution.
    Thread-safe implementation for parallel test execution.
    """
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._test_costs: Dict[str, Dict[str, float]] = {}
            self._current_test: Optional[str] = None
            self._session_total: float = 0.0
            self._initialized = True
    
    def start_test(self, test_name: str):
        """
        Initialize cost tracking for a new test.
        
        Args:
            test_name: Name of the test case
        """
        with self._lock:
            self._current_test = test_name
            if test_name not in self._test_costs:
                self._test_costs[test_name] = {
                    'total': 0.0,
                    'input_cost': 0.0,
                    'output_cost': 0.0,
                    'calls': 0,
                    'models': set()
                }
            logger.debug(f"Started cost tracking for test: {test_name}")
    
    def add_cost(self, input_cost: float, output_cost: float, model: str = "unknown"):
        """
        Add cost for a single API call.
        
        Args:
            input_cost: Cost for input tokens
            output_cost: Cost for output tokens
            model: Model name used for the call
        """
        with self._lock:
            if self._current_test is None:
                logger.warn("No active test for cost tracking. Call start_test() first.")
                return
            
            total_cost = input_cost + output_cost
            test_data = self._test_costs[self._current_test]
            test_data['input_cost'] += input_cost
            test_data['output_cost'] += output_cost
            test_data['total'] += total_cost
            test_data['calls'] += 1
            test_data['models'].add(model)
            self._session_total += total_cost
            
            logger.debug(
                f"API call cost: ${total_cost:.6f} (input: ${input_cost:.6f}, "
                f"output: ${output_cost:.6f}, model: {model})"
            )
    
    def get_test_cost(self, test_name: Optional[str] = None) -> Dict[str, float]:
        """
        Get cost information for a specific test.
        
        Args:
            test_name: Name of the test. If None, uses current test.
            
        Returns:
            Dictionary with cost breakdown
        """
        with self._lock:
            test_name = test_name or self._current_test
            if test_name is None:
                return {'total': 0.0, 'input_cost': 0.0, 'output_cost': 0.0, 'calls': 0, 'models': set()}
            return self._test_costs.get(test_name, {
                'total': 0.0,
                'input_cost': 0.0,
                'output_cost': 0.0,
                'calls': 0,
                'models': set()
            })
    
    def get_session_total(self) -> float:
        """
        Get total cost for the entire session.
        
        Returns:
            Total cost across all tests
        """
        with self._lock:
            return self._session_total
    
    def end_test(self, test_name: Optional[str] = None) -> Dict[str, float]:
        """
        End cost tracking for a test and return summary.
        
        Args:
            test_name: Name of the test. If None, uses current test.
            
        Returns:
            Dictionary with final cost breakdown
        """
        with self._lock:
            test_name = test_name or self._current_test
            if test_name is None:
                return {'total': 0.0, 'input_cost': 0.0, 'output_cost': 0.0, 'calls': 0, 'models': set()}
            
            cost_data = self._test_costs.get(test_name, {
                'total': 0.0,
                'input_cost': 0.0,
                'output_cost': 0.0,
                'calls': 0,
                'models': set()
            })
            
            if self._current_test == test_name:
                self._current_test = None
            
            return cost_data
    
    def reset(self):
        """Reset all cost tracking data."""
        with self._lock:
            self._test_costs.clear()
            self._current_test = None
            self._session_total = 0.0
            logger.debug("Cost tracker reset")
    
    def get_all_test_costs(self) -> Dict[str, Dict[str, float]]:
        """
        Get cost information for all tests.
        
        Returns:
            Dictionary with all test costs
        """
        with self._lock:
            return dict(self._test_costs)
    
    def reset_test(self, test_name: Optional[str] = None):
        """
        Reset cost tracking for a specific test.
        
        Args:
            test_name: Name of the test. If None, uses current test.
        """
        with self._lock:
            test_name = test_name or self._current_test
            if test_name and test_name in self._test_costs:
                old_total = self._test_costs[test_name]['total']
                self._session_total -= old_total
                self._test_costs[test_name] = {
                    'total': 0.0,
                    'input_cost': 0.0,
                    'output_cost': 0.0,
                    'calls': 0,
                    'models': set()
                }
                logger.debug(f"Reset cost tracking for test: {test_name}")

