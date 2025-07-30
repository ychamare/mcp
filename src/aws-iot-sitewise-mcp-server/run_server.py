#!/usr/bin/env python3
"""Runner script for AWS IoT SiteWise MCP Server."""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from awslabs.aws_iot_sitewise_mcp_server.server import main

if __name__ == "__main__":
    main()