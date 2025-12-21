"""
Unit tests for cost tracking functionality
"""
import unittest
from unittest.mock import Mock, MagicMock, patch
from Agent.utilities._costtracker import CostTracker
from Agent.ai.llm._openaiclient import OpenAIClient


class TestCostTracker(unittest.TestCase):
    """Test cases for CostTracker singleton"""
    
    def setUp(self):
        """Reset cost tracker before each test"""
        tracker = CostTracker()
        tracker.reset()
    
    def test_singleton_pattern(self):
        """Test that CostTracker follows singleton pattern"""
        tracker1 = CostTracker()
        tracker2 = CostTracker()
        self.assertIs(tracker1, tracker2)
    
    def test_start_test(self):
        """Test starting a new test tracking"""
        tracker = CostTracker()
        tracker.start_test("test_example")
        cost_data = tracker.get_test_cost()
        
        self.assertEqual(cost_data['total'], 0.0)
        self.assertEqual(cost_data['calls'], 0)
    
    def test_add_cost(self):
        """Test adding cost for API calls"""
        tracker = CostTracker()
        tracker.start_test("test_example")
        
        # Simulate an API call cost
        tracker.add_cost(input_cost=0.001, output_cost=0.002, model="gpt-4o-mini")
        
        cost_data = tracker.get_test_cost()
        self.assertEqual(cost_data['total'], 0.003)
        self.assertEqual(cost_data['input_cost'], 0.001)
        self.assertEqual(cost_data['output_cost'], 0.002)
        self.assertEqual(cost_data['calls'], 1)
    
    def test_multiple_calls(self):
        """Test tracking multiple API calls"""
        tracker = CostTracker()
        tracker.start_test("test_example")
        
        tracker.add_cost(input_cost=0.001, output_cost=0.002, model="gpt-4o-mini")
        tracker.add_cost(input_cost=0.003, output_cost=0.004, model="gpt-4o-mini")
        
        cost_data = tracker.get_test_cost()
        self.assertEqual(cost_data['total'], 0.010)
        self.assertEqual(cost_data['input_cost'], 0.004)
        self.assertEqual(cost_data['output_cost'], 0.006)
        self.assertEqual(cost_data['calls'], 2)
    
    def test_session_total(self):
        """Test tracking session total across multiple tests"""
        tracker = CostTracker()
        
        # First test
        tracker.start_test("test_1")
        tracker.add_cost(input_cost=0.001, output_cost=0.002, model="gpt-4o-mini")
        tracker.end_test()
        
        # Second test
        tracker.start_test("test_2")
        tracker.add_cost(input_cost=0.003, output_cost=0.004, model="gpt-4o-mini")
        tracker.end_test()
        
        session_total = tracker.get_session_total()
        self.assertEqual(session_total, 0.010)
    
    def test_reset(self):
        """Test resetting the cost tracker"""
        tracker = CostTracker()
        tracker.start_test("test_example")
        tracker.add_cost(input_cost=0.001, output_cost=0.002, model="gpt-4o-mini")
        
        tracker.reset()
        
        self.assertEqual(tracker.get_session_total(), 0.0)


class TestOpenAIClientCostCalculation(unittest.TestCase):
    """Test cases for OpenAI client cost calculation"""
    
    @patch('Agent.ai.llm._openaiclient.OpenAI')
    @patch('Agent.ai.llm._openaiclient.Config')
    def test_calculate_cost_gpt4o_mini(self, mock_config, mock_openai):
        """Test cost calculation for GPT-4o-mini"""
        # Mock the config
        mock_config_instance = Mock()
        mock_config_instance.OPENAI_API_KEY = "test_key"
        mock_config.return_value = mock_config_instance
        
        # Create client
        client = OpenAIClient(api_key="test_key", model="gpt-4o-mini")
        
        # Test cost calculation
        # According to llm_models.json:
        # gpt-4o-mini: input=$0.00015, output=$0.0006 per 1M tokens
        cost_data = client._calculate_cost(
            model="gpt-4o-mini",
            prompt_tokens=1000,
            completion_tokens=500
        )
        
        expected_input_cost = (1000 / 1_000_000) * 0.00015  # $0.00000015
        expected_output_cost = (500 / 1_000_000) * 0.0006   # $0.0000003
        expected_total = expected_input_cost + expected_output_cost
        
        self.assertAlmostEqual(cost_data['input_cost'], expected_input_cost, places=10)
        self.assertAlmostEqual(cost_data['output_cost'], expected_output_cost, places=10)
        self.assertAlmostEqual(cost_data['total_cost'], expected_total, places=10)
    
    @patch('Agent.ai.llm._openaiclient.OpenAI')
    @patch('Agent.ai.llm._openaiclient.Config')
    def test_calculate_cost_gpt4o(self, mock_config, mock_openai):
        """Test cost calculation for GPT-4o"""
        # Mock the config
        mock_config_instance = Mock()
        mock_config_instance.OPENAI_API_KEY = "test_key"
        mock_config.return_value = mock_config_instance
        
        # Create client
        client = OpenAIClient(api_key="test_key", model="gpt-4o")
        
        # Test cost calculation
        # According to llm_models.json:
        # gpt-4o: input=$0.005, output=$0.015 per 1M tokens
        cost_data = client._calculate_cost(
            model="gpt-4o",
            prompt_tokens=10000,
            completion_tokens=5000
        )
        
        expected_input_cost = (10000 / 1_000_000) * 0.005   # $0.00005
        expected_output_cost = (5000 / 1_000_000) * 0.015   # $0.000075
        expected_total = expected_input_cost + expected_output_cost
        
        self.assertAlmostEqual(cost_data['input_cost'], expected_input_cost, places=10)
        self.assertAlmostEqual(cost_data['output_cost'], expected_output_cost, places=10)
        self.assertAlmostEqual(cost_data['total_cost'], expected_total, places=10)
    
    @patch('Agent.ai.llm._openaiclient.OpenAI')
    @patch('Agent.ai.llm._openaiclient.Config')
    def test_calculate_cost_unknown_model(self, mock_config, mock_openai):
        """Test cost calculation for unknown model returns zero cost"""
        # Mock the config
        mock_config_instance = Mock()
        mock_config_instance.OPENAI_API_KEY = "test_key"
        mock_config.return_value = mock_config_instance
        
        # Create client
        client = OpenAIClient(api_key="test_key", model="gpt-4o-mini")
        
        # Test cost calculation with unknown model
        cost_data = client._calculate_cost(
            model="unknown-model",
            prompt_tokens=1000,
            completion_tokens=500
        )
        
        self.assertEqual(cost_data['input_cost'], 0.0)
        self.assertEqual(cost_data['output_cost'], 0.0)
        self.assertEqual(cost_data['total_cost'], 0.0)


if __name__ == '__main__':
    unittest.main()


