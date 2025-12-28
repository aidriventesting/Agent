"""
UI Collectors for mobile automation.

This module provides strategies for collecting UI elements:
- XMLCollector: XML page source parsing (Android/iOS)
"""

from Agent.platforms.collectors.base_collector import BaseUICollector
from Agent.platforms.collectors.collector_factory import CollectorRegistry
from Agent.platforms.collectors.xml_collector import XMLCollector
from Agent.platforms.collectors.som_renderer import render_som, bbox_center

__all__ = [
    'BaseUICollector',
    'CollectorRegistry',
    'XMLCollector',
    'render_som',
    'bbox_center',
]
