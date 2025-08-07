#!/usr/bin/env python3
"""This script starts the MCP server directly by using the Python import
approach.
"""

import os
import sys
from awslabs.aws_iot_sitewise_mcp_server.server import main


# Add the project root to the Python path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)


if __name__ == '__main__':
    print('Starting server using direct import...')
    main()
