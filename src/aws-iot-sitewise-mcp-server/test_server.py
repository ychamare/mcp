#!/usr/bin/env python3
"""Test script to verify the IoT SiteWise MCP server works."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from awslabs.aws_iot_sitewise_mcp_server import consts
        print("✅ Constants imported successfully")
        print(f"   - Read-only tools: {len(consts.READ_ONLY_TOOLS)}")
        print(f"   - Write tools: {len(consts.WRITE_TOOLS)}")
        print(f"   - Destructive tools: {len(consts.DESTRUCTIVE_TOOLS)}")
        
        from awslabs.aws_iot_sitewise_mcp_server import models
        print("✅ Models imported successfully")
        
        from awslabs.aws_iot_sitewise_mcp_server import iotsitewise
        print("✅ IoT SiteWise service imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_server_with_mocked_deps():
    """Test server import with mocked dependencies."""
    try:
        # Mock the dependencies
        import sys
        from unittest.mock import MagicMock
        
        sys.modules['fastmcp'] = MagicMock()
        sys.modules['loguru'] = MagicMock()
        sys.modules['boto3'] = MagicMock()
        
        from awslabs.aws_iot_sitewise_mcp_server import server
        print("✅ Server imported successfully (with mocked deps)")
        print(f"   - Main function available: {hasattr(server, 'main')}")
        
        return True
    except Exception as e:
        print(f"❌ Server import failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing AWS IoT SiteWise MCP Server...")
    print("=" * 50)
    
    # Test basic imports
    if test_imports():
        print("\n🧪 Testing server import...")
        test_server_with_mocked_deps()
    
    print("\n" + "=" * 50)
    print("💡 If imports work but server fails, install dependencies:")
    print("   pip install fastmcp boto3 pydantic loguru")
    print("   or")
    print("   uv sync")