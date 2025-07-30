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

"""Pydantic models for AWS IoT SiteWise MCP server tool parameters."""

from enum import Enum
from typing import Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field


class DataQuality(str, Enum):
    """Data quality values for IoT SiteWise properties."""
    GOOD = 'GOOD'
    BAD = 'BAD'
    UNCERTAIN = 'UNCERTAIN'


class TimeOrdering(str, Enum):
    """Time ordering options for property data queries."""
    ASCENDING = 'ASCENDING'
    DESCENDING = 'DESCENDING'


class TraversalDirection(str, Enum):
    """Direction to traverse asset hierarchies."""
    PARENT = 'PARENT'
    CHILD = 'CHILD'


class TimeSeriesType(str, Enum):
    """Time series association types."""
    ASSOCIATED = 'ASSOCIATED'
    DISASSOCIATED = 'DISASSOCIATED'


class IdentityType(str, Enum):
    """Identity types for access policies."""
    USER = 'USER'
    GROUP = 'GROUP'
    IAM = 'IAM'


class ResourceType(str, Enum):
    """Resource types for access policies."""
    PORTAL = 'PORTAL'
    PROJECT = 'PROJECT'


class AccessPolicyPermission(str, Enum):
    """Access policy permission levels."""
    ADMINISTRATOR = 'ADMINISTRATOR'
    VIEWER = 'VIEWER'


class PortalAuthMode(str, Enum):
    """Portal authentication modes."""
    IAM = 'IAM'
    SSO = 'SSO'


# Base property value model
class PropertyValue(BaseModel):
    """IoT SiteWise property value."""
    stringValue: Optional[str] = None
    integerValue: Optional[int] = None
    doubleValue: Optional[float] = None
    booleanValue: Optional[bool] = None


class PropertyTimestamp(BaseModel):
    """Timestamp for IoT SiteWise property values."""
    timeInSeconds: int = Field(..., description='Time in seconds since Unix epoch')
    offsetInNanos: Optional[int] = Field(None, description='Nanosecond offset')


class PropertyValueWithTimestamp(BaseModel):
    """Property value with timestamp and quality."""
    value: PropertyValue = Field(..., description='Property value')
    timestamp: PropertyTimestamp = Field(..., description='Timestamp of the value')
    quality: Optional[DataQuality] = Field(None, description='Quality of the value')


# Read-only tool models
class ListAssetModelsParams(BaseModel):
    """Parameters for list_asset_models tool."""
    maxResults: Optional[int] = Field(None, ge=1, le=250, description='Maximum number of results to return')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


class DescribeAssetModelParams(BaseModel):
    """Parameters for describe_asset_model tool."""
    assetModelId: str = Field(..., description='The ID of the asset model')


class ListAssetsParams(BaseModel):
    """Parameters for list_assets tool."""
    assetModelId: Optional[str] = Field(None, description='Filter assets by asset model ID')
    maxResults: Optional[int] = Field(None, ge=1, le=250, description='Maximum number of results to return')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


class DescribeAssetParams(BaseModel):
    """Parameters for describe_asset tool."""
    assetId: str = Field(..., description='The ID of the asset')


class GetAssetPropertyValueParams(BaseModel):
    """Parameters for get_asset_property_value tool."""
    assetId: str = Field(..., description='The ID of the asset')
    propertyId: Optional[str] = Field(None, description='The ID of the property')
    propertyAlias: Optional[str] = Field(None, description='The alias of the property (alternative to propertyId)')


class GetAssetPropertyValueHistoryParams(BaseModel):
    """Parameters for get_asset_property_value_history tool."""
    assetId: str = Field(..., description='The ID of the asset')
    propertyId: Optional[str] = Field(None, description='The ID of the property')
    propertyAlias: Optional[str] = Field(None, description='The alias of the property')
    startDate: Optional[str] = Field(None, description='Start date for the query (ISO 8601 format)')
    endDate: Optional[str] = Field(None, description='End date for the query (ISO 8601 format)')
    qualities: Optional[List[DataQuality]] = Field(None, description='Filter by data quality (GOOD, BAD, UNCERTAIN)')
    timeOrdering: Optional[TimeOrdering] = Field(None, description='Order of returned data points')
    maxResults: Optional[int] = Field(None, ge=1, le=4000, description='Maximum number of results to return')


