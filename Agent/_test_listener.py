"""
Robot Framework Test Listener
Automatically logs API costs after each test execution.
"""
import json
import os
from datetime import datetime
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
        Called when a test suite ends. Writes cost data to JSON file.
        
        Args:
            data: Suite data
            result: Suite result object
        """
        session_total = self.cost_tracker.get_session_total()
        if session_total > 0:
            cost_summary = {
                'suite_name': result.name,
                'timestamp': datetime.now().isoformat(),
                'session_total': round(session_total, 6),
                'tests': {}
            }
            
            all_test_costs = self.cost_tracker.get_all_test_costs()
            for test_name, cost_data in all_test_costs.items():
                cost_summary['tests'][test_name] = {
                    'total': round(cost_data['total'], 6),
                    'input_cost': round(cost_data['input_cost'], 6),
                    'output_cost': round(cost_data['output_cost'], 6),
                    'calls': cost_data['calls'],
                    'models': sorted(list(cost_data.get('models', set())))
                }
            
            log_dir = 'log'
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            json_file = os.path.join(log_dir, f'api_costs_{timestamp}.json')
            
            with open(json_file, 'w') as f:
                json.dump(cost_summary, f, indent=2)
            
