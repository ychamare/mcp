# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""AWS IoT SiteWise MCP Server implementation."""

import os
import sys
from typing import Any

from fastmcp import FastMCP
from loguru import logger
from pydantic import Field

from .consts import TOOL_SAFETY_DESCRIPTIONS
from .iotsitewise import IoTSiteWiseService
from .models import (
    # Read-only models
    ListAssetModelsParams,
    DescribeAssetModelParams,
    ListAssetsParams,
    DescribeAssetParams,
    GetAssetPropertyValueParams,
    GetAssetPropertyValueHistoryParams,
    GetAssetPropertyAggregatesParams,
    ListAssociatedAssetsParams,
    BatchGetAssetPropertyValueParams,
    BatchGetAssetPropertyValueHistoryParams,
    BatchGetAssetPropertyAggregatesParams,
    GetInterpolatedAssetPropertyValuesParams,
    ListGatewaysParams,
    DescribeGatewayParams,
    DescribeGatewayCapabilityConfigurationParams,
    ListPortalsParams,
    ListDashboardsParams,
    ListProjectsParams,
    ListTimeSeriesParams,
    DescribeTimeSeriesParams,
    ListAccessPoliciesParams,
    ListTagsForResourceParams,
    # Write models
    CreateAssetParams,
    UpdateAssetParams,
    DeleteAssetParams,
    AssociateAssetsParams,
    DisassociateAssetsParams,
    CreateAssetModelParams,
    UpdateAssetModelParams,
    DeleteAssetModelParams,
    BatchPutAssetPropertyValueParams,
    CreateGatewayParams,
    UpdateGatewayParams,
    DeleteGatewayParams,
    UpdateGatewayCapabilityConfigurationParams,
    CreatePortalParams,
    UpdatePortalParams,
    DeletePortalParams,
    CreateProjectParams,
    CreateDashboardParams,
    UpdateDashboardParams,
    DeleteDashboardParams,
    CreateAccessPolicyParams,
    UpdateAccessPolicyParams,
    DeleteAccessPolicyParams,
    AssociateTimeSeriesToAssetPropertyParams,
    DisassociateTimeSeriesFromAssetPropertyParams,
    TagResourceParams,
    UntagResourceParams,
)

# Configure logging
logger.remove()
logger.add(sys.stderr, level=os.getenv('FASTMCP_LOG_LEVEL', 'WARNING'))

# Initialize FastMCP server
mcp = FastMCP(
    'awslabs-aws-iot-sitewise-mcp-server',
    instructions="""
# AWS IoT SiteWise MCP Server

This MCP server provides comprehensive access to AWS IoT SiteWise APIs for industrial IoT data management.

## Available Tools

The server provides 49 tools categorized by safety level:

### 📖 Read-Only Tools (22 tools)
Safe operations that only retrieve data:
- Asset and Asset Model queries
- Property value and history retrieval
- Batch property operations
- Gateway, Portal, and Project listing
- Time series and access policy management

### ⚠️ Write Operations (21 tools)
Modify existing resources or create new ones:
- Asset and Asset Model management
- Property value ingestion
- Gateway and Portal configuration
- Dashboard and Project creation
- Time series associations

### 🚨 Destructive Operations (6 tools)
Permanently delete resources (use with extreme caution):
- Delete assets, asset models, gateways
- Delete portals, dashboards, access policies

## Safety Features

- All write operations are clearly marked with safety indicators
- Destructive operations require explicit confirmation
- Comprehensive error handling and validation
- Detailed logging for all operations

## Authentication

Configure AWS credentials using one of these methods:
- AWS CLI: `aws configure`
- Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- IAM roles (for EC2/Lambda execution)
- AWS profiles: Set `AWS_PROFILE` environment variable

## Region Configuration

Set the AWS region using the `AWS_REGION` environment variable (default: us-west-2).

## Usage Best Practices

1. Start with read-only tools to explore your IoT SiteWise resources
2. Use batch operations for efficient data retrieval
3. Always validate asset and property IDs before write operations
4. Be extremely cautious with destructive operations
5. Monitor logs for operation status and errors

## Example Workflows

### Basic Asset Discovery
1. `list_asset_models` - Get available asset models
2. `describe_asset_model` - Get details about a specific model
3. `list_assets` - Find assets based on the model
4. `describe_asset` - Get asset details and properties

### Property Data Retrieval
1. `get_asset_property_value` - Get current property value
2. `get_asset_property_value_history` - Get historical data
3. `get_asset_property_aggregates` - Get aggregated metrics
4. `batch_get_asset_property_value` - Efficient bulk retrieval
""",
    dependencies=[
        'pydantic',
        'boto3',
        'loguru',
    ],
)

# Initialize IoT SiteWise service
try:
    iot_sitewise = IoTSiteWiseService()
    logger.info('IoT SiteWise service initialized successfully')
except Exception as e:
    logger.error(f'Failed to initialize IoT SiteWise service: {str(e)}')
    raise