class GetAssetPropertyAggregatesParams(BaseModel):
    """Parameters for get_asset_property_aggregates tool."""
    assetId: str = Field(..., description='The ID of the asset')
    propertyId: Optional[str] = Field(None, description='The ID of the property')
    propertyAlias: Optional[str] = Field(None, description='The alias of the property')
    aggregateTypes: List[str] = Field(..., description='Types of aggregates (AVERAGE, COUNT, MAXIMUM, MINIMUM, SUM, STANDARD_DEVIATION)')
    resolution: str = Field(..., description='Time interval for aggregation (e.g., 1m, 5m, 1h, 1d)')
    startDate: str = Field(..., description='Start date for the query (ISO 8601 format)')
    endDate: str = Field(..., description='End date for the query (ISO 8601 format)')
    qualities: Optional[List[DataQuality]] = Field(None, description='Filter by data quality')


class ListAssociatedAssetsParams(BaseModel):
    """Parameters for list_associated_assets tool."""
    assetId: str = Field(..., description='The ID of the parent asset')
    hierarchyId: Optional[str] = Field(None, description='The ID of the hierarchy to traverse')
    traversalDirection: Optional[TraversalDirection] = Field(None, description='Direction to traverse the hierarchy')
    maxResults: Optional[int] = Field(None, ge=1, le=250, description='Maximum number of results to return')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


# Batch operation models
class BatchPropertyValueEntry(BaseModel):
    """Entry for batch property value requests."""
    entryId: str = Field(..., description='Unique identifier for this entry')
    assetId: Optional[str] = Field(None, description='The ID of the asset')
    propertyId: Optional[str] = Field(None, description='The ID of the property')
    propertyAlias: Optional[str] = Field(None, description='The alias of the property')


class BatchGetAssetPropertyValueParams(BaseModel):
    """Parameters for batch_get_asset_property_value tool."""
    entries: List[BatchPropertyValueEntry] = Field(..., max_length=128, description='List of property value requests')


class BatchPropertyHistoryEntry(BatchPropertyValueEntry):
    """Entry for batch property history requests."""
    startDate: Optional[str] = Field(None, description='Start date for the query (ISO 8601 format)')
    endDate: Optional[str] = Field(None, description='End date for the query (ISO 8601 format)')
    qualities: Optional[List[DataQuality]] = Field(None, description='Filter by data quality')
    timeOrdering: Optional[TimeOrdering] = Field(None, description='Order of returned data points')


class BatchGetAssetPropertyValueHistoryParams(BaseModel):
    """Parameters for batch_get_asset_property_value_history tool."""
    entries: List[BatchPropertyHistoryEntry] = Field(..., max_length=16, description='List of property history requests')
    maxResults: Optional[int] = Field(None, ge=1, le=4000, description='Maximum number of results per entry')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


class BatchPropertyAggregatesEntry(BatchPropertyValueEntry):
    """Entry for batch property aggregates requests."""
    aggregateTypes: List[str] = Field(..., description='Types of aggregates')
    resolution: str = Field(..., description='Time interval for aggregation')
    startDate: str = Field(..., description='Start date for the query (ISO 8601 format)')
    endDate: str = Field(..., description='End date for the query (ISO 8601 format)')
    qualities: Optional[List[DataQuality]] = Field(None, description='Filter by data quality')


class BatchGetAssetPropertyAggregatesParams(BaseModel):
    """Parameters for batch_get_asset_property_aggregates tool."""
    entries: List[BatchPropertyAggregatesEntry] = Field(..., max_length=16, description='List of property aggregate requests')
    maxResults: Optional[int] = Field(None, ge=1, le=4000, description='Maximum number of results per entry')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


