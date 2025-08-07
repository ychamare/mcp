# AWS IoT SiteWise MCP Server

[![GitHub](https://img.shields.io/badge/github-awslabs/mcp-blue.svg?style=flat&logo=github)](https://github.com/awslabs/mcp)
[![License](https://img.shields.io/badge/license-Apache--2.0-brightgreen)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)

A comprehensive Model Context Protocol (MCP) server for AWS IoT SiteWise API integration, providing AI assistants with seamless access to industrial IoT data management capabilities.

## Features

### 🚀 **Extensive API Coverage**
- **49 tools** covering AWS IoT SiteWise functionality
- **22 read-only tools** for safe data exploration
- **21 write operations** for resource management
- **6 destructive operations** with safety controls

### 🛡️ **Safety-First Design**
- **Visual safety indicators**: ⚠️ Write operations, 🚨 Destructive actions, 🔐 Security policies
- **Comprehensive validation** using Pydantic models
- **Detailed logging** with configurable levels
- **Error handling** with meaningful messages

### 📊 **Industrial IoT Capabilities**
- **Asset & Asset Model Management**: Create, update, and organize industrial assets
- **Time-Series Data**: Real-time and historical property values with aggregations
- **Batch Operations**: Efficient bulk data retrieval and ingestion
- **Gateway Management**: Connect on-premises systems to AWS (External service dependencies)
- **Monitor Portals**: Web-based dashboards and visualizations (External service dependencies)
- **Access Control**: Fine-grained security policies

## Quick Start

### Installation

#### Option 1: UVX (Recommended)
```bash
# Install and run directly with uvx
uvx awslabs.aws-iot-sitewise-mcp-server
```

#### Option 2: UV
```bash
# Clone the repository
git clone https://github.com/awslabs/mcp.git
cd mcp/src/aws-iot-sitewise-mcp-server

# Install dependencies with uv
uv sync

# Run the server
uv run awslabs.aws-iot-sitewise-mcp-server
```

#### Option 3: Pip
```bash

# Run the server
awslabs.aws-iot-sitewise-mcp-server

# Or install from source
git clone https://github.com/awslabs/mcp.git
cd mcp/src/aws-iot-sitewise-mcp-server
pip install -e .
```

### AWS Credentials

Configure AWS credentials using any of these methods:

```bash
# AWS CLI (recommended)
aws configure

# Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-west-2

# Or use AWS profiles
export AWS_PROFILE=your-profile-name
```

### Required IAM Permissions

Your AWS credentials need permissions for IoT SiteWise operations. **Open scope policy, only recommended for testing**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iotsitewise:*"
            ],
            "Resource": "*"
        }
    ]
}
```

For production use, restrict permissions to specific resources and actions as needed. Restricting the Actions will also help mitigate tool misuse - consider scoping your permissions to meet your use case needs.

## Usage with MCP Clients

### Amazon q cli
Add to your `mcp.json` configuration file:

```json
{
  "mcpServers": {
    "aws-iot-sitewise": {
      "args": ["awslabs.aws-iot-sitewise-mcp-server"],
      "env": {
        "AWS_REGION": "us-west-2",
        "AWS_PROFILE": "your-profile"
      }
    }
  }
}
```

### Claude Desktop
Add to your `claude_desktop_config.json` configuration file:

```json
{
  "mcpServers": {
    "aws-iot-sitewise": {
      "args": ["awslabs.aws-iot-sitewise-mcp-server"],
      "env": {
        "AWS_REGION": "us-west-2",
        "AWS_PROFILE": "your-profile"
      }
    }
  }
}
```

### Testing

```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector uvx awslabs.aws-iot-sitewise-mcp-server

