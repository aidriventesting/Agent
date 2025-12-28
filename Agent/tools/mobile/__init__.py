from Agent.tools.mobile.click_element import ClickElementTool
from Agent.tools.mobile.input_text import InputTextTool
from Agent.tools.mobile.scroll_down import ScrollDownTool
from Agent.tools.mobile.long_press import LongPressTool
from Agent.tools.mobile.swipe_left import SwipeLeftTool
from Agent.tools.mobile.swipe_right import SwipeRightTool
from Agent.tools.mobile.swipe_up import SwipeUpTool
from Agent.tools.mobile.hide_keyboard import HideKeyboardTool
from Agent.tools.mobile.go_back import GoBackTool


MOBILE_TOOLS = [
    ClickElementTool,
    InputTextTool,
    ScrollDownTool,
    LongPressTool,
    SwipeLeftTool,
    SwipeRightTool,
    SwipeUpTool,
    HideKeyboardTool,
    GoBackTool,
]

__all__ = [
    "MOBILE_TOOLS",
    "ClickElementTool",
    "InputTextTool",
    "ScrollDownTool",
    "LongPressTool",
    "SwipeLeftTool",
    "SwipeRightTool",
    "SwipeUpTool",
    "HideKeyboardTool",
    "GoBackTool",
]
