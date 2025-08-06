import argparse
import os
import signal
import sys

from anyio import create_task_group, open_signal_receiver, run
from anyio.abc import CancelScope
from mcp.server.fastmcp import FastMCP

# Import IoT SiteWise prompts
from awslabs.aws_iot_sitewise_mcp_server.prompts.asset_hierarchy import (
    asset_hierarchy_visualization_prompt,
)

# Import existing prompts
from awslabs.aws_iot_sitewise_mcp_server.prompts.dashboard_setup import (
    dashboard_setup_helper_prompt,
)
from awslabs.aws_iot_sitewise_mcp_server.prompts.data_exploration import (
    data_exploration_helper_prompt,
)
from awslabs.aws_iot_sitewise_mcp_server.prompts.data_ingestion import data_ingestion_helper_prompt
from awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_access import (
    create_access_policy_tool,
    delete_access_policy_tool,
    describe_access_policy_tool,
    describe_default_encryption_configuration_tool,
    describe_logging_options_tool,
    describe_storage_configuration_tool,
    list_access_policies_tool,
    put_default_encryption_configuration_tool,
    put_logging_options_tool,
    put_storage_configuration_tool,
    update_access_policy_tool,
)
from awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_asset_models import (
    create_asset_model_composite_model_tool,
    create_asset_model_tool,
    delete_asset_model_tool,
    describe_asset_model_tool,
    list_asset_model_properties_tool,
    list_asset_models_tool,
    update_asset_model_tool,
)

# Import IoT SiteWise tools
from awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_assets import (
    associate_assets_tool,
    create_asset_tool,
    delete_asset_tool,
    describe_asset_tool,
    disassociate_assets_tool,
    list_assets_tool,
    list_associated_assets_tool,
    update_asset_tool,
)
from awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_data import (
    batch_get_asset_property_aggregates_tool,
    batch_get_asset_property_value_history_tool,
    batch_get_asset_property_value_tool,
    batch_put_asset_property_value_tool,
    describe_execution_tool,
    execute_query_tool,
    get_asset_property_aggregates_tool,
    get_asset_property_value_history_tool,
    get_asset_property_value_tool,
    get_interpolated_asset_property_values_tool,
    list_executions_tool,
)
from awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_gateways import (
    associate_time_series_to_asset_property_tool,
    create_gateway_tool,
    delete_gateway_tool,
    delete_time_series_tool,
    describe_gateway_capability_configuration_tool,
    describe_gateway_tool,
    describe_time_series_tool,
    disassociate_time_series_from_asset_property_tool,
    list_gateways_tool,
    list_time_series_tool,
    update_gateway_capability_configuration_tool,
    update_gateway_tool,
)
from awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_portals import (
    create_dashboard_tool,
    create_portal_tool,
    create_project_tool,
    delete_dashboard_tool,
    delete_portal_tool,
    delete_project_tool,
    describe_dashboard_tool,
    describe_portal_tool,
    describe_project_tool,
    list_dashboards_tool,
    list_portals_tool,
    list_projects_tool,
    update_dashboard_tool,
    update_portal_tool,
    update_project_tool,
)
from awslabs.aws_iot_sitewise_mcp_server.utils import get_package_version


async def signal_handler(scope: CancelScope):
    """Handle SIGINT and SIGTERM signals asynchronously.

    The anyio.open_signal_receiver returns an async generator that yields
    signal numbers whenever a specified signal is received. The async for
    loop waits for signals and processes them as they arrive.
    """
    with open_signal_receiver(signal.SIGINT, signal.SIGTERM) as signals:
        async for _ in signals:  # Shutting down regardless of the signal type
            print("Shutting down MCP server...")
            # Force immediate exit since MCP blocks on stdio.
            # You can also use scope.cancel(), but it means after Ctrl+C, you need to press another
            # 'Enter' to unblock the stdio.
            os._exit(0)


