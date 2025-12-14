"""
UI Collectors for web automation.

This module provides different strategies for collecting UI elements:
- JSQueryCollector: JavaScript-based querySelector approach (default)

Use CollectorRegistry to switch between strategies.
"""

from Agent.platforms.collectors.base_collector import BaseUICollector
from Agent.platforms.collectors.collector_factory import CollectorRegistry
from Agent.platforms.collectors.som_renderer import render_som, bbox_center

__all__ = ['BaseUICollector', 'CollectorRegistry', 'render_som', 'bbox_center']

