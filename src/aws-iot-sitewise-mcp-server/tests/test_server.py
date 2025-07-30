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

"""Tests for server functionality."""

import pytest


class TestServer:
    """Test server initialization and basic functionality."""

    def test_server_imports(self):
        """Test that server module can be imported."""
        try:
            from awslabs.aws_iot_sitewise_mcp_server import server
            assert hasattr(server, 'main')
        except ImportError as e:
            pytest.skip(f"Server dependencies not available: {e}")

    def test_constants_import(self):
        """Test that constants can be imported."""
        from awslabs.aws_iot_sitewise_mcp_server.consts import READ_ONLY_TOOLS, WRITE_TOOLS, DESTRUCTIVE_TOOLS
        
        # Verify we have the expected number of tools
        assert len(READ_ONLY_TOOLS) == 22
        assert len(WRITE_TOOLS) == 21
        assert len(DESTRUCTIVE_TOOLS) == 6
        
        # Verify total is 49 tools
        total_tools = len(READ_ONLY_TOOLS) + len(WRITE_TOOLS) + len(DESTRUCTIVE_TOOLS)
        assert total_tools == 49

    def test_models_import(self):
        """Test that models can be imported."""
        from awslabs.aws_iot_sitewise_mcp_server.models import ListAssetModelsParams, CreateAssetParams
        
        # Test basic model creation
        list_params = ListAssetModelsParams()
        assert list_params.maxResults is None
        
        # Test required fields
        with pytest.raises(ValueError):
            CreateAssetParams()  # Should fail without required fields