class GetInterpolatedAssetPropertyValuesParams(BaseModel):
    """Parameters for get_interpolated_asset_property_values tool."""
    assetId: Optional[str] = Field(None, description='The ID of the asset')
    propertyId: Optional[str] = Field(None, description='The ID of the property')
    propertyAlias: Optional[str] = Field(None, description='The alias of the property')
    startTimeInSeconds: int = Field(..., description='Start time in seconds since Unix epoch')
    endTimeInSeconds: int = Field(..., description='End time in seconds since Unix epoch')
    quality: DataQuality = Field(..., description='Quality of interpolated values')
    intervalInSeconds: int = Field(..., ge=1, description='Time interval between interpolated values')
    type: str = Field(..., description='Type of interpolation algorithm')
    maxResults: Optional[int] = Field(None, ge=1, le=10000, description='Maximum number of results to return')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


# Gateway models
class ListGatewaysParams(BaseModel):
    """Parameters for list_gateways tool."""
    maxResults: Optional[int] = Field(None, ge=1, le=250, description='Maximum number of results to return')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


class DescribeGatewayParams(BaseModel):
    """Parameters for describe_gateway tool."""
    gatewayId: str = Field(..., description='The ID of the gateway')


class DescribeGatewayCapabilityConfigurationParams(BaseModel):
    """Parameters for describe_gateway_capability_configuration tool."""
    gatewayId: str = Field(..., description='The ID of the gateway')
    capabilityNamespace: str = Field(..., description='The namespace of the capability')


# Portal and project models
class ListPortalsParams(BaseModel):
    """Parameters for list_portals tool."""
    maxResults: Optional[int] = Field(None, ge=1, le=250, description='Maximum number of results to return')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


class ListDashboardsParams(BaseModel):
    """Parameters for list_dashboards tool."""
    projectId: str = Field(..., description='The ID of the project')
    maxResults: Optional[int] = Field(None, ge=1, le=250, description='Maximum number of results to return')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


class ListProjectsParams(BaseModel):
    """Parameters for list_projects tool."""
    portalId: str = Field(..., description='The ID of the portal')
    maxResults: Optional[int] = Field(None, ge=1, le=250, description='Maximum number of results to return')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


# Time series models
class ListTimeSeriesParams(BaseModel):
    """Parameters for list_time_series tool."""
    assetId: Optional[str] = Field(None, description='Filter by asset ID')
    aliasPrefix: Optional[str] = Field(None, description='Filter by alias prefix')
    timeSeriesType: Optional[TimeSeriesType] = Field(None, description='Filter by time series type')
    maxResults: Optional[int] = Field(None, ge=1, le=250, description='Maximum number of results to return')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


class DescribeTimeSeriesParams(BaseModel):
    """Parameters for describe_time_series tool."""
    alias: Optional[str] = Field(None, description='The alias of the time series')
    assetId: Optional[str] = Field(None, description='The ID of the asset')
    propertyId: Optional[str] = Field(None, description='The ID of the property')


# Access policy models
class ListAccessPoliciesParams(BaseModel):
    """Parameters for list_access_policies tool."""
    identityType: Optional[IdentityType] = Field(None, description='Type of identity')
    identityId: Optional[str] = Field(None, description='ID of the identity')
    resourceType: Optional[ResourceType] = Field(None, description='Type of resource')
    resourceId: Optional[str] = Field(None, description='ID of the resource')
    iamArn: Optional[str] = Field(None, description='ARN of the IAM identity')
    maxResults: Optional[int] = Field(None, ge=1, le=250, description='Maximum number of results to return')
    nextToken: Optional[str] = Field(None, description='Token for pagination')


class ListTagsForResourceParams(BaseModel):
    """Parameters for list_tags_for_resource tool."""
    resourceArn: str = Field(..., description='The ARN of the resource')


# Write operation models
class CreateAssetParams(BaseModel):
    """Parameters for create_asset tool."""
    assetName: str = Field(..., description='Name of the asset')
    assetModelId: str = Field(..., description='ID of the asset model to use')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')
    tags: Optional[Dict[str, str]] = Field(None, description='Tags to apply to the asset')
    assetDescription: Optional[str] = Field(None, description='Description of the asset')
    assetId: Optional[str] = Field(None, description='Custom asset ID (optional)')


