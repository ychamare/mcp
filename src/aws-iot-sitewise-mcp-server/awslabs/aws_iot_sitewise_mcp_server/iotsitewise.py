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

"""AWS IoT SiteWise service client for MCP server."""

import asyncio
import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from loguru import logger

from .consts import AWS_SERVICE_NAME


class IoTSiteWiseService:
    """AWS IoT SiteWise service client wrapper with async support and error handling."""

    def __init__(self):
        """Initialize the IoT SiteWise service client."""
        self.aws_region = os.environ.get('AWS_REGION', 'us-west-2')
        self.aws_profile = os.environ.get('AWS_PROFILE')
        self._client = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the boto3 IoT SiteWise client."""
        try:
            if self.aws_profile:
                logger.info(f'Creating IoT SiteWise client with profile: {self.aws_profile}')
                session = boto3.Session(profile_name=self.aws_profile, region_name=self.aws_region)
                self._client = session.client(AWS_SERVICE_NAME)
            else:
                logger.info(f'Creating IoT SiteWise client with default credentials in region: {self.aws_region}')
                self._client = boto3.client(AWS_SERVICE_NAME, region_name=self.aws_region)
            
            logger.info('IoT SiteWise client initialized successfully')
        except NoCredentialsError as e:
            logger.error(f'AWS credentials not found: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Error creating IoT SiteWise client: {str(e)}')
            raise

    async def _execute_operation(self, operation_name: str, **kwargs) -> Dict[str, Any]:
        """Execute an IoT SiteWise operation asynchronously with error handling.
        
        Args:
            operation_name: Name of the boto3 operation to execute
            **kwargs: Arguments to pass to the operation
            
        Returns:
            Dict containing the operation response
            
        Raises:
            Exception: If the operation fails
        """
        try:
            logger.debug(f'Executing {operation_name} with args: {kwargs}')
            
            # Remove None values from kwargs to avoid boto3 errors
            cleaned_kwargs = {k: v for k, v in kwargs.items() if v is not None}
            
            # Execute the operation in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            operation = getattr(self._client, operation_name)
            response = await loop.run_in_executor(None, lambda: operation(**cleaned_kwargs))
            
            logger.debug(f'{operation_name} completed successfully')
            return response
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'UnknownError')
            error_message = e.response.get('Error', {}).get('Message', str(e))
            logger.error(f'{operation_name} failed with {error_code}: {error_message}')
            raise Exception(f'AWS IoT SiteWise {operation_name} failed: {error_message}')
        except Exception as e:
            logger.error(f'{operation_name} failed with unexpected error: {str(e)}')
            raise Exception(f'Failed to execute {operation_name}: {str(e)}')

    # Read-only operations
    async def list_asset_models(self, max_results: Optional[int] = None, next_token: Optional[str] = None) -> str:
        """List all asset models in IoT SiteWise."""
        kwargs = {}
        if max_results is not None:
            kwargs['maxResults'] = max_results
        if next_token:
            kwargs['nextToken'] = next_token
            
        response = await self._execute_operation('list_asset_models', **kwargs)
        return json.dumps(response, default=str)

    async def describe_asset_model(self, asset_model_id: str) -> str:
        """Get detailed information about a specific asset model."""
        response = await self._execute_operation('describe_asset_model', assetModelId=asset_model_id)
        return json.dumps(response, default=str)

    async def list_assets(self, asset_model_id: Optional[str] = None, max_results: Optional[int] = None, next_token: Optional[str] = None) -> str:
        """List assets, optionally filtered by asset model."""
        kwargs = {}
        if asset_model_id:
            kwargs['assetModelId'] = asset_model_id
        if max_results is not None:
            kwargs['maxResults'] = max_results
        if next_token:
            kwargs['nextToken'] = next_token
            
        response = await self._execute_operation('list_assets', **kwargs)
        return json.dumps(response, default=str)

    async def describe_asset(self, asset_id: str) -> str:
        """Get detailed information about a specific asset."""
        response = await self._execute_operation('describe_asset', assetId=asset_id)
        return json.dumps(response, default=str)

    async def get_asset_property_value(self, asset_id: str, property_id: Optional[str] = None, property_alias: Optional[str] = None) -> str:
        """Get the current value of an asset property."""
        kwargs = {'assetId': asset_id}
        if property_id:
            kwargs['propertyId'] = property_id
        if property_alias:
            kwargs['propertyAlias'] = property_alias
            
        response = await self._execute_operation('get_asset_property_value', **kwargs)
        return json.dumps(response, default=str)

    async def get_asset_property_value_history(self, asset_id: str, property_id: Optional[str] = None, property_alias: Optional[str] = None, **kwargs) -> str:
        """Get historical values for an asset property."""
        params = {'assetId': asset_id}
        if property_id:
            params['propertyId'] = property_id
        if property_alias:
            params['propertyAlias'] = property_alias
        params.update(kwargs)
        
        response = await self._execute_operation('get_asset_property_value_history', **params)
        return json.dumps(response, default=str)

    async def get_asset_property_aggregates(self, asset_id: str, property_id: Optional[str] = None, property_alias: Optional[str] = None, **kwargs) -> str:
        """Get aggregated values for an asset property."""
        params = {'assetId': asset_id}
        if property_id:
            params['propertyId'] = property_id
        if property_alias:
            params['propertyAlias'] = property_alias
        params.update(kwargs)
        
        response = await self._execute_operation('get_asset_property_aggregates', **params)
        return json.dumps(response, default=str)

    async def list_associated_assets(self, asset_id: str, **kwargs) -> str:
        """List assets associated with a parent asset."""
        params = {'assetId': asset_id}
        params.update(kwargs)
        
        response = await self._execute_operation('list_associated_assets', **params)
        return json.dumps(response, default=str)

    async def batch_get_asset_property_value(self, entries: list) -> str:
        """Get current values for multiple asset properties in a single request."""
        response = await self._execute_operation('batch_get_asset_property_value', entries=entries)
        return json.dumps(response, default=str)

    async def batch_get_asset_property_value_history(self, entries: list, **kwargs) -> str:
        """Get historical values for multiple asset properties in a single request."""
        params = {'entries': entries}
        params.update(kwargs)
        
        response = await self._execute_operation('batch_get_asset_property_value_history', **params)
        return json.dumps(response, default=str)

    async def batch_get_asset_property_aggregates(self, entries: list, **kwargs) -> str:
        """Get aggregated values for multiple asset properties in a single request."""
        params = {'entries': entries}
        params.update(kwargs)
        
        response = await self._execute_operation('batch_get_asset_property_aggregates', **params)
        return json.dumps(response, default=str)

    async def get_interpolated_asset_property_values(self, **kwargs) -> str:
        """Get interpolated values for an asset property over a time range."""
        response = await self._execute_operation('get_interpolated_asset_property_values', **kwargs)
        return json.dumps(response, default=str)

    async def list_gateways(self, max_results: Optional[int] = None, next_token: Optional[str] = None) -> str:
        """List all IoT SiteWise gateways."""
        kwargs = {}
        if max_results is not None:
            kwargs['maxResults'] = max_results
        if next_token:
            kwargs['nextToken'] = next_token
            
        response = await self._execute_operation('list_gateways', **kwargs)
        return json.dumps(response, default=str)

    async def describe_gateway(self, gateway_id: str) -> str:
        """Get detailed information about a specific gateway."""
        response = await self._execute_operation('describe_gateway', gatewayId=gateway_id)
        return json.dumps(response, default=str)

    async def describe_gateway_capability_configuration(self, gateway_id: str, capability_namespace: str) -> str:
        """Get the capability configuration for a gateway."""
        response = await self._execute_operation(
            'describe_gateway_capability_configuration',
            gatewayId=gateway_id,
            capabilityNamespace=capability_namespace
        )
        return json.dumps(response, default=str)

    async def list_portals(self, max_results: Optional[int] = None, next_token: Optional[str] = None) -> str:
        """List all IoT SiteWise Monitor portals."""
        kwargs = {}
        if max_results is not None:
            kwargs['maxResults'] = max_results
        if next_token:
            kwargs['nextToken'] = next_token
            
        response = await self._execute_operation('list_portals', **kwargs)
        return json.dumps(response, default=str)

    async def list_dashboards(self, project_id: str, max_results: Optional[int] = None, next_token: Optional[str] = None) -> str:
        """List dashboards in a project."""
        kwargs = {'projectId': project_id}
        if max_results is not None:
            kwargs['maxResults'] = max_results
        if next_token:
            kwargs['nextToken'] = next_token
            
        response = await self._execute_operation('list_dashboards', **kwargs)
        return json.dumps(response, default=str)

    async def list_projects(self, portal_id: str, max_results: Optional[int] = None, next_token: Optional[str] = None) -> str:
        """List projects in a portal."""
        kwargs = {'portalId': portal_id}
        if max_results is not None:
            kwargs['maxResults'] = max_results
        if next_token:
            kwargs['nextToken'] = next_token
            
        response = await self._execute_operation('list_projects', **kwargs)
        return json.dumps(response, default=str)

    async def list_time_series(self, **kwargs) -> str:
        """List time series in your account."""
        response = await self._execute_operation('list_time_series', **kwargs)
        return json.dumps(response, default=str)

    async def describe_time_series(self, **kwargs) -> str:
        """Get detailed information about a time series."""
        response = await self._execute_operation('describe_time_series', **kwargs)
        return json.dumps(response, default=str)

    async def list_access_policies(self, **kwargs) -> str:
        """List access policies for IoT SiteWise Monitor."""
        response = await self._execute_operation('list_access_policies', **kwargs)
        return json.dumps(response, default=str)

    async def list_tags_for_resource(self, resource_arn: str) -> str:
        """List tags for a resource."""
        response = await self._execute_operation('list_tags_for_resource', resourceArn=resource_arn)
        return json.dumps(response, default=str)

    # Write operations
    async def create_asset(self, **kwargs) -> str:
        """Create a new asset from an asset model."""
        response = await self._execute_operation('create_asset', **kwargs)
        return json.dumps(response, default=str)

    async def update_asset(self, **kwargs) -> str:
        """Update an existing asset."""
        response = await self._execute_operation('update_asset', **kwargs)
        return json.dumps(response, default=str)

    async def delete_asset(self, **kwargs) -> str:
        """Delete an asset permanently."""
        response = await self._execute_operation('delete_asset', **kwargs)
        return json.dumps(response, default=str)

    async def associate_assets(self, **kwargs) -> str:
        """Associate a child asset with a parent asset."""
        response = await self._execute_operation('associate_assets', **kwargs)
        return json.dumps(response, default=str)

    async def disassociate_assets(self, **kwargs) -> str:
        """Remove association between parent and child assets."""
        response = await self._execute_operation('disassociate_assets', **kwargs)
        return json.dumps(response, default=str)

    async def create_asset_model(self, **kwargs) -> str:
        """Create a new asset model."""
        response = await self._execute_operation('create_asset_model', **kwargs)
        return json.dumps(response, default=str)

    async def update_asset_model(self, **kwargs) -> str:
        """Update an existing asset model."""
        response = await self._execute_operation('update_asset_model', **kwargs)
        return json.dumps(response, default=str)

    async def delete_asset_model(self, **kwargs) -> str:
        """Delete an asset model permanently."""
        response = await self._execute_operation('delete_asset_model', **kwargs)
        return json.dumps(response, default=str)

    async def batch_put_asset_property_value(self, entries: list) -> str:
        """Send property values to IoT SiteWise."""
        response = await self._execute_operation('batch_put_asset_property_value', entries=entries)
        return json.dumps(response, default=str)

    async def create_gateway(self, **kwargs) -> str:
        """Create a new IoT SiteWise gateway."""
        response = await self._execute_operation('create_gateway', **kwargs)
        return json.dumps(response, default=str)

    async def update_gateway(self, **kwargs) -> str:
        """Update an existing gateway."""
        response = await self._execute_operation('update_gateway', **kwargs)
        return json.dumps(response, default=str)

    async def delete_gateway(self, **kwargs) -> str:
        """Delete a gateway permanently."""
        response = await self._execute_operation('delete_gateway', **kwargs)
        return json.dumps(response, default=str)

    async def update_gateway_capability_configuration(self, **kwargs) -> str:
        """Update gateway capability configuration."""
        response = await self._execute_operation('update_gateway_capability_configuration', **kwargs)
        return json.dumps(response, default=str)

    async def create_portal(self, **kwargs) -> str:
        """Create a new IoT SiteWise Monitor portal."""
        response = await self._execute_operation('create_portal', **kwargs)
        return json.dumps(response, default=str)

    async def update_portal(self, **kwargs) -> str:
        """Update an existing portal."""
        response = await self._execute_operation('update_portal', **kwargs)
        return json.dumps(response, default=str)

    async def delete_portal(self, **kwargs) -> str:
        """Delete a portal permanently."""
        response = await self._execute_operation('delete_portal', **kwargs)
        return json.dumps(response, default=str)

    async def create_project(self, **kwargs) -> str:
        """Create a new project in a portal."""
        response = await self._execute_operation('create_project', **kwargs)
        return json.dumps(response, default=str)

    async def create_dashboard(self, **kwargs) -> str:
        """Create a new dashboard in a project."""
        response = await self._execute_operation('create_dashboard', **kwargs)
        return json.dumps(response, default=str)

    async def update_dashboard(self, **kwargs) -> str:
        """Update an existing dashboard."""
        response = await self._execute_operation('update_dashboard', **kwargs)
        return json.dumps(response, default=str)

    async def delete_dashboard(self, **kwargs) -> str:
        """Delete a dashboard permanently."""
        response = await self._execute_operation('delete_dashboard', **kwargs)
        return json.dumps(response, default=str)

    async def create_access_policy(self, **kwargs) -> str:
        """Create an access policy for IoT SiteWise Monitor."""
        response = await self._execute_operation('create_access_policy', **kwargs)
        return json.dumps(response, default=str)

    async def update_access_policy(self, **kwargs) -> str:
        """Update an existing access policy."""
        response = await self._execute_operation('update_access_policy', **kwargs)
        return json.dumps(response, default=str)

    async def delete_access_policy(self, **kwargs) -> str:
        """Delete an access policy permanently."""
        response = await self._execute_operation('delete_access_policy', **kwargs)
        return json.dumps(response, default=str)

    async def associate_time_series_to_asset_property(self, **kwargs) -> str:
        """Associate a time series with an asset property."""
        response = await self._execute_operation('associate_time_series_to_asset_property', **kwargs)
        return json.dumps(response, default=str)

    async def disassociate_time_series_from_asset_property(self, **kwargs) -> str:
        """Remove association between time series and asset property."""
        response = await self._execute_operation('disassociate_time_series_from_asset_property', **kwargs)
        return json.dumps(response, default=str)

    async def tag_resource(self, resource_arn: str, tags: dict) -> str:
        """Add tags to a resource."""
        response = await self._execute_operation('tag_resource', resourceArn=resource_arn, tags=tags)
        return json.dumps(response, default=str)

    async def untag_resource(self, resource_arn: str, tag_keys: list) -> str:
        """Remove tags from a resource."""
        response = await self._execute_operation('untag_resource', resourceArn=resource_arn, tagKeys=tag_keys)
        return json.dumps(response, default=str)