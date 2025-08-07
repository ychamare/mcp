"""Prompts for AWS IoT SiteWise MCP server."""

from .asset_hierarchy import asset_hierarchy_visualization_prompt
from .dashboard_setup import dashboard_setup_helper_prompt
from .data_exploration import data_exploration_helper_prompt
from .data_ingestion import data_ingestion_helper_prompt

__all__ = [
    'asset_hierarchy_visualization_prompt',
    'data_ingestion_helper_prompt',
    'dashboard_setup_helper_prompt',
    'data_exploration_helper_prompt',
]
