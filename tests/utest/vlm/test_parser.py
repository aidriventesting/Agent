import unittest
from Agent.ai.vlm._parser import OmniParserResultProcessor


class TestOmniParserResultProcessor(unittest.TestCase):
    def setUp(self):
        self.response_text = """
icon 0: {'type': 'text', 'bbox': [0.14722222089767456, 0.02478632517158985, 0.24074074625968933, 0.04059829190373421], 'interactivity': False, 'content': '22:37'}
icon 1: {'type': 'text', 'bbox': [0.19166666269302368, 0.11153846234083176, 0.7564814686775208, 0.1260683834552765], 'interactivity': False, 'content': 'Applications prevues pour vous'}
icon 2: {'type': 'text', 'bbox': [0.31203705072402954, 0.30811965465545654, 0.6898148059844971, 0.32606837153434753], 'interactivity': False, 'content': 'Toutes les applications.'}
icon 3: {'type': 'icon', 'bbox': [0.41938668489456177, 0.17028668522834778, 0.5745916366577148, 0.2660691440105438], 'interactivity': True, 'content': 'YouTube '}
icon 4: {'type': 'icon', 'bbox': [0.6046537756919861, 0.3621394634246826, 0.7612757086753845, 0.45402267575263977], 'interactivity': True, 'content': 'Astuces .... '}
icon 5: {'type': 'icon', 'bbox': [0.4223991930484772, 0.7786725759506226, 0.5733458995819092, 0.872641921043396], 'interactivity': True, 'content': 'Firefox '}
icon 9: {'type': 'icon', 'bbox': [0.23282678425312042, 0.17132169008255005, 0.38811373710632324, 0.26554766297340393], 'interactivity': True, 'content': 'Gmail '}
icon 22: {'type': 'icon', 'bbox': [0.05158957466483116, 0.639639139175415, 0.2134605348110199, 0.7337194681167603], 'interactivity': True, 'content': 'Chrome '}
"""
        self.image_temp_path = "/tmp/gradio/test_image.webp"
    
    def test_parse_response(self):
        result = OmniParserResultProcessor(
            response_text=self.response_text, 
            image_temp_path=self.image_temp_path
        )
        elements = result.get_parsed_ui_elements(element_type="interactive")
        
        self.assertIsInstance(elements, dict)
        self.assertGreater(len(elements), 0)
        
    def test_filter_by_type_interactive(self):
        result = OmniParserResultProcessor(
            response_text=self.response_text,
            image_temp_path=self.image_temp_path
        )
        elements = result.get_parsed_ui_elements(element_type="interactive")
        
        for key, data in elements.items():
            self.assertTrue(data['interactivity'])
    
    def test_filter_by_type_icon(self):
        result = OmniParserResultProcessor(
            response_text=self.response_text,
            image_temp_path=self.image_temp_path
        )
        elements = result.get_parsed_ui_elements(element_type="icon")
        
        for key, data in elements.items():
            self.assertEqual(data['type'], 'icon')
    
    def test_filter_by_type_text(self):
        result = OmniParserResultProcessor(
            response_text=self.response_text,
            image_temp_path=self.image_temp_path
        )
        elements = result.get_parsed_ui_elements(element_type="text")
        
        for key, data in elements.items():
            self.assertEqual(data['type'], 'text')
    
    def test_filter_all(self):
        result = OmniParserResultProcessor(
            response_text=self.response_text,
            image_temp_path=self.image_temp_path
        )
        elements = result.get_parsed_ui_elements(element_type="all")
        
        self.assertGreater(len(elements), 5)
    
    def test_element_key_format(self):
        result = OmniParserResultProcessor(
            response_text=self.response_text,
            image_temp_path=self.image_temp_path
        )
        elements = result.get_parsed_ui_elements(element_type="all")
        
        for key in elements.keys():
            self.assertNotIn(' ', key)
            self.assertTrue(key.startswith('icon'))


if __name__ == "__main__":
    unittest.main()

