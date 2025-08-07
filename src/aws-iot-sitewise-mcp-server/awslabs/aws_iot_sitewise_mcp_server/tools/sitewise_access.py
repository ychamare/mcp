"""AWS IoT SiteWise Access Policies and Configuration Management Tools."""

import boto3
from botocore.exceptions import ClientError
from mcp.server.fastmcp.tools import Tool
from typing import Any, Dict, Optional


def create_access_policy(
    access_policy_identity: Dict[str, Any],
    access_policy_resource: Dict[str, Any],
    access_policy_permission: str,
    region: str = 'us-east-1',
    client_token: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """From typing import Any, Dict, Optional
        Create an access policy that grants the specified identity the specified AWS IoT SiteWise Monitor permissions.

    Args:
            access_policy_identity: The identity for this access policy (user, group, or IAM role)
            access_policy_resource: The AWS IoT SiteWise Monitor resource for this access policy
            access_policy_permission: The permission level for this access policy (ADMINISTRATOR, VIEWER)
            region: AWS region (default: us-east-1)
            client_token: A unique case-sensitive identifier for the request
            tags: A list of key-value pairs that contain metadata for the access policy

    Returns:
            Dictionary containing access policy creation response
    """
    try:
        client = boto3.client('iotsitewise', region_name=region)

        params: Dict[str, Any] = {
            'accessPolicyIdentity': access_policy_identity,
            'accessPolicyResource': access_policy_resource,
            'accessPolicyPermission': access_policy_permission,
        }

        if client_token:
            params['clientToken'] = client_token
        if tags:
            params['tags'] = tags

        response = client.create_access_policy(**params)
        return {
            'success': True,
            'access_policy_id': response['accessPolicyId'],
            'access_policy_arn': response['accessPolicyArn'],
        }

    except ClientError as e:
        return {'success': False, 'error': str(e), 'error_code': e.response['Error']['Code']}


def describe_access_policy(access_policy_id: str, region: str = 'us-east-1') -> Dict[str, Any]:
    """Describe an access policy.

    Args:
        access_policy_id: The ID of the access policy
        region: AWS region (default: us-east-1)

    Returns:
        Dictionary containing access policy information
    """
    try:
        client = boto3.client('iotsitewise', region_name=region)

        response = client.describe_access_policy(accessPolicyId=access_policy_id)

        return {
            'success': True,
            'access_policy_id': response['accessPolicyId'],
            'access_policy_arn': response['accessPolicyArn'],
            'access_policy_identity': response['accessPolicyIdentity'],
            'access_policy_resource': response['accessPolicyResource'],
            'access_policy_permission': response['accessPolicyPermission'],
            'access_policy_creation_date': response['accessPolicyCreationDate'].isoformat(),
            'access_policy_last_update_date': response['accessPolicyLastUpdateDate'].isoformat(),
        }

    except ClientError as e:
        return {'success': False, 'error': str(e), 'error_code': e.response['Error']['Code']}


def list_access_policies(
    region: str = 'us-east-1',
    identity_type: Optional[str] = None,
    identity_id: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    iam_arn: Optional[str] = None,
    next_token: Optional[str] = None,
    max_results: int = 50,
) -> Dict[str, Any]:
    """Retrieve a paginated list of access policies for an AWS IoT SiteWise Monitor portal or project.

    Args:
        region: AWS region (default: us-east-1)
        identity_type: The type of identity (USER, GROUP, IAM)
        identity_id: The ID of the identity
        resource_type: The type of resource (PORTAL, PROJECT)
        resource_id: The ID of the resource
        iam_arn: The ARN of the IAM role
        next_token: The token to be used for the next set of paginated results
        max_results: The maximum number of results to return (1-250, default: 50)

    Returns:
        Dictionary containing list of access policies
    """
    try:
        client = boto3.client('iotsitewise', region_name=region)

        params: Dict[str, Any] = {'maxResults': max_results}

        if identity_type:
            params['identityType'] = identity_type
        if identity_id:
            params['identityId'] = identity_id
        if resource_type:
            params['resourceType'] = resource_type
        if resource_id:
            params['resourceId'] = resource_id
        if iam_arn:
            params['iamArn'] = iam_arn
        if next_token:
            params['nextToken'] = next_token

        response = client.list_access_policies(**params)

        return {
            'success': True,
            'access_policy_summaries': response['accessPolicySummaries'],
            'next_token': response.get('nextToken', ''),
        }

    except ClientError as e:
        return {'success': False, 'error': str(e), 'error_code': e.response['Error']['Code']}


def update_access_policy(
    access_policy_id: str,
    access_policy_identity: Dict[str, Any],
    access_policy_resource: Dict[str, Any],
    access_policy_permission: str,
    region: str = 'us-east-1',
    client_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an access policy.

    Args:
        access_policy_id: The ID of the access policy
        access_policy_identity: The identity for this access policy
        access_policy_resource: The AWS IoT SiteWise Monitor resource for this access policy
        access_policy_permission: The permission level for this access policy
        region: AWS region (default: us-east-1)
        client_token: A unique case-sensitive identifier for the request

    Returns:
        Dictionary containing update response
    """
    try:
        client = boto3.client('iotsitewise', region_name=region)

        params: Dict[str, Any] = {
            'accessPolicyId': access_policy_id,
            'accessPolicyIdentity': access_policy_identity,
            'accessPolicyResource': access_policy_resource,
            'accessPolicyPermission': access_policy_permission,
        }

        if client_token:
            params['clientToken'] = client_token

        client.update_access_policy(**params)
        return {'success': True, 'message': 'Access policy updated successfully'}

    except ClientError as e:
        return {'success': False, 'error': str(e), 'error_code': e.response['Error']['Code']}


def delete_access_policy(
    access_policy_id: str, region: str = 'us-east-1', client_token: Optional[str] = None
) -> Dict[str, Any]:
    """Delete an access policy.

    Args:
        access_policy_id: The ID of the access policy to be deleted
        region: AWS region (default: us-east-1)
        client_token: A unique case-sensitive identifier for the request

    Returns:
        Dictionary containing deletion response
    """
    try:
        client = boto3.client('iotsitewise', region_name=region)

        params: Dict[str, Any] = {'accessPolicyId': access_policy_id}
        if client_token:
            params['clientToken'] = client_token

        client.delete_access_policy(**params)
        return {'success': True, 'message': 'Access policy deleted successfully'}

    except ClientError as e:
        return {'success': False, 'error': str(e), 'error_code': e.response['Error']['Code']}


def describe_default_encryption_configuration(region: str = 'us-east-1') -> Dict[str, Any]:
    """Retrieve information about the default encryption configuration for your AWS account.

    Args:
        region: AWS region (default: us-east-1)

    Returns:
        Dictionary containing default encryption configuration
    """
    try:
        client = boto3.client('iotsitewise', region_name=region)

        response = client.describe_default_encryption_configuration()

        return {
            'success': True,
            'encryption_type': response['encryptionType'],
            'kms_key_id': response.get('kmsKeyId', ''),
            'configuration_status': response['configurationStatus'],
        }

    except ClientError as e:
        return {'success': False, 'error': str(e), 'error_code': e.response['Error']['Code']}


def put_default_encryption_configuration(
    encryption_type: str, region: str = 'us-east-1', kms_key_id: Optional[str] = None
) -> Dict[str, Any]:
    """Set the default encryption configuration for your AWS account.

    Args:
        encryption_type: The type of encryption used for the encryption configuration (SITEWISE_DEFAULT_ENCRYPTION, KMS_BASED_ENCRYPTION)
        region: AWS region (default: us-east-1)
        kms_key_id: The Key ID of the customer managed key used for KMS encryption

    Returns:
        Dictionary containing encryption configuration response
    """
    try:
        client = boto3.client('iotsitewise', region_name=region)

        params: Dict[str, Any] = {'encryptionType': encryption_type}
        if kms_key_id:
            params['kmsKeyId'] = kms_key_id

        response = client.put_default_encryption_configuration(**params)

        return {
            'success': True,
            'encryption_type': response['encryptionType'],
            'kms_key_id': response.get('kmsKeyId', ''),
            'configuration_status': response['configurationStatus'],
        }

    except ClientError as e:
        return {'success': False, 'error': str(e), 'error_code': e.response['Error']['Code']}


def describe_logging_options(region: str = 'us-east-1') -> Dict[str, Any]:
    """Retrieve the current AWS IoT SiteWise logging options.

    Args:
        region: AWS region (default: us-east-1)

    Returns:
        Dictionary containing logging options
    """
    try:
        client = boto3.client('iotsitewise', region_name=region)

        response = client.describe_logging_options()

        return {'success': True, 'logging_options': response['loggingOptions']}

    except ClientError as e:
        return {'success': False, 'error': str(e), 'error_code': e.response['Error']['Code']}


def put_logging_options(
    logging_options: Dict[str, Any], region: str = 'us-east-1'
) -> Dict[str, Any]:
    """Set logging options for AWS IoT SiteWise.

    Args:
        logging_options: The logging options to set
        region: AWS region (default: us-east-1)

    Returns:
        Dictionary containing logging options response
    """
    try:
        client = boto3.client('iotsitewise', region_name=region)

        client.put_logging_options(loggingOptions=logging_options)
        return {'success': True, 'message': 'Logging options updated successfully'}

    except ClientError as e:
        return {'success': False, 'error': str(e), 'error_code': e.response['Error']['Code']}


def describe_storage_configuration(region: str = 'us-east-1') -> Dict[str, Any]:
    """Retrieve information about the storage configuration for your AWS account.

    Args:
        region: AWS region (default: us-east-1)

    Returns:
        Dictionary containing storage configuration
    """
    try:
        client = boto3.client('iotsitewise', region_name=region)

        response = client.describe_storage_configuration()

        return {
            'success': True,
            'storage_type': response['storageType'],
            'multi_layer_storage': response.get('multiLayerStorage', {}),
            'disassociated_data_storage': response.get('disassociatedDataStorage', 'ENABLED'),
            'retention_period': response.get('retentionPeriod', {}),
            'configuration_status': response['configurationStatus'],
            'last_update_date': (
                response.get('lastUpdateDate', '').isoformat()
                if response.get('lastUpdateDate')
                else ''
            ),
        }

    except ClientError as e:
        return {'success': False, 'error': str(e), 'error_code': e.response['Error']['Code']}


def put_storage_configuration(
    storage_type: str,
    region: str = 'us-east-1',
    multi_layer_storage: Optional[Dict[str, Any]] = None,
    disassociated_data_storage: str = 'ENABLED',
    retention_period: Optional[Dict[str, Any]] = None,
    warm_tier: str = 'ENABLED',
    warm_tier_retention_period: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Configure storage settings for AWS IoT SiteWise.

    Args:
        storage_type: The storage tier that you specified for your data (SITEWISE_DEFAULT_STORAGE, MULTI_LAYER_STORAGE)
        region: AWS region (default: us-east-1)
        multi_layer_storage: Identifies a storage destination
        disassociated_data_storage: Contains the storage configuration for time series data that isn't associated with asset properties
        retention_period: How many days your data is kept in the hot tier
        warm_tier: A service managed storage tier optimized for analytical queries (ENABLED, DISABLED)
        warm_tier_retention_period: Set this period to specify how long your data is stored in the warm tier

    Returns:
        Dictionary containing storage configuration response
    """
    try:
        client = boto3.client('iotsitewise', region_name=region)

        params: Dict[str, Any] = {
            'storageType': storage_type,
            'disassociatedDataStorage': disassociated_data_storage,
            'warmTier': warm_tier,
        }

        if multi_layer_storage:
            params['multiLayerStorage'] = multi_layer_storage
        if retention_period:
            params['retentionPeriod'] = retention_period
        if warm_tier_retention_period:
            params['warmTierRetentionPeriod'] = warm_tier_retention_period

        response = client.put_storage_configuration(**params)

        return {
            'success': True,
            'storage_type': response['storageType'],
            'multi_layer_storage': response.get('multiLayerStorage', {}),
            'disassociated_data_storage': response.get('disassociatedDataStorage', 'ENABLED'),
            'retention_period': response.get('retentionPeriod', {}),
            'configuration_status': response['configurationStatus'],
            'warm_tier': response.get('warmTier', 'ENABLED'),
            'warm_tier_retention_period': response.get('warmTierRetentionPeriod', {}),
        }

    except ClientError as e:
        return {'success': False, 'error': str(e), 'error_code': e.response['Error']['Code']}


# Create MCP tools
create_access_policy_tool = Tool.from_function(
    fn=create_access_policy,
    name='create_access_policy',
    description='Create an access policy that grants specified permissions to AWS IoT SiteWise Monitor resources.',
)

describe_access_policy_tool = Tool.from_function(
    fn=describe_access_policy,
    name='describe_access_policy',
    description='Retrieve detailed information about an AWS IoT SiteWise access policy.',
)

list_access_policies_tool = Tool.from_function(
    fn=list_access_policies,
    name='list_access_policies',
    description='Retrieve a paginated list of access policies for AWS IoT SiteWise Monitor resources.',
)

update_access_policy_tool = Tool.from_function(
    fn=update_access_policy,
    name='update_access_policy',
    description='Update an AWS IoT SiteWise access policy.',
)

delete_access_policy_tool = Tool.from_function(
    fn=delete_access_policy,
    name='delete_access_policy',
    description='Delete an AWS IoT SiteWise access policy.',
)

describe_default_encryption_configuration_tool = Tool.from_function(
    fn=describe_default_encryption_configuration,
    name='describe_default_encryption_config',
    description='Retrieve information about the default encryption configuration for AWS IoT SiteWise.',
)

put_default_encryption_configuration_tool = Tool.from_function(
    fn=put_default_encryption_configuration,
    name='put_default_encryption_configuration',
    description='Set the default encryption configuration for AWS IoT SiteWise.',
)

describe_logging_options_tool = Tool.from_function(
    fn=describe_logging_options,
    name='describe_logging_options',
    description='Retrieve the current AWS IoT SiteWise logging options.',
)

put_logging_options_tool = Tool.from_function(
    fn=put_logging_options,
    name='put_logging_options',
    description='Set logging options for AWS IoT SiteWise.',
)

describe_storage_configuration_tool = Tool.from_function(
    fn=describe_storage_configuration,
    name='describe_storage_configuration',
    description='Retrieve information about the storage configuration for AWS IoT SiteWise.',
)

put_storage_configuration_tool = Tool.from_function(
    fn=put_storage_configuration,
    name='put_storage_configuration',
    description='Configure storage settings for AWS IoT SiteWise including multi-layer storage and retention policies.',
)
