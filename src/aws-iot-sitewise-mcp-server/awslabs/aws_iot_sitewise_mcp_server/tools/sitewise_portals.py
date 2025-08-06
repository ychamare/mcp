"""AWS IoT SiteWise Portals, Projects, and Dashboards Management Tools."""

from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError
from mcp.server.fastmcp.tools import Tool


def create_portal(
    portal_name: str,
    portal_contact_email: str,
    region: str = "us-east-1",
    portal_description: Optional[str] = None,
    client_token: Optional[str] = None,
    portal_logo_image_file: Optional[Dict[str, Any]] = None,
    role_arn: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    portal_auth_mode: str = "IAM",
    notification_sender_email: Optional[str] = None,
    alarms: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    from typing import Any, Dict, Optional
        Create a portal in AWS IoT SiteWise Monitor.

        Args:
            portal_name: A friendly name for the portal
            portal_contact_email: The AWS administrator's contact email address
            region: AWS region (default: us-east-1)
            portal_description: A description for the portal
            client_token: A unique case-sensitive identifier for the request
            portal_logo_image_file: A logo image to display in the portal
            role_arn: The ARN of a service role that allows the portal's users to access your AWS IoT SiteWise resources
            tags: A list of key-value pairs that contain metadata for the portal
            portal_auth_mode: The service to use to authenticate users to the portal (IAM, SSO)
            notification_sender_email: The email address that sends alarm notifications
            alarms: Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal

        Returns:
            Dictionary containing portal creation response
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {
            "portalName": portal_name,
            "portalContactEmail": portal_contact_email,
            "portalAuthMode": portal_auth_mode,
        }

        if portal_description:
            params["portalDescription"] = portal_description
        if client_token:
            params["clientToken"] = client_token
        if portal_logo_image_file:
            params["portalLogoImageFile"] = portal_logo_image_file
        if role_arn:
            params["roleArn"] = role_arn
        if tags:
            params["tags"] = tags
        if notification_sender_email:
            params["notificationSenderEmail"] = notification_sender_email
        if alarms:
            params["alarms"] = alarms

        response = client.create_portal(**params)
        return {
            "success": True,
            "portal_id": response["portalId"],
            "portal_arn": response["portalArn"],
            "portal_start_url": response["portalStartUrl"],
            "portal_status": response["portalStatus"],
            "sso_application_id": response.get("ssoApplicationId", ""),
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def describe_portal(portal_id: str, region: str = "us-east-1") -> Dict[str, Any]:
    """
    Retrieve information about a portal.

    Args:
        portal_id: The ID of the portal
        region: AWS region (default: us-east-1)

    Returns:
        Dictionary containing portal information
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        response = client.describe_portal(portalId=portal_id)

        return {
            "success": True,
            "portal_id": response["portalId"],
            "portal_arn": response["portalArn"],
            "portal_name": response["portalName"],
            "portal_description": response.get("portalDescription", ""),
            "portal_contact_email": response["portalContactEmail"],
            "portal_status": response["portalStatus"],
            "portal_creation_date": response["portalCreationDate"].isoformat(),
            "portal_last_update_date": response["portalLastUpdateDate"].isoformat(),
            "portal_logo_image_location": response.get("portalLogoImageLocation", {}),
            "role_arn": response.get("roleArn", ""),
            "portal_auth_mode": response.get("portalAuthMode", "IAM"),
            "notification_sender_email": response.get("notificationSenderEmail", ""),
            "portal_start_url": response["portalStartUrl"],
            "alarms": response.get("alarms", {}),
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def list_portals(
    region: str = "us-east-1", next_token: Optional[str] = None, max_results: int = 50
) -> Dict[str, Any]:
    """
    Retrieve a paginated list of AWS IoT SiteWise Monitor portals.

    Args:
        region: AWS region (default: us-east-1)
        next_token: The token to be used for the next set of paginated results
        max_results: The maximum number of results to return (1-250, default: 50)

    Returns:
        Dictionary containing list of portals
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {"maxResults": max_results}
        if next_token:
            params["nextToken"] = next_token

        response = client.list_portals(**params)

        return {
            "success": True,
            "portal_summaries": response["portalSummaries"],
            "next_token": response.get("nextToken", ""),
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def update_portal(
    portal_id: str,
    portal_name: str,
    portal_contact_email: str,
    region: str = "us-east-1",
    portal_description: Optional[str] = None,
    client_token: Optional[str] = None,
    portal_logo_image_file: Optional[Dict[str, Any]] = None,
    role_arn: Optional[str] = None,
    notification_sender_email: Optional[str] = None,
    alarms: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Update an AWS IoT SiteWise Monitor portal.

    Args:
        portal_id: The ID of the portal to update
        portal_name: A new friendly name for the portal
        portal_contact_email: The AWS administrator's contact email address
        region: AWS region (default: us-east-1)
        portal_description: A new description for the portal
        client_token: A unique case-sensitive identifier for the request
        portal_logo_image_file: A logo image to display in the portal
        role_arn: The ARN of a service role that allows the portal's users to access your AWS IoT SiteWise resources
        notification_sender_email: The email address that sends alarm notifications
        alarms: Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal

    Returns:
        Dictionary containing update response
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {
            "portalId": portal_id,
            "portalName": portal_name,
            "portalContactEmail": portal_contact_email,
        }

        if portal_description:
            params["portalDescription"] = portal_description
        if client_token:
            params["clientToken"] = client_token
        if portal_logo_image_file:
            params["portalLogoImageFile"] = portal_logo_image_file
        if role_arn:
            params["roleArn"] = role_arn
        if notification_sender_email:
            params["notificationSenderEmail"] = notification_sender_email
        if alarms:
            params["alarms"] = alarms

        response = client.update_portal(**params)
        return {"success": True, "portal_status": response["portalStatus"]}

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def delete_portal(
    portal_id: str, region: str = "us-east-1", client_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a portal from AWS IoT SiteWise Monitor.

    Args:
        portal_id: The ID of the portal to delete
        region: AWS region (default: us-east-1)
        client_token: A unique case-sensitive identifier for the request

    Returns:
        Dictionary containing deletion response
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {"portalId": portal_id}
        if client_token:
            params["clientToken"] = client_token

        response = client.delete_portal(**params)
        return {"success": True, "portal_status": response["portalStatus"]}

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def create_project(
    portal_id: str,
    project_name: str,
    region: str = "us-east-1",
    project_description: Optional[str] = None,
    client_token: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Create a project in the specified portal.

    Args:
        portal_id: The ID of the portal in which to create the project
        project_name: A friendly name for the project
        region: AWS region (default: us-east-1)
        project_description: A description for the project
        client_token: A unique case-sensitive identifier for the request
        tags: A list of key-value pairs that contain metadata for the project

    Returns:
        Dictionary containing project creation response
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {"portalId": portal_id, "projectName": project_name}

        if project_description:
            params["projectDescription"] = project_description
        if client_token:
            params["clientToken"] = client_token
        if tags:
            params["tags"] = tags

        response = client.create_project(**params)
        return {
            "success": True,
            "project_id": response["projectId"],
            "project_arn": response["projectArn"],
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def describe_project(project_id: str, region: str = "us-east-1") -> Dict[str, Any]:
    """
    Retrieve information about a project.

    Args:
        project_id: The ID of the project
        region: AWS region (default: us-east-1)

    Returns:
        Dictionary containing project information
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        response = client.describe_project(projectId=project_id)

        return {
            "success": True,
            "project_id": response["projectId"],
            "project_arn": response["projectArn"],
            "project_name": response["projectName"],
            "portal_id": response["portalId"],
            "project_description": response.get("projectDescription", ""),
            "project_creation_date": response["projectCreationDate"].isoformat(),
            "project_last_update_date": response["projectLastUpdateDate"].isoformat(),
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def list_projects(
    portal_id: str,
    region: str = "us-east-1",
    next_token: Optional[str] = None,
    max_results: int = 50,
) -> Dict[str, Any]:
    """
    Retrieve a paginated list of projects for an AWS IoT SiteWise Monitor portal.

    Args:
        portal_id: The ID of the portal
        region: AWS region (default: us-east-1)
        next_token: The token to be used for the next set of paginated results
        max_results: The maximum number of results to return (1-250, default: 50)

    Returns:
        Dictionary containing list of projects
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {"portalId": portal_id, "maxResults": max_results}
        if next_token:
            params["nextToken"] = next_token

        response = client.list_projects(**params)

        return {
            "success": True,
            "project_summaries": response["projectSummaries"],
            "next_token": response.get("nextToken", ""),
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def update_project(
    project_id: str,
    project_name: str,
    region: str = "us-east-1",
    project_description: Optional[str] = None,
    client_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update a project.

    Args:
        project_id: The ID of the project to update
        project_name: A new friendly name for the project
        region: AWS region (default: us-east-1)
        project_description: A new description for the project
        client_token: A unique case-sensitive identifier for the request

    Returns:
        Dictionary containing update response
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {"projectId": project_id, "projectName": project_name}

        if project_description:
            params["projectDescription"] = project_description
        if client_token:
            params["clientToken"] = client_token

        client.update_project(**params)
        return {"success": True, "message": "Project updated successfully"}

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def delete_project(
    project_id: str, region: str = "us-east-1", client_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a project from AWS IoT SiteWise Monitor.

    Args:
        project_id: The ID of the project
        region: AWS region (default: us-east-1)
        client_token: A unique case-sensitive identifier for the request

    Returns:
        Dictionary containing deletion response
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {"projectId": project_id}
        if client_token:
            params["clientToken"] = client_token

        client.delete_project(**params)
        return {"success": True, "message": "Project deleted successfully"}

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def create_dashboard(
    project_id: str,
    dashboard_name: str,
    dashboard_definition: str,
    region: str = "us-east-1",
    dashboard_description: Optional[str] = None,
    client_token: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Create a dashboard in a project.

    Args:
        project_id: The ID of the project in which to create the dashboard
        dashboard_name: A friendly name for the dashboard
        dashboard_definition: The dashboard definition specified in a JSON literal
        region: AWS region (default: us-east-1)
        dashboard_description: A description for the dashboard
        client_token: A unique case-sensitive identifier for the request
        tags: A list of key-value pairs that contain metadata for the dashboard

    Returns:
        Dictionary containing dashboard creation response
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {
            "projectId": project_id,
            "dashboardName": dashboard_name,
            "dashboardDefinition": dashboard_definition,
        }

        if dashboard_description:
            params["dashboardDescription"] = dashboard_description
        if client_token:
            params["clientToken"] = client_token
        if tags:
            params["tags"] = tags

        response = client.create_dashboard(**params)
        return {
            "success": True,
            "dashboard_id": response["dashboardId"],
            "dashboard_arn": response["dashboardArn"],
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def describe_dashboard(dashboard_id: str, region: str = "us-east-1") -> Dict[str, Any]:
    """
    Retrieve information about a dashboard.

    Args:
        dashboard_id: The ID of the dashboard
        region: AWS region (default: us-east-1)

    Returns:
        Dictionary containing dashboard information
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        response = client.describe_dashboard(dashboardId=dashboard_id)

        return {
            "success": True,
            "dashboard_id": response["dashboardId"],
            "dashboard_arn": response["dashboardArn"],
            "dashboard_name": response["dashboardName"],
            "project_id": response["projectId"],
            "dashboard_description": response.get("dashboardDescription", ""),
            "dashboard_definition": response["dashboardDefinition"],
            "dashboard_creation_date": response["dashboardCreationDate"].isoformat(),
            "dashboard_last_update_date": response["dashboardLastUpdateDate"].isoformat(),
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def list_dashboards(
    project_id: str,
    region: str = "us-east-1",
    next_token: Optional[str] = None,
    max_results: int = 50,
) -> Dict[str, Any]:
    """
    Retrieve a paginated list of dashboards for an AWS IoT SiteWise Monitor project.

    Args:
        project_id: The ID of the project
        region: AWS region (default: us-east-1)
        next_token: The token to be used for the next set of paginated results
        max_results: The maximum number of results to return (1-250, default: 50)

    Returns:
        Dictionary containing list of dashboards
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {"projectId": project_id, "maxResults": max_results}
        if next_token:
            params["nextToken"] = next_token

        response = client.list_dashboards(**params)

        return {
            "success": True,
            "dashboard_summaries": response["dashboardSummaries"],
            "next_token": response.get("nextToken", ""),
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def update_dashboard(
    dashboard_id: str,
    dashboard_name: str,
    dashboard_definition: str,
    region: str = "us-east-1",
    dashboard_description: Optional[str] = None,
    client_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update an AWS IoT SiteWise Monitor dashboard.

    Args:
        dashboard_id: The ID of the dashboard to update
        dashboard_name: A new friendly name for the dashboard
        dashboard_definition: The new dashboard definition
        region: AWS region (default: us-east-1)
        dashboard_description: A new description for the dashboard
        client_token: A unique case-sensitive identifier for the request

    Returns:
        Dictionary containing update response
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {
            "dashboardId": dashboard_id,
            "dashboardName": dashboard_name,
            "dashboardDefinition": dashboard_definition,
        }

        if dashboard_description:
            params["dashboardDescription"] = dashboard_description
        if client_token:
            params["clientToken"] = client_token

        client.update_dashboard(**params)
        return {"success": True, "message": "Dashboard updated successfully"}

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


def delete_dashboard(
    dashboard_id: str, region: str = "us-east-1", client_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delete a dashboard from AWS IoT SiteWise Monitor.

    Args:
        dashboard_id: The ID of the dashboard to delete
        region: AWS region (default: us-east-1)
        client_token: A unique case-sensitive identifier for the request

    Returns:
        Dictionary containing deletion response
    """
    try:
        client = boto3.client("iotsitewise", region_name=region)

        params: Dict[str, Any] = {"dashboardId": dashboard_id}
        if client_token:
            params["clientToken"] = client_token

        client.delete_dashboard(**params)
        return {"success": True, "message": "Dashboard deleted successfully"}

    except ClientError as e:
        return {"success": False, "error": str(e), "error_code": e.response["Error"]["Code"]}


# Create MCP tools
create_portal_tool = Tool.from_function(
    fn=create_portal,
    name="create_portal",
    description="Create a portal in AWS IoT SiteWise Monitor for web-based asset monitoring and management.",
)

describe_portal_tool = Tool.from_function(
    fn=describe_portal,
    name="describe_portal",
    description="Retrieve detailed information about an AWS IoT SiteWise Monitor portal.",
)

list_portals_tool = Tool.from_function(
    fn=list_portals,
    name="list_portals",
    description="Retrieve a paginated list of AWS IoT SiteWise Monitor portals.",
)

update_portal_tool = Tool.from_function(
    fn=update_portal,
    name="update_portal",
    description="Update an AWS IoT SiteWise Monitor portal's configuration.",
)

delete_portal_tool = Tool.from_function(
    fn=delete_portal,
    name="delete_portal",
    description="Delete a portal from AWS IoT SiteWise Monitor.",
)

create_project_tool = Tool.from_function(
    fn=create_project,
    name="create_project",
    description="Create a project in an AWS IoT SiteWise Monitor portal.",
)

describe_project_tool = Tool.from_function(
    fn=describe_project,
    name="describe_project",
    description="Retrieve detailed information about an AWS IoT SiteWise Monitor project.",
)

list_projects_tool = Tool.from_function(
    fn=list_projects,
    name="list_projects",
    description="Retrieve a paginated list of projects for an AWS IoT SiteWise Monitor portal.",
)

update_project_tool = Tool.from_function(
    fn=update_project,
    name="update_project",
    description="Update an AWS IoT SiteWise Monitor project.",
)

delete_project_tool = Tool.from_function(
    fn=delete_project,
    name="delete_project",
    description="Delete a project from AWS IoT SiteWise Monitor.",
)

create_dashboard_tool = Tool.from_function(
    fn=create_dashboard,
    name="create_dashboard",
    description="Create a dashboard in an AWS IoT SiteWise Monitor project.",
)

describe_dashboard_tool = Tool.from_function(
    fn=describe_dashboard,
    name="describe_dashboard",
    description="Retrieve detailed information about an AWS IoT SiteWise Monitor dashboard.",
)

list_dashboards_tool = Tool.from_function(
    fn=list_dashboards,
    name="list_dashboards",
    description="Retrieve a paginated list of dashboards for an AWS IoT SiteWise Monitor project.",
)

update_dashboard_tool = Tool.from_function(
    fn=update_dashboard,
    name="update_dashboard",
    description="Update an AWS IoT SiteWise Monitor dashboard.",
)

delete_dashboard_tool = Tool.from_function(
    fn=delete_dashboard,
    name="delete_dashboard",
    description="Delete a dashboard from AWS IoT SiteWise Monitor.",
)
