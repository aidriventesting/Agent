import unittest
from Agent.tools.registry import ToolRegistry
from Agent.tools.mobile import MOBILE_TOOLS


class TestToolRegistryModes(unittest.TestCase):
    
    def setUp(self):
        self.registry = ToolRegistry()
        self.registry.clear()
        for ToolClass in MOBILE_TOOLS:
            self.registry.register(ToolClass())
    
    def test_xml_mode_excludes_visual_only_tools(self):
        tools = self.registry.get_tools_for_mode("mobile", "xml")
        tool_names = [tool.name for tool in tools]
        
        self.assertIn("tap_element", tool_names)
        self.assertNotIn("click_visual_element", tool_names)
        self.assertIn("input_text", tool_names)
    
    def test_visual_mode_excludes_tools_with_equivalents(self):
        tools = self.registry.get_tools_for_mode("mobile", "visual")
        tool_names = [tool.name for tool in tools]
        
        self.assertNotIn("tap_element", tool_names)
        self.assertIn("click_visual_element", tool_names)
        self.assertIn("input_text", tool_names)
        self.assertIn("scroll_down", tool_names)
    
    def test_xml_has_more_locator_tools(self):
        xml_tools = self.registry.get_tools_for_mode("mobile", "xml")
        visual_tools = self.registry.get_tools_for_mode("mobile", "visual")
        
        xml_locator_tools = [t for t in xml_tools if t.works_on_locator]
        visual_locator_tools = [t for t in visual_tools if t.works_on_locator]
        
        self.assertGreaterEqual(len(xml_locator_tools), len(visual_locator_tools))


if __name__ == '__main__':
    unittest.main()