async def run_server():
    """Run the MCP server with signal handling."""
    mcp = FastMCP(
        name="sitewise",
        instructions="A comprehensive AWS IoT SiteWise MCP server providing full functionality for industrial IoT asset management, data ingestion, monitoring, and analytics.",
    )
    
    # Set the server version
    mcp._mcp_server.version = get_package_version()

    # IoT SiteWise Asset Management Tools
    asset_tools = [
        create_asset_tool,
        describe_asset_tool,
        list_assets_tool,
        update_asset_tool,
        delete_asset_tool,
        associate_assets_tool,
        disassociate_assets_tool,
        list_associated_assets_tool,
    ]

    # IoT SiteWise Asset Model Management Tools
    asset_model_tools = [
        create_asset_model_tool,
        describe_asset_model_tool,
        list_asset_models_tool,
        update_asset_model_tool,
        delete_asset_model_tool,
        list_asset_model_properties_tool,
        create_asset_model_composite_model_tool,
    ]

    # IoT SiteWise Data Ingestion and Retrieval Tools
    data_tools = [
        batch_put_asset_property_value_tool,
        get_asset_property_value_tool,
        get_asset_property_value_history_tool,
        get_asset_property_aggregates_tool,
        get_interpolated_asset_property_values_tool,
        batch_get_asset_property_value_tool,
        batch_get_asset_property_value_history_tool,
        batch_get_asset_property_aggregates_tool,
        execute_query_tool,
        list_executions_tool,
        describe_execution_tool,
    ]

    # IoT SiteWise Gateway and Time Series Management Tools
    gateway_tools = [
        create_gateway_tool,
        describe_gateway_tool,
        list_gateways_tool,
        update_gateway_tool,
        delete_gateway_tool,
        describe_gateway_capability_configuration_tool,
        update_gateway_capability_configuration_tool,
        list_time_series_tool,
        describe_time_series_tool,
        associate_time_series_to_asset_property_tool,
        disassociate_time_series_from_asset_property_tool,
        delete_time_series_tool,
    ]

    # IoT SiteWise Portal, Project, and Dashboard Management Tools
    portal_tools = [
        create_portal_tool,
        describe_portal_tool,
        list_portals_tool,
        update_portal_tool,
        delete_portal_tool,
        create_project_tool,
        describe_project_tool,
        list_projects_tool,
        update_project_tool,
        delete_project_tool,
        create_dashboard_tool,
        describe_dashboard_tool,
        list_dashboards_tool,
        update_dashboard_tool,
        delete_dashboard_tool,
    ]

    # IoT SiteWise Access Control and Configuration Tools
    access_tools = [
        create_access_policy_tool,
        describe_access_policy_tool,
        list_access_policies_tool,
        update_access_policy_tool,
        delete_access_policy_tool,
        describe_default_encryption_configuration_tool,
        put_default_encryption_configuration_tool,
        describe_logging_options_tool,
        put_logging_options_tool,
        describe_storage_configuration_tool,
        put_storage_configuration_tool,
    ]

    # Combine all tools
    all_tools = (
        asset_tools + asset_model_tools + data_tools + gateway_tools + portal_tools + access_tools
    )

    # Add all tools to the MCP server
    for tool in all_tools:
        mcp.add_tool(tool.fn, tool.name, tool.description, tool.annotations)

    # Add prompts
    prompts = [
        asset_hierarchy_visualization_prompt,
        data_ingestion_helper_prompt,
        dashboard_setup_helper_prompt,
        data_exploration_helper_prompt,
    ]

    for prompt in prompts:
        mcp.add_prompt(prompt)

    async with create_task_group() as tg:
        tg.start_soon(signal_handler, tg.cancel_scope)
        # proceed with starting the actual application logic
        await mcp.run_stdio_async()


def main():
    """Run the MCP server with CLI argument support.
    
    This function initializes and runs the AWS IoT SiteWise MCP server, which provides
    programmatic access to manage AWS IoT SiteWise resources through the Model Context Protocol.
    """
    parser = argparse.ArgumentParser(
        description='An AWS Labs Model Context Protocol (MCP) server for AWS IoT SiteWise'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {get_package_version()}',
        help='Show the version number and exit'
    )
    
    args = parser.parse_args()
    
    # Run the async server
    run(run_server)


if __name__ == '__main__':
    main()
