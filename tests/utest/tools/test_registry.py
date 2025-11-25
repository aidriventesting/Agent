"""Tests for ToolRegistry mode filtering logic."""
import unittest
from Agent.tools.registry import ToolRegistry
from Agent.tools.mobile import MOBILE_TOOLS


class TestToolRegistryModes(unittest.TestCase):
    """Test ToolRegistry filtering based on click_mode (xml/visual/hybrid)."""
    
    def setUp(self):
        """Initialize registry with all mobile tools."""
        self.registry = ToolRegistry()
        self.registry.clear()
        
        # Register all mobile tools
        for ToolClass in MOBILE_TOOLS:
            self.registry.register(ToolClass())
    
    def test_xml_mode_excludes_visual_only_tools(self):
        """XML mode should exclude click_visual_element, keep tap_element and input_text."""
        tools = self.registry.get_tools_for_mode("mobile", "xml")
        tool_names = [tool.name for tool in tools]
        
        # tap_element should be available (works_on_locator=True)
        self.assertIn("tap_element", tool_names, 
                     "tap_element should be available in XML mode")
        
        # click_visual_element should be EXCLUDED (works_on_visual=True only)
        self.assertNotIn("click_visual_element", tool_names,
                        "click_visual_element should be excluded in XML mode")
        
        # input_text should be available (works_on_locator=True)
        self.assertIn("input_text", tool_names,
                     "input_text should be available in XML mode")
        
        print(f"✅ XML mode: {len(tool_names)} tools available")
        print(f"   Tools: {', '.join(sorted(tool_names))}")
    
    def test_visual_mode_excludes_tools_with_equivalents(self):
        """Visual mode should exclude tap_element (has equivalent), but KEEP input_text (no equivalent)."""
        tools = self.registry.get_tools_for_mode("mobile", "visual")
        tool_names = [tool.name for tool in tools]
        
        # tap_element should be EXCLUDED (has_visual_equivalent=True)
        self.assertNotIn("tap_element", tool_names,
                        "tap_element should be excluded in Visual mode (has visual equivalent)")
        
        # click_visual_element should be available
        self.assertIn("click_visual_element", tool_names,
                     "click_visual_element should be available in Visual mode")
        
        # input_text should be KEPT (has_visual_equivalent=False)
        self.assertIn("input_text", tool_names,
                     "input_text should be KEPT in Visual mode (no visual equivalent)")
        
        # scroll/swipe should be available
        self.assertIn("scroll_down", tool_names,
                     "scroll_down should be available in Visual mode")
        
        print(f"✅ Visual mode: {len(tool_names)} tools available")
        print(f"   Tools: {', '.join(sorted(tool_names))}")
    
    def test_hybrid_mode_includes_all_tools(self):
        """Hybrid mode should include ALL tools, letting AI choose between equivalents."""
        tools = self.registry.get_tools_for_mode("mobile", "hybrid")
        tool_names = [tool.name for tool in tools]
        
        # Both click variants should be available
        self.assertIn("tap_element", tool_names,
                     "tap_element should be available in Hybrid mode")
        self.assertIn("click_visual_element", tool_names,
                     "click_visual_element should be available in Hybrid mode")
        
        # input_text should be available
        self.assertIn("input_text", tool_names,
                     "input_text should be available in Hybrid mode")
        
        # All navigation tools should be available
        self.assertIn("scroll_down", tool_names)
        self.assertIn("go_back", tool_names)
        
        print(f"✅ Hybrid mode: {len(tool_names)} tools available")
        print(f"   Tools: {', '.join(sorted(tool_names))}")
    
    def test_tool_count_comparison(self):
        """Hybrid should have more tools than XML or Visual alone."""
        xml_tools = self.registry.get_tools_for_mode("mobile", "xml")
        visual_tools = self.registry.get_tools_for_mode("mobile", "visual")
        hybrid_tools = self.registry.get_tools_for_mode("mobile", "hybrid")
        
        xml_count = len(xml_tools)
        visual_count = len(visual_tools)
        hybrid_count = len(hybrid_tools)
        
        # Hybrid should have more tools
        self.assertGreater(hybrid_count, xml_count,
                          "Hybrid mode should have more tools than XML mode")
        self.assertGreater(hybrid_count, visual_count,
                          "Hybrid mode should have more tools than Visual mode")
        
        print(f"📊 Tool counts:")
        print(f"   XML mode: {xml_count} tools")
        print(f"   Visual mode: {visual_count} tools")
        print(f"   Hybrid mode: {hybrid_count} tools")


if __name__ == '__main__':
    unittest.main()

