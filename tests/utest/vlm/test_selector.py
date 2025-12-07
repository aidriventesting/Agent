import unittest
from unittest.mock import Mock, patch
from Agent.ai.vlm._selector import OmniParserElementSelector


class TestOmniParserElementSelector(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            'icon3': {
                'type': 'icon',
                'bbox': [0.41938668489456177, 0.17028668522834778, 0.5745916366577148, 0.2660691440105438],
                'interactivity': True,
                'content': 'YouTube '
            },
            'icon9': {
                'type': 'icon',
                'bbox': [0.23282678425312042, 0.17132169008255005, 0.38811373710632324, 0.26554766297340393],
                'interactivity': True,
                'content': 'Gmail '
            },
            'icon22': {
                'type': 'icon',
                'bbox': [0.05158957466483116, 0.639639139175415, 0.2134605348110199, 0.7337194681167603],
                'interactivity': True,
                'content': 'Chrome '
            }
        }
    
    @patch('Agent.ai.vlm._selector.UnifiedLLMFacade')
    def test_select_element_youtube(self, mock_llm_facade):
        mock_llm_instance = Mock()
        mock_llm_instance.send_ai_request_and_return_response.return_value = {
            "element_key": "icon3",
            "confidence": "high",
            "reason": "YouTube matches the content"
        }
        mock_llm_facade.return_value = mock_llm_instance
        
        selector = OmniParserElementSelector()
        result = selector.select_element(self.test_data, "YouTube")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['element_key'], 'icon3')
        self.assertIn('confidence', result)
        self.assertIn('reason', result)
        self.assertIn('element_data', result)
    
    @patch('Agent.ai.vlm._selector.UnifiedLLMFacade')
    def test_select_element_not_found(self, mock_llm_facade):
        mock_llm_instance = Mock()
        mock_llm_instance.send_ai_request_and_return_response.return_value = {
            "element_key": None,
            "confidence": "low",
            "reason": "No matching element"
        }
        mock_llm_facade.return_value = mock_llm_instance
        
        selector = OmniParserElementSelector()
        result = selector.select_element(self.test_data, "NonExistent")
        
        self.assertIsNone(result)
    
    @patch('Agent.ai.vlm._selector.UnifiedLLMFacade')
    def test_select_element_invalid_key(self, mock_llm_facade):
        mock_llm_instance = Mock()
        mock_llm_instance.send_ai_request_and_return_response.return_value = {
            "element_key": "icon999",
            "confidence": "high",
            "reason": "Invalid key"
        }
        mock_llm_facade.return_value = mock_llm_instance
        
        selector = OmniParserElementSelector()
        result = selector.select_element(self.test_data, "Something")
        
        self.assertIsNone(result)
    
    def test_format_elements(self):
        selector = OmniParserElementSelector()
        formatted = selector._format_elements(self.test_data)
        
        self.assertIn('icon3', formatted)
        self.assertIn('YouTube', formatted)
        self.assertIn('Gmail', formatted)
        self.assertIn('Chrome', formatted)


if __name__ == "__main__":
    unittest.main()

