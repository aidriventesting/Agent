"""
Robot Framework Test Listener
Automatically logs API costs after each test execution.
"""
from robot.api import logger
from Agent.utilities._costtracker import CostTracker


class CostLoggingListener:
    """
    Robot Framework listener that tracks and logs API costs per test.
    """
    
    ROBOT_LISTENER_API_VERSION = 3
    
    def __init__(self):
        self.cost_tracker = CostTracker()
    
    def start_test(self, data, result):
        """
        Called when a test starts.
        
        Args:
            data: Test data
            result: Test result object
        """
        test_name = result.name
        self.cost_tracker.start_test(test_name)
        logger.debug(f"Started test: {test_name}")
    
    def end_test(self, data, result):
        """
        Called when a test ends. Logs the total cost for the test.
        
        Args:
            data: Test data
            result: Test result object
        """
        test_name = result.name
        cost_data = self.cost_tracker.end_test(test_name)
        
        if cost_data['calls'] > 0:
            logger.info(
                f"\n{'='*60}\n"
                f"API Cost Summary for Test: {test_name}\n"
                f"{'='*60}\n"
                f"  Total API Calls: {cost_data['calls']}\n"
                f"  Input Cost:  ${cost_data['input_cost']:.6f}\n"
                f"  Output Cost: ${cost_data['output_cost']:.6f}\n"
                f"  Total Cost:  ${cost_data['total']:.6f}\n"
                f"{'='*60}",
                html=True
            )
        else:
            logger.debug(f"No API calls made during test: {test_name}")
    
    def end_suite(self, data, result):
        """
        Called when a test suite ends. Logs the session total.
        
        Args:
            data: Suite data
            result: Suite result object
        """
        session_total = self.cost_tracker.get_session_total()
        
        if session_total > 0:
            logger.info(
                f"\n{'='*60}\n"
                f"SESSION TOTAL API COST: ${session_total:.6f}\n"
                f"{'='*60}",
                html=True
            )