class UpdateAssetParams(BaseModel):
    """Parameters for update_asset tool."""
    assetId: str = Field(..., description='ID of the asset to update')
    assetName: str = Field(..., description='New name for the asset')
    assetDescription: Optional[str] = Field(None, description='New description for the asset')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


class DeleteAssetParams(BaseModel):
    """Parameters for delete_asset tool."""
    assetId: str = Field(..., description='ID of the asset to delete')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


class AssociateAssetsParams(BaseModel):
    """Parameters for associate_assets tool."""
    assetId: str = Field(..., description='ID of the parent asset')
    hierarchyId: str = Field(..., description='ID of the hierarchy in the parent asset model')
    childAssetId: str = Field(..., description='ID of the child asset')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


class DisassociateAssetsParams(BaseModel):
    """Parameters for disassociate_assets tool."""
    assetId: str = Field(..., description='ID of the parent asset')
    hierarchyId: str = Field(..., description='ID of the hierarchy in the parent asset model')
    childAssetId: str = Field(..., description='ID of the child asset')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


# Asset model models
class AssetModelProperty(BaseModel):
    """Asset model property definition."""
    name: str = Field(..., description='Name of the property')
    dataType: str = Field(..., description='Data type of the property')
    type: Dict = Field(..., description='Property type configuration')
    unit: Optional[str] = Field(None, description='Unit of measurement')


class AssetModelHierarchy(BaseModel):
    """Asset model hierarchy definition."""
    name: str = Field(..., description='Name of the hierarchy')
    childAssetModelId: str = Field(..., description='ID of the child asset model')


class CreateAssetModelParams(BaseModel):
    """Parameters for create_asset_model tool."""
    assetModelName: str = Field(..., description='Name of the asset model')
    assetModelDescription: Optional[str] = Field(None, description='Description of the asset model')
    assetModelProperties: Optional[List[AssetModelProperty]] = Field(None, description='Properties of the asset model')
    assetModelHierarchies: Optional[List[AssetModelHierarchy]] = Field(None, description='Hierarchies of the asset model')
    assetModelCompositeModels: Optional[List] = Field(None, description='Composite models of the asset model')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')
    tags: Optional[Dict[str, str]] = Field(None, description='Tags to apply to the asset model')
    assetModelId: Optional[str] = Field(None, description='Custom asset model ID (optional)')
    assetModelExternalId: Optional[str] = Field(None, description='External ID for the asset model')


class UpdateAssetModelParams(BaseModel):
    """Parameters for update_asset_model tool."""
    assetModelId: str = Field(..., description='ID of the asset model to update')
    assetModelName: str = Field(..., description='New name for the asset model')
    assetModelDescription: Optional[str] = Field(None, description='New description for the asset model')
    assetModelProperties: Optional[List] = Field(None, description='Updated properties of the asset model')
    assetModelHierarchies: Optional[List] = Field(None, description='Updated hierarchies of the asset model')
    assetModelCompositeModels: Optional[List] = Field(None, description='Updated composite models')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


class DeleteAssetModelParams(BaseModel):
    """Parameters for delete_asset_model tool."""
    assetModelId: str = Field(..., description='ID of the asset model to delete')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


# Data ingestion models
class BatchPutPropertyValueEntry(BaseModel):
    """Entry for batch property value ingestion."""
    entryId: str = Field(..., description='Unique identifier for this entry')
    assetId: Optional[str] = Field(None, description='ID of the asset')
    propertyId: Optional[str] = Field(None, description='ID of the property')
    propertyAlias: Optional[str] = Field(None, description='Alias of the property')
    propertyValues: List[PropertyValueWithTimestamp] = Field(..., description='Property values to send')


class BatchPutAssetPropertyValueParams(BaseModel):
    """Parameters for batch_put_asset_property_value tool."""
    entries: List[BatchPutPropertyValueEntry] = Field(..., max_length=10, description='List of property values to send')


# Gateway management models
class GreengrassConfig(BaseModel):
    """Greengrass v1 configuration."""
    groupArn: str = Field(..., description='ARN of the Greengrass group')


