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

"""Constants for the AWS IoT SiteWise MCP server."""

# Default pagination values
DEFAULT_MAX_RESULTS = 250
MAX_BATCH_ENTRIES = 128
MAX_PROPERTY_HISTORY_BATCH_ENTRIES = 16
MAX_PROPERTY_AGGREGATES_BATCH_ENTRIES = 16
MAX_PROPERTY_VALUES_BATCH_ENTRIES = 10

# Data quality values
DATA_QUALITIES = ['GOOD', 'BAD', 'UNCERTAIN']

# Time ordering options
TIME_ORDERING = ['ASCENDING', 'DESCENDING']

# Aggregate types
AGGREGATE_TYPES = [
    'AVERAGE',
    'COUNT',
    'MAXIMUM',
    'MINIMUM',
    'SUM',
    'STANDARD_DEVIATION'
]

# Portal authentication modes
PORTAL_AUTH_MODES = ['IAM', 'SSO']

# Access policy permissions
ACCESS_POLICY_PERMISSIONS = ['ADMINISTRATOR', 'VIEWER']

# Identity types
IDENTITY_TYPES = ['USER', 'GROUP', 'IAM']

# Resource types
RESOURCE_TYPES = ['PORTAL', 'PROJECT']

# Time series types
TIME_SERIES_TYPES = ['ASSOCIATED', 'DISASSOCIATED']

# Traversal directions
TRAVERSAL_DIRECTIONS = ['PARENT', 'CHILD']

# Safety categorization for tools
READ_ONLY_TOOLS = {
    'list_asset_models',
    'describe_asset_model',
    'list_assets',
    'describe_asset',
    'get_asset_property_value',
    'get_asset_property_value_history',
    'get_asset_property_aggregates',
    'list_associated_assets',
    'batch_get_asset_property_value',
    'batch_get_asset_property_value_history',
    'batch_get_asset_property_aggregates',
    'get_interpolated_asset_property_values',
    'list_gateways',
    'describe_gateway',
    'describe_gateway_capability_configuration',
    'list_portals',
    'list_dashboards',
    'list_projects',
    'list_time_series',
    'describe_time_series',
    'list_access_policies',
    'list_tags_for_resource',
}

WRITE_TOOLS = {
    'create_asset',
    'update_asset',
    'associate_assets',
    'disassociate_assets',
    'create_asset_model',
    'update_asset_model',
    'batch_put_asset_property_value',
    'create_gateway',
    'update_gateway',
    'update_gateway_capability_configuration',
    'create_portal',
    'update_portal',
    'create_project',
    'create_dashboard',
    'update_dashboard',
    'create_access_policy',
    'update_access_policy',
    'associate_time_series_to_asset_property',
    'disassociate_time_series_from_asset_property',
    'tag_resource',
    'untag_resource',
}

DESTRUCTIVE_TOOLS = {
    'delete_asset',
    'delete_asset_model',
    'delete_gateway',
    'delete_portal',
    'delete_dashboard',
    'delete_access_policy',
}

SECURITY_TOOLS = {
    'create_access_policy',
    'update_access_policy',
    'delete_access_policy',
}

# Tool descriptions with safety indicators
TOOL_SAFETY_DESCRIPTIONS = {
    # Read-only tools (no safety indicator needed)
    **{tool: '' for tool in READ_ONLY_TOOLS},
    
    # Write tools with ⚠️ indicator
    **{tool: '⚠️ WRITE OPERATION: ' for tool in WRITE_TOOLS},
    
    # Destructive tools with 🚨 indicator
    **{tool: '🚨 DESTRUCTIVE OPERATION: ' for tool in DESTRUCTIVE_TOOLS},
    
    # Security tools with 🔐 indicator
    'create_access_policy': '🔐 SECURITY OPERATION: ',
    'update_access_policy': '🔐 SECURITY OPERATION: ',
    'delete_access_policy': '🚨 DESTRUCTIVE SECURITY OPERATION: ',
}

# AWS SDK service name
AWS_SERVICE_NAME = 'iotsitewise'