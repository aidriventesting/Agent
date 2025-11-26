from Agent.tools.web.click_element import ClickElementTool
from Agent.tools.web.input_text import InputTextTool
from Agent.tools.web.scroll_down import ScrollDownTool
from Agent.tools.web.scroll_up import ScrollUpTool
from Agent.tools.web.scroll_to_element import ScrollToElementTool
from Agent.tools.web.select_option import SelectOptionTool
from Agent.tools.web.press_key import PressKeyTool
from Agent.tools.web.go_back import GoBackTool
from Agent.tools.web.hover import HoverTool
from Agent.tools.web.double_click import DoubleClickTool
from Agent.tools.web.clear_text import ClearTextTool
from Agent.tools.web.click_visual import ClickVisualElementTool
from Agent.tools.web.input_text_visual import InputTextVisualTool
from Agent.tools.web.hover_visual import HoverVisualTool
from Agent.tools.web.double_click_visual import DoubleClickVisualTool
from Agent.tools.web.select_option_visual import SelectOptionVisualTool
from Agent.tools.web.scroll_to_element_visual import ScrollToElementVisualTool
from Agent.tools.web.clear_text_visual import ClearTextVisualTool


WEB_TOOLS = [
    ClickElementTool,
    InputTextTool,
    ScrollDownTool,
    ScrollUpTool,
    ScrollToElementTool,
    SelectOptionTool,
    PressKeyTool,
    GoBackTool,
    HoverTool,
    DoubleClickTool,
    ClearTextTool,
    ClickVisualElementTool,
    InputTextVisualTool,
    HoverVisualTool,
    DoubleClickVisualTool,
    SelectOptionVisualTool,
    ScrollToElementVisualTool,
    ClearTextVisualTool,
]

__all__ = [
    "WEB_TOOLS",
    "ClickElementTool",
    "InputTextTool",
    "ScrollDownTool",
    "ScrollUpTool",
    "ScrollToElementTool",
    "SelectOptionTool",
    "PressKeyTool",
    "GoBackTool",
    "HoverTool",
    "DoubleClickTool",
    "ClearTextTool",
    "ClickVisualElementTool",
    "InputTextVisualTool",
    "HoverVisualTool",
    "DoubleClickVisualTool",
    "SelectOptionVisualTool",
    "ScrollToElementVisualTool",
    "ClearTextVisualTool",
]

