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
]

