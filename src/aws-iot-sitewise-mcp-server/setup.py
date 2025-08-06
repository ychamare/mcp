#!/usr/bin/env python

from setuptools import setup, find_namespace_packages

if __name__ == "__main__":
    setup(
        name="aws-iot-sitewise-mcp",
        version="0.1.0",
        description="An AWS Labs Model Context Protocol (MCP) server for AWS IoT SiteWise API integration",
        packages=find_namespace_packages(include=['awslabs.*']),
        entry_points={
            'console_scripts': [
                'aws-iot-sitewise-mcp=awslabs.aws_iot_sitewise_mcp_server.server:main',
            ],
        },
    )
