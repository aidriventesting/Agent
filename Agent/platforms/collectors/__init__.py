"""
UI Collectors for mobile automation.

- AndroidCollector: Android XML page source parsing
- IOSCollector: iOS XML page source parsing (NotImplemented)
"""

from Agent.platforms.collectors.android_collector import AndroidCollector
from Agent.platforms.collectors.ios_collector import IOSCollector
from Agent.platforms.grounding.som.annotator import annotate_screenshot, bbox_center

__all__ = [
    'AndroidCollector',
    'IOSCollector',
    'annotate_screenshot',
    'bbox_center',
]
