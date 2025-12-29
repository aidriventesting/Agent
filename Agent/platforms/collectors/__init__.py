"""
UI Collectors for mobile automation.

- AndroidCollector: Android XML page source parsing
- IOSCollector: iOS XML page source parsing (NotImplemented)
"""

from Agent.platforms.collectors.android_collector import AndroidCollector
from Agent.platforms.collectors.ios_collector import IOSCollector
from Agent.platforms.collectors.som_renderer import render_som, bbox_center

__all__ = [
    'AndroidCollector',
    'IOSCollector',
    'render_som',
    'bbox_center',
]
