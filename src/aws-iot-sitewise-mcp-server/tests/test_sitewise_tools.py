"""Tests for AWS IoT SiteWise MCP tools."""

import os
import pytest
import sys
from botocore.exceptions import ClientError
from unittest.mock import Mock, patch


# Add the project root directory and its parent to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.insert(0, project_dir)
sys.path.insert(0, os.path.dirname(project_dir))
sys.path.insert(0, os.path.dirname(os.path.dirname(project_dir)))

# Import awslabs modules with the updated path
from awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_asset_models import create_asset_model
from awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_assets import create_asset, describe_asset
from awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_data import (
    batch_put_asset_property_value,
    get_asset_property_value,
)


class TestSiteWiseAssets:
    """Test cases for SiteWise asset management tools."""

    @patch('awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_assets.boto3.client')
    def test_create_asset_success(self, mock_boto_client):
        """Test successful asset creation."""
        # Mock the boto3 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client

        # Mock the response
        mock_response = {
            'assetId': 'test-asset-123',
            'assetArn': 'arn:aws:iotsitewise:us-east-1:123456789012:asset/test-asset-123',
            'assetStatus': {'state': 'CREATING'},
        }
        mock_client.create_asset.return_value = mock_response

        # Call the function
        result = create_asset(
            asset_name='Test Asset', asset_model_id='test-model-456', region='us-east-1'
        )

        # Verify the result
        assert result['success'] is True
        assert result['asset_id'] == 'test-asset-123'
        assert (
            result['asset_arn']
            == 'arn:aws:iotsitewise:us-east-1:123456789012:asset/test-asset-123'
        )

        # Verify the client was called correctly
        mock_client.create_asset.assert_called_once_with(
            assetName='Test Asset', assetModelId='test-model-456'
        )

    @patch('awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_assets.boto3.client')
    def test_create_asset_failure(self, mock_boto_client):
        """Test asset creation failure."""
        # Mock the boto3 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client

        # Mock a ClientError
        error_response = {
            'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Asset model not found'}
        }
        mock_client.create_asset.side_effect = ClientError(error_response, 'CreateAsset')

        # Call the function
        result = create_asset(
            asset_name='Test Asset', asset_model_id='nonexistent-model', region='us-east-1'
        )

        # Verify the result
        assert result['success'] is False
        assert result['error_code'] == 'ResourceNotFoundException'
        assert 'Asset model not found' in result['error']

    @patch('awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_assets.boto3.client')
    def test_describe_asset_success(self, mock_boto_client):
        """Test successful asset description."""
        # Mock the boto3 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client

        # Mock the response
        mock_response = {
            'assetId': 'test-asset-123',
            'assetArn': 'arn:aws:iotsitewise:us-east-1:123456789012:asset/test-asset-123',
            'assetName': 'Test Asset',
            'assetModelId': 'test-model-456',
            'assetProperties': [],
            'assetHierarchies': [],
            'assetCompositeModels': [],
            'assetStatus': {'state': 'ACTIVE'},
            'assetCreationDate': Mock(),
            'assetLastUpdateDate': Mock(),
            'assetDescription': 'Test asset description',
        }
        mock_response['assetCreationDate'].isoformat.return_value = '2023-01-01T00:00:00Z'
        mock_response['assetLastUpdateDate'].isoformat.return_value = '2023-01-01T00:00:00Z'
        mock_client.describe_asset.return_value = mock_response

        # Call the function
        result = describe_asset(asset_id='test-asset-123', region='us-east-1')

        # Verify the result
        assert result['success'] is True
        assert result['asset_id'] == 'test-asset-123'
        assert result['asset_name'] == 'Test Asset'
        assert result['asset_model_id'] == 'test-model-456'


class TestSiteWiseAssetModels:
    """Test cases for SiteWise asset model management tools."""

    @patch('awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_asset_models.boto3.client')
    def test_create_asset_model_success(self, mock_boto_client):
        """Test successful asset model creation."""
        # Mock the boto3 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client

        # Mock the response
        mock_response = {
            'assetModelId': 'test-model-123',
            'assetModelArn': 'arn:aws:iotsitewise:us-east-1:123456789012:asset-model/test-model-123',
            'assetModelStatus': {'state': 'CREATING'},
        }
        mock_client.create_asset_model.return_value = mock_response

        # Call the function
        result = create_asset_model(asset_model_name='Test Model', region='us-east-1')

        # Verify the result
        assert result['success'] is True
        assert result['asset_model_id'] == 'test-model-123'
        assert (
            result['asset_model_arn']
            == 'arn:aws:iotsitewise:us-east-1:123456789012:asset-model/test-model-123'
        )


class TestSiteWiseData:
    """Test cases for SiteWise data ingestion and retrieval tools."""

    @patch('awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_data.boto3.client')
    def test_batch_put_asset_property_value_success(self, mock_boto_client):
        """Test successful batch data ingestion."""
        # Mock the boto3 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client

        # Mock the response
        mock_response = {'errorEntries': []}
        mock_client.batch_put_asset_property_value.return_value = mock_response

        # Test data
        entries = [
            {
                'entryId': 'entry1',
                'assetId': 'test-asset-123',
                'propertyId': 'test-property-456',
                'propertyValues': [
                    {
                        'value': {'doubleValue': 25.5},
                        'timestamp': {'timeInSeconds': 1640995200},
                        'quality': 'GOOD',
                    }
                ],
            }
        ]

        # Call the function
        result = batch_put_asset_property_value(entries=entries, region='us-east-1')

        # Verify the result
        assert result['success'] is True
        assert result['error_entries'] == []

        # Verify the client was called correctly
        mock_client.batch_put_asset_property_value.assert_called_once_with(entries=entries)

    @patch('awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_data.boto3.client')
    def test_get_asset_property_value_success(self, mock_boto_client):
        """Test successful property value retrieval."""
        # Mock the boto3 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client

        # Mock the response
        mock_response = {
            'propertyValue': {
                'value': {'doubleValue': 25.5},
                'timestamp': {'timeInSeconds': 1640995200},
                'quality': 'GOOD',
            }
        }
        mock_client.get_asset_property_value.return_value = mock_response

        # Call the function
        result = get_asset_property_value(
            asset_id='test-asset-123', property_id='test-property-456', region='us-east-1'
        )

        # Verify the result
        assert result['success'] is True
        assert result['value']['doubleValue'] == 25.5
        assert result['quality'] == 'GOOD'


class TestErrorHandling:
    """Test cases for error handling across all tools."""

    @patch('awslabs.aws_iot_sitewise_mcp_server.tools.sitewise_assets.boto3.client')
    def test_client_error_handling(self, mock_boto_client):
        """Test that ClientError exceptions are properly handled."""
        # Mock the boto3 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client

        # Mock various types of errors
        error_cases = [
            ('ResourceNotFoundException', 'Resource not found'),
            ('InvalidRequestException', 'Invalid request'),
            ('ThrottlingException', 'Request throttled'),
            ('InternalFailureException', 'Internal server error'),
        ]

        for error_code, error_message in error_cases:
            error_response = {'Error': {'Code': error_code, 'Message': error_message}}
            mock_client.create_asset.side_effect = ClientError(error_response, 'CreateAsset')

            # Call the function
            result = create_asset(
                asset_name='Test Asset', asset_model_id='test-model', region='us-east-1'
            )

            # Verify error handling
            assert result['success'] is False
            assert result['error_code'] == error_code
            assert error_message in result['error']


if __name__ == '__main__':
    pytest.main([__file__])