# Read-only tools (22 tools)
@mcp.tool(name='list_asset_models')
async def list_asset_models_tool(
    max_results: int = Field(None, ge=1, le=250, description='Maximum number of results to return'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """List all asset models in IoT SiteWise.
    
    This tool retrieves a list of all asset models available in your AWS IoT SiteWise account.
    Asset models define the structure and properties for industrial assets.
    """
    logger.info('Executing list_asset_models')
    return await iot_sitewise.list_asset_models(max_results=max_results, next_token=next_token)


@mcp.tool(name='describe_asset_model')
async def describe_asset_model_tool(
    asset_model_id: str = Field(..., description='The ID of the asset model'),
) -> str:
    """Get detailed information about a specific asset model.
    
    This tool provides comprehensive details about an asset model including its properties,
    hierarchies, and composite models.
    """
    logger.info(f'Executing describe_asset_model for model: {asset_model_id}')
    return await iot_sitewise.describe_asset_model(asset_model_id=asset_model_id)


@mcp.tool(name='list_assets')
async def list_assets_tool(
    asset_model_id: str = Field(None, description='Filter assets by asset model ID'),
    max_results: int = Field(None, ge=1, le=250, description='Maximum number of results to return'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """List assets, optionally filtered by asset model.
    
    This tool retrieves a list of assets in your AWS IoT SiteWise account.
    You can filter the results by asset model ID to find specific types of assets.
    """
    logger.info(f'Executing list_assets with model filter: {asset_model_id}')
    return await iot_sitewise.list_assets(
        asset_model_id=asset_model_id,
        max_results=max_results,
        next_token=next_token
    )


@mcp.tool(name='describe_asset')
async def describe_asset_tool(
    asset_id: str = Field(..., description='The ID of the asset'),
) -> str:
    """Get detailed information about a specific asset.
    
    This tool provides comprehensive details about an asset including its properties,
    hierarchies, and current status.
    """
    logger.info(f'Executing describe_asset for asset: {asset_id}')
    return await iot_sitewise.describe_asset(asset_id=asset_id)


@mcp.tool(name='get_asset_property_value')
async def get_asset_property_value_tool(
    asset_id: str = Field(..., description='The ID of the asset'),
    property_id: str = Field(None, description='The ID of the property'),
    property_alias: str = Field(None, description='The alias of the property (alternative to propertyId)'),
) -> str:
    """Get the current value of an asset property.
    
    This tool retrieves the most recent value for a specified asset property.
    You can specify the property by either its ID or alias.
    """
    logger.info(f'Executing get_asset_property_value for asset: {asset_id}, property: {property_id or property_alias}')
    return await iot_sitewise.get_asset_property_value(
        asset_id=asset_id,
        property_id=property_id,
        property_alias=property_alias
    )


@mcp.tool(name='get_asset_property_value_history')
async def get_asset_property_value_history_tool(
    asset_id: str = Field(..., description='The ID of the asset'),
    property_id: str = Field(None, description='The ID of the property'),
    property_alias: str = Field(None, description='The alias of the property'),
    start_date: str = Field(None, description='Start date for the query (ISO 8601 format)'),
    end_date: str = Field(None, description='End date for the query (ISO 8601 format)'),
    qualities: list = Field(None, description='Filter by data quality (GOOD, BAD, UNCERTAIN)'),
    time_ordering: str = Field(None, description='Order of returned data points (ASCENDING, DESCENDING)'),
    max_results: int = Field(None, ge=1, le=4000, description='Maximum number of results to return'),
) -> str:
    """Get historical values for an asset property.
    
    This tool retrieves historical data points for a specified asset property within a time range.
    You can filter by data quality and control the ordering of results.
    """
    logger.info(f'Executing get_asset_property_value_history for asset: {asset_id}, property: {property_id or property_alias}')
    kwargs = {}
    if start_date:
        kwargs['startDate'] = start_date
    if end_date:
        kwargs['endDate'] = end_date
    if qualities:
        kwargs['qualities'] = qualities
    if time_ordering:
        kwargs['timeOrdering'] = time_ordering
    if max_results:
        kwargs['maxResults'] = max_results
    
    return await iot_sitewise.get_asset_property_value_history(
        asset_id=asset_id,
        property_id=property_id,
        property_alias=property_alias,
        **kwargs
    )


@mcp.tool(name='get_asset_property_aggregates')
async def get_asset_property_aggregates_tool(
    asset_id: str = Field(..., description='The ID of the asset'),
    aggregate_types: list = Field(..., description='Types of aggregates (AVERAGE, COUNT, MAXIMUM, MINIMUM, SUM, STANDARD_DEVIATION)'),
    resolution: str = Field(..., description='Time interval for aggregation (e.g., 1m, 5m, 1h, 1d)'),
    start_date: str = Field(..., description='Start date for the query (ISO 8601 format)'),
    end_date: str = Field(..., description='End date for the query (ISO 8601 format)'),
    property_id: str = Field(None, description='The ID of the property'),
    property_alias: str = Field(None, description='The alias of the property'),
    qualities: list = Field(None, description='Filter by data quality'),
) -> str:
    """Get aggregated values for an asset property.
    
    This tool calculates aggregated statistics for an asset property over specified time intervals.
    Supports various aggregate types including average, count, maximum, minimum, sum, and standard deviation.
    """
    logger.info(f'Executing get_asset_property_aggregates for asset: {asset_id}, property: {property_id or property_alias}')
    kwargs = {
        'aggregateTypes': aggregate_types,
        'resolution': resolution,
        'startDate': start_date,
        'endDate': end_date,
    }
    if qualities:
        kwargs['qualities'] = qualities
    
    return await iot_sitewise.get_asset_property_aggregates(
        asset_id=asset_id,
        property_id=property_id,
        property_alias=property_alias,
        **kwargs
    )


@mcp.tool(name='list_associated_assets')
async def list_associated_assets_tool(
    asset_id: str = Field(..., description='The ID of the parent asset'),
    hierarchy_id: str = Field(None, description='The ID of the hierarchy to traverse'),
    traversal_direction: str = Field(None, description='Direction to traverse the hierarchy (PARENT, CHILD)'),
    max_results: int = Field(None, ge=1, le=250, description='Maximum number of results to return'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """List assets associated with a parent asset.
    
    This tool retrieves assets that are associated with a specified parent asset through
    hierarchical relationships defined in asset models.
    """
    logger.info(f'Executing list_associated_assets for asset: {asset_id}')
    kwargs = {}
    if hierarchy_id:
        kwargs['hierarchyId'] = hierarchy_id
    if traversal_direction:
        kwargs['traversalDirection'] = traversal_direction
    if max_results:
        kwargs['maxResults'] = max_results
    if next_token:
        kwargs['nextToken'] = next_token
    
    return await iot_sitewise.list_associated_assets(asset_id=asset_id, **kwargs)


@mcp.tool(name='batch_get_asset_property_value')
async def batch_get_asset_property_value_tool(
    entries: list = Field(..., max_length=128, description='List of property value requests with entryId, assetId, propertyId/propertyAlias'),
) -> str:
    """Get current values for multiple asset properties in a single request.
    
    This tool efficiently retrieves current values for multiple asset properties in a single API call.
    Each entry requires an entryId and either (assetId + propertyId) or propertyAlias.
    """
    logger.info(f'Executing batch_get_asset_property_value for {len(entries)} entries')
    return await iot_sitewise.batch_get_asset_property_value(entries=entries)


@mcp.tool(name='batch_get_asset_property_value_history')
async def batch_get_asset_property_value_history_tool(
    entries: list = Field(..., max_length=16, description='List of property history requests'),
    max_results: int = Field(None, ge=1, le=4000, description='Maximum number of results per entry'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """Get historical values for multiple asset properties in a single request.
    
    This tool efficiently retrieves historical data for multiple asset properties in a single API call.
    Supports time range filtering and data quality filtering per entry.
    """
    logger.info(f'Executing batch_get_asset_property_value_history for {len(entries)} entries')
    kwargs = {}
    if max_results:
        kwargs['maxResults'] = max_results
    if next_token:
        kwargs['nextToken'] = next_token
    
    return await iot_sitewise.batch_get_asset_property_value_history(entries=entries, **kwargs)


@mcp.tool(name='batch_get_asset_property_aggregates')
async def batch_get_asset_property_aggregates_tool(
    entries: list = Field(..., max_length=16, description='List of property aggregate requests'),
    max_results: int = Field(None, ge=1, le=4000, description='Maximum number of results per entry'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """Get aggregated values for multiple asset properties in a single request.
    
    This tool efficiently calculates aggregated statistics for multiple asset properties in a single API call.
    Each entry must specify aggregate types, resolution, and time range.
    """
    logger.info(f'Executing batch_get_asset_property_aggregates for {len(entries)} entries')
    kwargs = {}
    if max_results:
        kwargs['maxResults'] = max_results
    if next_token:
        kwargs['nextToken'] = next_token
    
    return await iot_sitewise.batch_get_asset_property_aggregates(entries=entries, **kwargs)


@mcp.tool(name='get_interpolated_asset_property_values')
async def get_interpolated_asset_property_values_tool(
    start_time_in_seconds: int = Field(..., description='Start time in seconds since Unix epoch'),
    end_time_in_seconds: int = Field(..., description='End time in seconds since Unix epoch'),
    quality: str = Field(..., description='Quality of interpolated values (GOOD, BAD, UNCERTAIN)'),
    interval_in_seconds: int = Field(..., ge=1, description='Time interval between interpolated values'),
    type: str = Field(..., description='Type of interpolation algorithm'),
    asset_id: str = Field(None, description='The ID of the asset'),
    property_id: str = Field(None, description='The ID of the property'),
    property_alias: str = Field(None, description='The alias of the property'),
    max_results: int = Field(None, ge=1, le=10000, description='Maximum number of results to return'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """Get interpolated values for an asset property over a time range.
    
    This tool calculates interpolated values for an asset property at regular intervals
    within a specified time range using various interpolation algorithms.
    """
    logger.info(f'Executing get_interpolated_asset_property_values for asset: {asset_id}, property: {property_id or property_alias}')
    kwargs = {
        'startTimeInSeconds': start_time_in_seconds,
        'endTimeInSeconds': end_time_in_seconds,
        'quality': quality,
        'intervalInSeconds': interval_in_seconds,
        'type': type,
    }
    if asset_id:
        kwargs['assetId'] = asset_id
    if property_id:
        kwargs['propertyId'] = property_id
    if property_alias:
        kwargs['propertyAlias'] = property_alias
    if max_results:
        kwargs['maxResults'] = max_results
    if next_token:
        kwargs['nextToken'] = next_token
    
    return await iot_sitewise.get_interpolated_asset_property_values(**kwargs)


@mcp.tool(name='list_gateways')
async def list_gateways_tool(
    max_results: int = Field(None, ge=1, le=250, description='Maximum number of results to return'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """List all IoT SiteWise gateways.
    
    This tool retrieves a list of all IoT SiteWise gateways in your account.
    Gateways connect your on-premises data sources to AWS IoT SiteWise.
    """
    logger.info('Executing list_gateways')
    return await iot_sitewise.list_gateways(max_results=max_results, next_token=next_token)


@mcp.tool(name='describe_gateway')
async def describe_gateway_tool(
    gateway_id: str = Field(..., description='The ID of the gateway'),
) -> str:
    """Get detailed information about a specific gateway.
    
    This tool provides comprehensive details about a gateway including its configuration,
    capabilities, and current status.
    """
    logger.info(f'Executing describe_gateway for gateway: {gateway_id}')
    return await iot_sitewise.describe_gateway(gateway_id=gateway_id)


@mcp.tool(name='describe_gateway_capability_configuration')
async def describe_gateway_capability_configuration_tool(
    gateway_id: str = Field(..., description='The ID of the gateway'),
    capability_namespace: str = Field(..., description='The namespace of the capability'),
) -> str:
    """Get the capability configuration for a gateway.
    
    This tool retrieves the configuration for a specific capability of a gateway.
    Capabilities define how the gateway processes and forwards data.
    """
    logger.info(f'Executing describe_gateway_capability_configuration for gateway: {gateway_id}, capability: {capability_namespace}')
    return await iot_sitewise.describe_gateway_capability_configuration(
        gateway_id=gateway_id,
        capability_namespace=capability_namespace
    )


@mcp.tool(name='list_portals')
async def list_portals_tool(
    max_results: int = Field(None, ge=1, le=250, description='Maximum number of results to return'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """List all IoT SiteWise Monitor portals.
    
    This tool retrieves a list of all IoT SiteWise Monitor portals in your account.
    Portals provide web-based dashboards for visualizing your IoT data.
    """
    logger.info('Executing list_portals')
    return await iot_sitewise.list_portals(max_results=max_results, next_token=next_token)


@mcp.tool(name='list_dashboards')
async def list_dashboards_tool(
    project_id: str = Field(..., description='The ID of the project'),
    max_results: int = Field(None, ge=1, le=250, description='Maximum number of results to return'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """List dashboards in a project.
    
    This tool retrieves all dashboards within a specified project.
    Dashboards contain visualizations and metrics for your IoT data.
    """
    logger.info(f'Executing list_dashboards for project: {project_id}')
    return await iot_sitewise.list_dashboards(
        project_id=project_id,
        max_results=max_results,
        next_token=next_token
    )


@mcp.tool(name='list_projects')
async def list_projects_tool(
    portal_id: str = Field(..., description='The ID of the portal'),
    max_results: int = Field(None, ge=1, le=250, description='Maximum number of results to return'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """List projects in a portal.
    
    This tool retrieves all projects within a specified portal.
    Projects organize related dashboards and assets within a portal.
    """
    logger.info(f'Executing list_projects for portal: {portal_id}')
    return await iot_sitewise.list_projects(
        portal_id=portal_id,
        max_results=max_results,
        next_token=next_token
    )


@mcp.tool(name='list_time_series')
async def list_time_series_tool(
    asset_id: str = Field(None, description='Filter by asset ID'),
    alias_prefix: str = Field(None, description='Filter by alias prefix'),
    time_series_type: str = Field(None, description='Filter by time series type (ASSOCIATED, DISASSOCIATED)'),
    max_results: int = Field(None, ge=1, le=250, description='Maximum number of results to return'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """List time series in your account.
    
    This tool retrieves time series data streams in your IoT SiteWise account.
    You can filter by asset ID, alias prefix, or association type.
    """
    logger.info('Executing list_time_series')
    kwargs = {}
    if asset_id:
        kwargs['assetId'] = asset_id
    if alias_prefix:
        kwargs['aliasPrefix'] = alias_prefix
    if time_series_type:
        kwargs['timeSeriesType'] = time_series_type
    if max_results:
        kwargs['maxResults'] = max_results
    if next_token:
        kwargs['nextToken'] = next_token
    
    return await iot_sitewise.list_time_series(**kwargs)


@mcp.tool(name='describe_time_series')
async def describe_time_series_tool(
    alias: str = Field(None, description='The alias of the time series'),
    asset_id: str = Field(None, description='The ID of the asset'),
    property_id: str = Field(None, description='The ID of the property'),
) -> str:
    """Get detailed information about a time series.
    
    This tool provides comprehensive details about a time series including its
    data type, alias, and association status.
    """
    logger.info(f'Executing describe_time_series for alias: {alias}')
    kwargs = {}
    if alias:
        kwargs['alias'] = alias
    if asset_id:
        kwargs['assetId'] = asset_id
    if property_id:
        kwargs['propertyId'] = property_id
    
    return await iot_sitewise.describe_time_series(**kwargs)


@mcp.tool(name='list_access_policies')
async def list_access_policies_tool(
    identity_type: str = Field(None, description='Type of identity (USER, GROUP, IAM)'),
    identity_id: str = Field(None, description='ID of the identity'),
    resource_type: str = Field(None, description='Type of resource (PORTAL, PROJECT)'),
    resource_id: str = Field(None, description='ID of the resource'),
    iam_arn: str = Field(None, description='ARN of the IAM identity'),
    max_results: int = Field(None, ge=1, le=250, description='Maximum number of results to return'),
    next_token: str = Field(None, description='Token for pagination'),
) -> str:
    """List access policies for IoT SiteWise Monitor.
    
    This tool retrieves access policies that control user permissions for portals and projects.
    You can filter by identity type, resource type, or specific IDs.
    """
    logger.info('Executing list_access_policies')
    kwargs = {}
    if identity_type:
        kwargs['identityType'] = identity_type
    if identity_id:
        kwargs['identityId'] = identity_id
    if resource_type:
        kwargs['resourceType'] = resource_type
    if resource_id:
        kwargs['resourceId'] = resource_id
    if iam_arn:
        kwargs['iamArn'] = iam_arn
    if max_results:
        kwargs['maxResults'] = max_results
    if next_token:
        kwargs['nextToken'] = next_token
    
    return await iot_sitewise.list_access_policies(**kwargs)


@mcp.tool(name='list_tags_for_resource')
async def list_tags_for_resource_tool(
    resource_arn: str = Field(..., description='The ARN of the resource'),
) -> str:
    """List tags for a resource.
    
    This tool retrieves all tags associated with a specified AWS IoT SiteWise resource.
    Tags are key-value pairs used for resource organization and cost allocation.
    """
    logger.info(f'Executing list_tags_for_resource for resource: {resource_arn}')
    return await iot_sitewise.list_tags_for_resource(resource_arn=resource_arn)


# Write operation tools (21 tools with safety indicators)
@mcp.tool(name='create_asset')
async def create_asset_tool(
    asset_name: str = Field(..., description='Name of the asset'),
    asset_model_id: str = Field(..., description='ID of the asset model to use'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
    tags: dict = Field(None, description='Tags to apply to the asset'),
    asset_description: str = Field(None, description='Description of the asset'),
    asset_id: str = Field(None, description='Custom asset ID (optional)'),
) -> str:
    """⚠️ WRITE OPERATION: Create a new asset from an asset model.
    
    This tool creates a new asset instance based on an existing asset model.
    The asset will inherit the properties and structure defined in the asset model.
    """
    logger.warning(f'Executing create_asset: {asset_name} from model {asset_model_id}')
    kwargs = {
        'assetName': asset_name,
        'assetModelId': asset_model_id,
    }
    if client_token:
        kwargs['clientToken'] = client_token
    if tags:
        kwargs['tags'] = tags
    if asset_description:
        kwargs['assetDescription'] = asset_description
    if asset_id:
        kwargs['assetId'] = asset_id
    
    return await iot_sitewise.create_asset(**kwargs)


@mcp.tool(name='update_asset')
async def update_asset_tool(
    asset_id: str = Field(..., description='ID of the asset to update'),
    asset_name: str = Field(..., description='New name for the asset'),
    asset_description: str = Field(None, description='New description for the asset'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """⚠️ WRITE OPERATION: Update an existing asset.
    
    This tool modifies the name and description of an existing asset.
    The asset's structure and properties are defined by its asset model and cannot be changed.
    """
    logger.warning(f'Executing update_asset: {asset_id} -> {asset_name}')
    kwargs = {
        'assetId': asset_id,
        'assetName': asset_name,
    }
    if asset_description:
        kwargs['assetDescription'] = asset_description
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.update_asset(**kwargs)


@mcp.tool(name='delete_asset')
async def delete_asset_tool(
    asset_id: str = Field(..., description='ID of the asset to delete'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """🚨 DESTRUCTIVE OPERATION: Delete an asset permanently.
    
    WARNING: This operation permanently deletes an asset and all its associated data.
    This action cannot be undone. Ensure you have proper backups before proceeding.
    """
    logger.critical(f'Executing delete_asset: {asset_id} - DESTRUCTIVE OPERATION')
    kwargs = {'assetId': asset_id}
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.delete_asset(**kwargs)


@mcp.tool(name='associate_assets')
async def associate_assets_tool(
    asset_id: str = Field(..., description='ID of the parent asset'),
    hierarchy_id: str = Field(..., description='ID of the hierarchy in the parent asset model'),
    child_asset_id: str = Field(..., description='ID of the child asset'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """⚠️ WRITE OPERATION: Associate a child asset with a parent asset.
    
    This tool creates a hierarchical relationship between two assets based on the
    hierarchy definitions in the parent asset's model.
    """
    logger.warning(f'Executing associate_assets: parent {asset_id} -> child {child_asset_id}')
    kwargs = {
        'assetId': asset_id,
        'hierarchyId': hierarchy_id,
        'childAssetId': child_asset_id,
    }
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.associate_assets(**kwargs)


@mcp.tool(name='disassociate_assets')
async def disassociate_assets_tool(
    asset_id: str = Field(..., description='ID of the parent asset'),
    hierarchy_id: str = Field(..., description='ID of the hierarchy in the parent asset model'),
    child_asset_id: str = Field(..., description='ID of the child asset'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """⚠️ WRITE OPERATION: Remove association between parent and child assets.
    
    This tool removes a hierarchical relationship between two assets.
    The child asset will no longer be associated with the parent asset.
    """
    logger.warning(f'Executing disassociate_assets: parent {asset_id} -/-> child {child_asset_id}')
    kwargs = {
        'assetId': asset_id,
        'hierarchyId': hierarchy_id,
        'childAssetId': child_asset_id,
    }
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.disassociate_assets(**kwargs)


@mcp.tool(name='create_asset_model')
async def create_asset_model_tool(
    asset_model_name: str = Field(..., description='Name of the asset model'),
    asset_model_description: str = Field(None, description='Description of the asset model'),
    asset_model_properties: list = Field(None, description='Properties of the asset model'),
    asset_model_hierarchies: list = Field(None, description='Hierarchies of the asset model'),
    asset_model_composite_models: list = Field(None, description='Composite models of the asset model'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
    tags: dict = Field(None, description='Tags to apply to the asset model'),
    asset_model_id: str = Field(None, description='Custom asset model ID (optional)'),
    asset_model_external_id: str = Field(None, description='External ID for the asset model'),
) -> str:
    """⚠️ WRITE OPERATION: Create a new asset model.
    
    This tool creates a new asset model that defines the structure, properties, and
    hierarchies for a type of industrial asset.
    """
    logger.warning(f'Executing create_asset_model: {asset_model_name}')
    kwargs = {'assetModelName': asset_model_name}
    if asset_model_description:
        kwargs['assetModelDescription'] = asset_model_description
    if asset_model_properties:
        kwargs['assetModelProperties'] = asset_model_properties
    if asset_model_hierarchies:
        kwargs['assetModelHierarchies'] = asset_model_hierarchies
    if asset_model_composite_models:
        kwargs['assetModelCompositeModels'] = asset_model_composite_models
    if client_token:
        kwargs['clientToken'] = client_token
    if tags:
        kwargs['tags'] = tags
    if asset_model_id:
        kwargs['assetModelId'] = asset_model_id
    if asset_model_external_id:
        kwargs['assetModelExternalId'] = asset_model_external_id
    
    return await iot_sitewise.create_asset_model(**kwargs)


@mcp.tool(name='update_asset_model')
async def update_asset_model_tool(
    asset_model_id: str = Field(..., description='ID of the asset model to update'),
    asset_model_name: str = Field(..., description='New name for the asset model'),
    asset_model_description: str = Field(None, description='New description for the asset model'),
    asset_model_properties: list = Field(None, description='Updated properties of the asset model'),
    asset_model_hierarchies: list = Field(None, description='Updated hierarchies of the asset model'),
    asset_model_composite_models: list = Field(None, description='Updated composite models'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """⚠️ WRITE OPERATION: Update an existing asset model.
    
    This tool modifies an existing asset model's properties, hierarchies, and configuration.
    Changes will affect all assets created from this model.
    """
    logger.warning(f'Executing update_asset_model: {asset_model_id} -> {asset_model_name}')
    kwargs = {
        'assetModelId': asset_model_id,
        'assetModelName': asset_model_name,
    }
    if asset_model_description:
        kwargs['assetModelDescription'] = asset_model_description
    if asset_model_properties:
        kwargs['assetModelProperties'] = asset_model_properties
    if asset_model_hierarchies:
        kwargs['assetModelHierarchies'] = asset_model_hierarchies
    if asset_model_composite_models:
        kwargs['assetModelCompositeModels'] = asset_model_composite_models
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.update_asset_model(**kwargs)


@mcp.tool(name='delete_asset_model')
async def delete_asset_model_tool(
    asset_model_id: str = Field(..., description='ID of the asset model to delete'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """🚨 DESTRUCTIVE OPERATION: Delete an asset model permanently.
    
    WARNING: This operation permanently deletes an asset model and prevents creation of new assets
    from this model. Existing assets based on this model will become orphaned.
    This action cannot be undone.
    """
    logger.critical(f'Executing delete_asset_model: {asset_model_id} - DESTRUCTIVE OPERATION')
    kwargs = {'assetModelId': asset_model_id}
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.delete_asset_model(**kwargs)


@mcp.tool(name='batch_put_asset_property_value')
async def batch_put_asset_property_value_tool(
    entries: list = Field(..., max_length=10, description='List of property values to send'),
) -> str:
    """⚠️ WRITE OPERATION: Send property values to IoT SiteWise.
    
    This tool ingests time-series data into IoT SiteWise properties.
    Each entry contains property values with timestamps and quality indicators.
    """
    logger.warning(f'Executing batch_put_asset_property_value with {len(entries)} entries')
    return await iot_sitewise.batch_put_asset_property_value(entries=entries)


@mcp.tool(name='create_gateway')
async def create_gateway_tool(
    gateway_name: str = Field(..., description='Name of the gateway'),
    gateway_platform: dict = Field(..., description='Platform configuration for the gateway'),
    tags: dict = Field(None, description='Tags to apply to the gateway'),
) -> str:
    """⚠️ WRITE OPERATION: Create a new IoT SiteWise gateway.
    
    This tool creates a new gateway to connect on-premises data sources to AWS IoT SiteWise.
    Requires platform configuration for Greengrass v1 or v2.
    """
    logger.warning(f'Executing create_gateway: {gateway_name}')
    kwargs = {
        'gatewayName': gateway_name,
        'gatewayPlatform': gateway_platform,
    }
    if tags:
        kwargs['tags'] = tags
    
    return await iot_sitewise.create_gateway(**kwargs)


@mcp.tool(name='update_gateway')
async def update_gateway_tool(
    gateway_id: str = Field(..., description='ID of the gateway to update'),
    gateway_name: str = Field(..., description='New name for the gateway'),
) -> str:
    """⚠️ WRITE OPERATION: Update an existing gateway.
    
    This tool modifies the name of an existing IoT SiteWise gateway.
    """
    logger.warning(f'Executing update_gateway: {gateway_id} -> {gateway_name}')
    return await iot_sitewise.update_gateway(gatewayId=gateway_id, gatewayName=gateway_name)


@mcp.tool(name='delete_gateway')
async def delete_gateway_tool(
    gateway_id: str = Field(..., description='ID of the gateway to delete'),
) -> str:
    """🚨 DESTRUCTIVE OPERATION: Delete a gateway permanently.
    
    WARNING: This operation permanently deletes a gateway and stops all data collection
    from connected sources. This action cannot be undone.
    """
    logger.critical(f'Executing delete_gateway: {gateway_id} - DESTRUCTIVE OPERATION')
    return await iot_sitewise.delete_gateway(gatewayId=gateway_id)


@mcp.tool(name='update_gateway_capability_configuration')
async def update_gateway_capability_configuration_tool(
    gateway_id: str = Field(..., description='ID of the gateway'),
    capability_namespace: str = Field(..., description='Namespace of the capability'),
    capability_configuration: str = Field(..., description='JSON configuration for the capability'),
) -> str:
    """⚠️ WRITE OPERATION: Update gateway capability configuration.
    
    This tool modifies the configuration of a specific capability on a gateway.
    Capabilities control how the gateway processes and forwards data.
    """
    logger.warning(f'Executing update_gateway_capability_configuration: {gateway_id}/{capability_namespace}')
    return await iot_sitewise.update_gateway_capability_configuration(
        gatewayId=gateway_id,
        capabilityNamespace=capability_namespace,
        capabilityConfiguration=capability_configuration
    )


@mcp.tool(name='create_portal')
async def create_portal_tool(
    portal_name: str = Field(..., description='Name of the portal'),
    portal_contact_email: str = Field(..., description='Contact email for the portal'),
    role_arn: str = Field(..., description='ARN of the service role for the portal'),
    portal_description: str = Field(None, description='Description of the portal'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
    portal_logo_image_file: dict = Field(None, description='Logo image file for the portal'),
    tags: dict = Field(None, description='Tags to apply to the portal'),
    portal_auth_mode: str = Field(None, description='Authentication mode for the portal (IAM, SSO)'),
) -> str:
    """⚠️ WRITE OPERATION: Create a new IoT SiteWise Monitor portal.
    
    This tool creates a new web portal for visualizing and monitoring IoT data.
    Requires a service role for portal access to IoT SiteWise resources.
    """
    logger.warning(f'Executing create_portal: {portal_name}')
    kwargs = {
        'portalName': portal_name,
        'portalContactEmail': portal_contact_email,
        'roleArn': role_arn,
    }
    if portal_description:
        kwargs['portalDescription'] = portal_description
    if client_token:
        kwargs['clientToken'] = client_token
    if portal_logo_image_file:
        kwargs['portalLogoImageFile'] = portal_logo_image_file
    if tags:
        kwargs['tags'] = tags
    if portal_auth_mode:
        kwargs['portalAuthMode'] = portal_auth_mode
    
    return await iot_sitewise.create_portal(**kwargs)


@mcp.tool(name='update_portal')
async def update_portal_tool(
    portal_id: str = Field(..., description='ID of the portal to update'),
    portal_name: str = Field(..., description='New name for the portal'),
    portal_contact_email: str = Field(..., description='New contact email for the portal'),
    role_arn: str = Field(..., description='New ARN of the service role for the portal'),
    portal_description: str = Field(None, description='New description for the portal'),
    portal_logo_image_file: dict = Field(None, description='New logo image file for the portal'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """⚠️ WRITE OPERATION: Update an existing portal.
    
    This tool modifies the configuration of an existing IoT SiteWise Monitor portal.
    """
    logger.warning(f'Executing update_portal: {portal_id} -> {portal_name}')
    kwargs = {
        'portalId': portal_id,
        'portalName': portal_name,
        'portalContactEmail': portal_contact_email,
        'roleArn': role_arn,
    }
    if portal_description:
        kwargs['portalDescription'] = portal_description
    if portal_logo_image_file:
        kwargs['portalLogoImageFile'] = portal_logo_image_file
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.update_portal(**kwargs)


@mcp.tool(name='delete_portal')
async def delete_portal_tool(
    portal_id: str = Field(..., description='ID of the portal to delete'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """🚨 DESTRUCTIVE OPERATION: Delete a portal permanently.
    
    WARNING: This operation permanently deletes a portal and all its associated projects
    and dashboards. This action cannot be undone.
    """
    logger.critical(f'Executing delete_portal: {portal_id} - DESTRUCTIVE OPERATION')
    kwargs = {'portalId': portal_id}
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.delete_portal(**kwargs)


@mcp.tool(name='create_project')
async def create_project_tool(
    portal_id: str = Field(..., description='ID of the portal'),
    project_name: str = Field(..., description='Name of the project'),
    project_description: str = Field(None, description='Description of the project'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
    tags: dict = Field(None, description='Tags to apply to the project'),
) -> str:
    """⚠️ WRITE OPERATION: Create a new project in a portal.
    
    This tool creates a new project within an IoT SiteWise Monitor portal.
    Projects organize related dashboards and provide access control.
    """
    logger.warning(f'Executing create_project: {project_name} in portal {portal_id}')
    kwargs = {
        'portalId': portal_id,
        'projectName': project_name,
    }
    if project_description:
        kwargs['projectDescription'] = project_description
    if client_token:
        kwargs['clientToken'] = client_token
    if tags:
        kwargs['tags'] = tags
    
    return await iot_sitewise.create_project(**kwargs)


@mcp.tool(name='create_dashboard')
async def create_dashboard_tool(
    project_id: str = Field(..., description='ID of the project'),
    dashboard_name: str = Field(..., description='Name of the dashboard'),
    dashboard_definition: str = Field(..., description='JSON definition of the dashboard'),
    dashboard_description: str = Field(None, description='Description of the dashboard'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
    tags: dict = Field(None, description='Tags to apply to the dashboard'),
) -> str:
    """⚠️ WRITE OPERATION: Create a new dashboard in a project.
    
    This tool creates a new dashboard within a project. The dashboard definition
    specifies the layout, widgets, and data sources for the dashboard.
    """
    logger.warning(f'Executing create_dashboard: {dashboard_name} in project {project_id}')
    kwargs = {
        'projectId': project_id,
        'dashboardName': dashboard_name,
        'dashboardDefinition': dashboard_definition,
    }
    if dashboard_description:
        kwargs['dashboardDescription'] = dashboard_description
    if client_token:
        kwargs['clientToken'] = client_token
    if tags:
        kwargs['tags'] = tags
    
    return await iot_sitewise.create_dashboard(**kwargs)


@mcp.tool(name='update_dashboard')
async def update_dashboard_tool(
    dashboard_id: str = Field(..., description='ID of the dashboard to update'),
    dashboard_name: str = Field(..., description='New name for the dashboard'),
    dashboard_definition: str = Field(..., description='New JSON definition of the dashboard'),
    dashboard_description: str = Field(None, description='New description for the dashboard'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """⚠️ WRITE OPERATION: Update an existing dashboard.
    
    This tool modifies an existing dashboard's name, description, and definition.
    The dashboard definition controls the layout and content of the dashboard.
    """
    logger.warning(f'Executing update_dashboard: {dashboard_id} -> {dashboard_name}')
    kwargs = {
        'dashboardId': dashboard_id,
        'dashboardName': dashboard_name,
        'dashboardDefinition': dashboard_definition,
    }
    if dashboard_description:
        kwargs['dashboardDescription'] = dashboard_description
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.update_dashboard(**kwargs)


@mcp.tool(name='delete_dashboard')
async def delete_dashboard_tool(
    dashboard_id: str = Field(..., description='ID of the dashboard to delete'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """🚨 DESTRUCTIVE OPERATION: Delete a dashboard permanently.
    
    WARNING: This operation permanently deletes a dashboard and all its visualizations.
    This action cannot be undone.
    """
    logger.critical(f'Executing delete_dashboard: {dashboard_id} - DESTRUCTIVE OPERATION')
    kwargs = {'dashboardId': dashboard_id}
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.delete_dashboard(**kwargs)


@mcp.tool(name='create_access_policy')
async def create_access_policy_tool(
    access_policy_identity: dict = Field(..., description='Identity for the access policy'),
    access_policy_resource: dict = Field(..., description='Resource for the access policy'),
    access_policy_permission: str = Field(..., description='Permission level for the access policy (ADMINISTRATOR, VIEWER)'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
    tags: dict = Field(None, description='Tags to apply to the access policy'),
) -> str:
    """🔐 SECURITY OPERATION: Create an access policy for IoT SiteWise Monitor.
    
    This tool creates a security policy that grants users or groups access to specific
    portals or projects with defined permission levels.
    """
    logger.warning(f'Executing create_access_policy with permission: {access_policy_permission}')
    kwargs = {
        'accessPolicyIdentity': access_policy_identity,
        'accessPolicyResource': access_policy_resource,
        'accessPolicyPermission': access_policy_permission,
    }
    if client_token:
        kwargs['clientToken'] = client_token
    if tags:
        kwargs['tags'] = tags
    
    return await iot_sitewise.create_access_policy(**kwargs)


@mcp.tool(name='update_access_policy')
async def update_access_policy_tool(
    access_policy_id: str = Field(..., description='ID of the access policy to update'),
    access_policy_identity: dict = Field(..., description='New identity for the access policy'),
    access_policy_resource: dict = Field(..., description='New resource for the access policy'),
    access_policy_permission: str = Field(..., description='New permission level (ADMINISTRATOR, VIEWER)'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """🔐 SECURITY OPERATION: Update an existing access policy.
    
    This tool modifies an existing security policy's identity, resource, or permission level.
    Changes take effect immediately for affected users.
    """
    logger.warning(f'Executing update_access_policy: {access_policy_id} -> {access_policy_permission}')
    kwargs = {
        'accessPolicyId': access_policy_id,
        'accessPolicyIdentity': access_policy_identity,
        'accessPolicyResource': access_policy_resource,
        'accessPolicyPermission': access_policy_permission,
    }
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.update_access_policy(**kwargs)


@mcp.tool(name='delete_access_policy')
async def delete_access_policy_tool(
    access_policy_id: str = Field(..., description='ID of the access policy to delete'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """🚨 DESTRUCTIVE SECURITY OPERATION: Delete an access policy permanently.
    
    WARNING: This operation permanently deletes a security policy and immediately
    revokes access for affected users. This action cannot be undone.
    """
    logger.critical(f'Executing delete_access_policy: {access_policy_id} - DESTRUCTIVE SECURITY OPERATION')
    kwargs = {'accessPolicyId': access_policy_id}
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.delete_access_policy(**kwargs)


@mcp.tool(name='associate_time_series_to_asset_property')
async def associate_time_series_to_asset_property_tool(
    alias: str = Field(..., description='Alias of the time series'),
    asset_id: str = Field(..., description='ID of the asset'),
    property_id: str = Field(..., description='ID of the property'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """⚠️ WRITE OPERATION: Associate a time series with an asset property.
    
    This tool creates an association between a time series and an asset property.
    The time series data will be associated with the specified property.
    """
    logger.warning(f'Executing associate_time_series_to_asset_property: {alias} -> {asset_id}/{property_id}')
    kwargs = {
        'alias': alias,
        'assetId': asset_id,
        'propertyId': property_id,
    }
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.associate_time_series_to_asset_property(**kwargs)


@mcp.tool(name='disassociate_time_series_from_asset_property')
async def disassociate_time_series_from_asset_property_tool(
    alias: str = Field(..., description='Alias of the time series'),
    asset_id: str = Field(..., description='ID of the asset'),
    property_id: str = Field(..., description='ID of the property'),
    client_token: str = Field(None, description='Unique case-sensitive identifier for the request'),
) -> str:
    """⚠️ WRITE OPERATION: Remove association between time series and asset property.
    
    This tool removes the association between a time series and an asset property.
    The time series will become disassociated and can be associated with another property.
    """
    logger.warning(f'Executing disassociate_time_series_from_asset_property: {alias} -/-> {asset_id}/{property_id}')
    kwargs = {
        'alias': alias,
        'assetId': asset_id,
        'propertyId': property_id,
    }
    if client_token:
        kwargs['clientToken'] = client_token
    
    return await iot_sitewise.disassociate_time_series_from_asset_property(**kwargs)


@mcp.tool(name='tag_resource')
async def tag_resource_tool(
    resource_arn: str = Field(..., description='ARN of the resource to tag'),
    tags: dict = Field(..., description='Tags to add to the resource'),
) -> str:
    """⚠️ WRITE OPERATION: Add tags to a resource.
    
    This tool adds or updates tags on an AWS IoT SiteWise resource.
    Tags are key-value pairs used for organization and cost allocation.
    """
    logger.warning(f'Executing tag_resource: {resource_arn} with {len(tags)} tags')
    return await iot_sitewise.tag_resource(resource_arn=resource_arn, tags=tags)


@mcp.tool(name='untag_resource')
async def untag_resource_tool(
    resource_arn: str = Field(..., description='ARN of the resource to untag'),
    tag_keys: list = Field(..., description='Keys of tags to remove'),
) -> str:
    """⚠️ WRITE OPERATION: Remove tags from a resource.
    
    This tool removes specified tags from an AWS IoT SiteWise resource.
    Only the specified tag keys will be removed.
    """
    logger.warning(f'Executing untag_resource: {resource_arn} removing {len(tag_keys)} tags')
    return await iot_sitewise.untag_resource(resource_arn=resource_arn, tag_keys=tag_keys)


def main():
    """Run the MCP server with CLI argument support."""
    mcp.run()


if __name__ == '__main__':
    main()