class GreengrassV2Config(BaseModel):
    """Greengrass v2 configuration."""
    coreDeviceThingName: str = Field(..., description='Name of the Greengrass v2 core device')


class GatewayPlatform(BaseModel):
    """Gateway platform configuration."""
    greengrass: Optional[GreengrassConfig] = Field(None, description='Greengrass v1 configuration')
    greengrassV2: Optional[GreengrassV2Config] = Field(None, description='Greengrass v2 configuration')


class CreateGatewayParams(BaseModel):
    """Parameters for create_gateway tool."""
    gatewayName: str = Field(..., description='Name of the gateway')
    gatewayPlatform: GatewayPlatform = Field(..., description='Platform configuration for the gateway')
    tags: Optional[Dict[str, str]] = Field(None, description='Tags to apply to the gateway')


class UpdateGatewayParams(BaseModel):
    """Parameters for update_gateway tool."""
    gatewayId: str = Field(..., description='ID of the gateway to update')
    gatewayName: str = Field(..., description='New name for the gateway')


class DeleteGatewayParams(BaseModel):
    """Parameters for delete_gateway tool."""
    gatewayId: str = Field(..., description='ID of the gateway to delete')


class UpdateGatewayCapabilityConfigurationParams(BaseModel):
    """Parameters for update_gateway_capability_configuration tool."""
    gatewayId: str = Field(..., description='ID of the gateway')
    capabilityNamespace: str = Field(..., description='Namespace of the capability')
    capabilityConfiguration: str = Field(..., description='JSON configuration for the capability')


# Portal management models
class CreatePortalParams(BaseModel):
    """Parameters for create_portal tool."""
    portalName: str = Field(..., description='Name of the portal')
    portalDescription: Optional[str] = Field(None, description='Description of the portal')
    portalContactEmail: str = Field(..., description='Contact email for the portal')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')
    portalLogoImageFile: Optional[Dict] = Field(None, description='Logo image file for the portal')
    roleArn: str = Field(..., description='ARN of the service role for the portal')
    tags: Optional[Dict[str, str]] = Field(None, description='Tags to apply to the portal')
    portalAuthMode: Optional[PortalAuthMode] = Field(None, description='Authentication mode for the portal')


class UpdatePortalParams(BaseModel):
    """Parameters for update_portal tool."""
    portalId: str = Field(..., description='ID of the portal to update')
    portalName: str = Field(..., description='New name for the portal')
    portalDescription: Optional[str] = Field(None, description='New description for the portal')
    portalContactEmail: str = Field(..., description='New contact email for the portal')
    portalLogoImageFile: Optional[Dict] = Field(None, description='New logo image file for the portal')
    roleArn: str = Field(..., description='New ARN of the service role for the portal')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


class DeletePortalParams(BaseModel):
    """Parameters for delete_portal tool."""
    portalId: str = Field(..., description='ID of the portal to delete')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


# Project and dashboard models
class CreateProjectParams(BaseModel):
    """Parameters for create_project tool."""
    portalId: str = Field(..., description='ID of the portal')
    projectName: str = Field(..., description='Name of the project')
    projectDescription: Optional[str] = Field(None, description='Description of the project')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')
    tags: Optional[Dict[str, str]] = Field(None, description='Tags to apply to the project')


class CreateDashboardParams(BaseModel):
    """Parameters for create_dashboard tool."""
    projectId: str = Field(..., description='ID of the project')
    dashboardName: str = Field(..., description='Name of the dashboard')
    dashboardDescription: Optional[str] = Field(None, description='Description of the dashboard')
    dashboardDefinition: str = Field(..., description='JSON definition of the dashboard')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')
    tags: Optional[Dict[str, str]] = Field(None, description='Tags to apply to the dashboard')


class UpdateDashboardParams(BaseModel):
    """Parameters for update_dashboard tool."""
    dashboardId: str = Field(..., description='ID of the dashboard to update')
    dashboardName: str = Field(..., description='New name for the dashboard')
    dashboardDescription: Optional[str] = Field(None, description='New description for the dashboard')
    dashboardDefinition: str = Field(..., description='New JSON definition of the dashboard')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


