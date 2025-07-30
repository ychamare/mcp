# Changelog

All notable changes to the AWS IoT SiteWise MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-30

### Added
- Initial Python implementation using FastMCP framework
- Extensive AWS IoT SiteWise API coverage (49 tools)
- Safety categorization with visual indicators (📖 read-only, ⚠️ write, 🚨 destructive, 🔐 security)
- 22 read-only tools for safe data exploration
- 21 write operation tools with safety warnings  
- 6 destructive operation tools with critical warnings
- Asset and asset model management capabilities
- Time-series data operations (current, historical, aggregated)
- Batch operations for efficient data processing
- Gateway management for on-premises connectivity
- Portal and dashboard management for visualization
- Access policy management for security
- Comprehensive Pydantic models for parameter validation
- Structured logging with loguru
- Async error handling and retry logic
- UV dependency management support
- Pre-commit hooks and code quality tools (ruff, pyright, pytest)
- Proper awslabs repository structure and naming conventions
- Multi-platform MCP client support (Claude Desktop, Claude Code, Amazon Q CLI)
- Comprehensive documentation with setup instructions

### Security
- Safety indicators for all operations
- Comprehensive input validation  
- Secure credential handling
- No sensitive data logging