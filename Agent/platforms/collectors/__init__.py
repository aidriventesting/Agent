"""
UI Collectors for web and mobile automation.

This module provides different strategies for collecting UI elements:
- JSQueryCollector: JavaScript-based querySelector approach (web)
- XMLCollector: XML page source parsing (mobile)

Use CollectorRegistry to switch between strategies.
"""

from Agent.platforms.collectors.base_collector import BaseUICollector
from Agent.platforms.collectors.collector_factory import CollectorRegistry
from Agent.platforms.collectors.js_query_collector import JSQueryCollector
from Agent.platforms.collectors.xml_collector import XMLCollector
from Agent.platforms.collectors.som_renderer import render_som, bbox_center

__all__ = [
    'BaseUICollector',
    'CollectorRegistry',
    'JSQueryCollector',
    'XMLCollector',
    'render_som',
    'bbox_center',
]