# Run with debug logging
FASTMCP_LOG_LEVEL=DEBUG uvx awslabs.aws-iot-sitewise-mcp-server
```

## Available Tools

### 📖 Read-Only Operations (22 tools)

**Asset Management:**
- `list_asset_models` - List all asset models
- `describe_asset_model` - Get asset model details
- `list_assets` - List assets (optionally filtered by model)
- `describe_asset` - Get asset details
- `list_associated_assets` - List child/parent assets

**Property Data:**
- `get_asset_property_value` - Get current property value
- `get_asset_property_value_history` - Get historical data
- `get_asset_property_aggregates` - Get aggregated statistics
- `get_interpolated_asset_property_values` - Get interpolated values

**Batch Operations:**
- `batch_get_asset_property_value` - Bulk current values
- `batch_get_asset_property_value_history` - Bulk historical data
- `batch_get_asset_property_aggregates` - Bulk aggregates

**Infrastructure:**
- `list_gateways` - List IoT SiteWise gateways
- `describe_gateway` - Get gateway details
- `describe_gateway_capability_configuration` - Get gateway capabilities

**Monitor & Portals:**
- `list_portals` - List Monitor portals
- `list_projects` - List projects in portal
- `list_dashboards` - List dashboards in project

**Time Series & Policies:**
- `list_time_series` - List time series
- `describe_time_series` - Get time series details
- `list_access_policies` - List access policies
- `execute_query` - Execute SQL queries against SiteWise data
- `list_executions` - List query executions
- `describe_execution` - Get query execution details

### ⚠️ Write Operations (21 tools)

**Asset Management:**
- `create_asset` - Create new asset
- `update_asset` - Update asset details
- `associate_assets` - Create asset hierarchies
- `disassociate_assets` - Remove asset associations

**Asset Models:**
- `create_asset_model` - Create asset model template
- `update_asset_model` - Modify asset model

**Data Ingestion:**
- `batch_put_asset_property_value` - Send time-series data

**Gateway Operations:**
- `create_gateway` - Create new gateway
- `update_gateway` - Update gateway settings
- `update_gateway_capability_configuration` - Configure gateway capabilities

**Portal & Dashboard Management:**
- `create_portal` - Create Monitor portal
- `update_portal` - Update portal settings
- `create_project` - Create project in portal
- `create_dashboard` - Create dashboard
- `update_dashboard` - Update dashboard

**Security & Access:**
- `create_access_policy` - 🔐 Create access policy
- `update_access_policy` - 🔐 Update access policy

**Time Series:**
- `associate_time_series_to_asset_property` - Link time series to property
- `disassociate_time_series_from_asset_property` - Unlink time series

**Configuration:**
- `put_default_encryption_configuration` - Set default encryption
- `put_logging_options` - Configure logging
- `put_storage_configuration` - Configure storage settings

### 🚨 Destructive Operations (6 tools)

**WARNING: These operations permanently delete resources and cannot be undone!**

- `delete_asset` - 🚨 Delete asset permanently
- `delete_asset_model` - 🚨 Delete asset model permanently
- `delete_gateway` - 🚨 Delete gateway permanently
- `delete_portal` - 🚨 Delete portal permanently
- `delete_dashboard` - 🚨 Delete dashboard permanently
- `delete_access_policy` - 🚨 Delete access policy permanently
- `delete_time_series` - 🚨 Delete time series permanently
- `delete_project` - 🚨 Delete project permanently

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AWS_REGION` | `us-east-1` | AWS region for IoT SiteWise |
| `AWS_PROFILE` | None | AWS CLI profile to use |
| `FASTMCP_LOG_LEVEL` | `WARNING` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Development

### Local Development

```bash
# Clone the repository
git clone https://github.com/awslabs/mcp.git
cd mcp/src/aws-iot-sitewise-mcp-server

# Install in editable mode for development
pip install -e .

# Or run directly from source
uv run python -m awslabs.aws_iot_sitewise_mcp_server.server

# Test the installed command
awslabs.aws-iot-sitewise-mcp-server --version
```

### Building the Package

```bash
# Build package for distribution
uv build

# Install the built wheel for testing
pip install dist/awslabs_aws_iot_sitewise_mcp_server-*.whl
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ by AWS Gen AI Labs and AWS IoT Sitewise Engineering teams**