class DeleteDashboardParams(BaseModel):
    """Parameters for delete_dashboard tool."""
    dashboardId: str = Field(..., description='ID of the dashboard to delete')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


# Access policy models
class AccessPolicyIdentityUser(BaseModel):
    """User identity for access policy."""
    id: str = Field(..., description='User ID')


class AccessPolicyIdentityGroup(BaseModel):
    """Group identity for access policy."""
    id: str = Field(..., description='Group ID')


class AccessPolicyIdentityIamUser(BaseModel):
    """IAM user identity for access policy."""
    arn: str = Field(..., description='IAM user ARN')


class AccessPolicyIdentityIamRole(BaseModel):
    """IAM role identity for access policy."""
    arn: str = Field(..., description='IAM role ARN')


class AccessPolicyIdentity(BaseModel):
    """Identity for access policy."""
    user: Optional[AccessPolicyIdentityUser] = Field(None, description='User identity')
    group: Optional[AccessPolicyIdentityGroup] = Field(None, description='Group identity')
    iamUser: Optional[AccessPolicyIdentityIamUser] = Field(None, description='IAM user identity')
    iamRole: Optional[AccessPolicyIdentityIamRole] = Field(None, description='IAM role identity')


class AccessPolicyResourcePortal(BaseModel):
    """Portal resource for access policy."""
    id: str = Field(..., description='Portal ID')


class AccessPolicyResourceProject(BaseModel):
    """Project resource for access policy."""
    id: str = Field(..., description='Project ID')


class AccessPolicyResource(BaseModel):
    """Resource for access policy."""
    portal: Optional[AccessPolicyResourcePortal] = Field(None, description='Portal resource')
    project: Optional[AccessPolicyResourceProject] = Field(None, description='Project resource')


class CreateAccessPolicyParams(BaseModel):
    """Parameters for create_access_policy tool."""
    accessPolicyIdentity: AccessPolicyIdentity = Field(..., description='Identity for the access policy')
    accessPolicyResource: AccessPolicyResource = Field(..., description='Resource for the access policy')
    accessPolicyPermission: AccessPolicyPermission = Field(..., description='Permission level for the access policy')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')
    tags: Optional[Dict[str, str]] = Field(None, description='Tags to apply to the access policy')


class UpdateAccessPolicyParams(BaseModel):
    """Parameters for update_access_policy tool."""
    accessPolicyId: str = Field(..., description='ID of the access policy to update')
    accessPolicyIdentity: AccessPolicyIdentity = Field(..., description='New identity for the access policy')
    accessPolicyResource: AccessPolicyResource = Field(..., description='New resource for the access policy')
    accessPolicyPermission: AccessPolicyPermission = Field(..., description='New permission level')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


class DeleteAccessPolicyParams(BaseModel):
    """Parameters for delete_access_policy tool."""
    accessPolicyId: str = Field(..., description='ID of the access policy to delete')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


# Time series management models
class AssociateTimeSeriesToAssetPropertyParams(BaseModel):
    """Parameters for associate_time_series_to_asset_property tool."""
    alias: str = Field(..., description='Alias of the time series')
    assetId: str = Field(..., description='ID of the asset')
    propertyId: str = Field(..., description='ID of the property')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


class DisassociateTimeSeriesFromAssetPropertyParams(BaseModel):
    """Parameters for disassociate_time_series_from_asset_property tool."""
    alias: str = Field(..., description='Alias of the time series')
    assetId: str = Field(..., description='ID of the asset')
    propertyId: str = Field(..., description='ID of the property')
    clientToken: Optional[str] = Field(None, description='Unique case-sensitive identifier for the request')


# Resource management models
class TagResourceParams(BaseModel):
    """Parameters for tag_resource tool."""
    resourceArn: str = Field(..., description='ARN of the resource to tag')
    tags: Dict[str, str] = Field(..., description='Tags to add to the resource')


class UntagResourceParams(BaseModel):
    """Parameters for untag_resource tool."""
    resourceArn: str = Field(..., description='ARN of the resource to untag')
    tagKeys: List[str] = Field(..., description='Keys of tags to remove')