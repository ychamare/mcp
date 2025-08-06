#!/usr/bin/env python3
"""
Integration test runner with comprehensive resource cleanup.

This script runs integration tests with proper setup and cleanup,
ensuring no AWS resources are leaked.

Usage:
    python scripts/run_integration_tests.py [--test TEST_CLASS] [--region REGION] [--dry-run]
"""

import argparse
import sys
import os
import subprocess
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_command(cmd, check=True):
    """Run a command and return the result."""
    logger.info("Running: {}".format(' '.join(cmd)))
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        logger.info("STDOUT: {}".format(result.stdout))
    if result.stderr:
        logger.warning("STDERR: {}".format(result.stderr))
    
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)
    
    return result


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(
        description='Run AWS IoT SiteWise integration tests with cleanup'
    )
    parser.add_argument(
        '--test',
        help='Specific test class to run (e.g., TestAssetModelLifecycle)'
    )
    parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region for testing (default: us-east-1)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Check setup without running tests'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--cleanup-only',
        action='store_true',
        help='Only run cleanup, skip tests'
    )
    
    args = parser.parse_args()
    
    # Set environment variables
    os.environ['AWS_DEFAULT_REGION'] = args.region
    
    try:
        # Pre-test cleanup
        logger.info("Running pre-test cleanup...")
        cleanup_cmd = [
            sys.executable, 'scripts/cleanup_test_resources.py',
            '--region', args.region,
            '--force'
        ]
        
        if args.dry_run:
            cleanup_cmd.append('--dry-run')
        
        run_command(cleanup_cmd, check=False)  # Don't fail if cleanup has issues
        
        if args.cleanup_only:
            logger.info("Cleanup-only mode - skipping tests")
            return 0
        
        if args.dry_run:
            logger.info("Dry run mode - checking test setup...")
            
            # Check AWS credentials
            try:
                import boto3
                client = boto3.client('iotsitewise', region_name=args.region)
                client.describe_default_encryption_configuration()
                logger.info("✓ AWS credentials are valid")
            except Exception as e:
                logger.error("✗ AWS credentials issue: {}".format(e))
                return 1
            
            logger.info("✓ Setup check completed successfully")
            return 0
        
        # Build pytest command
        pytest_cmd = [sys.executable, '-m', 'pytest', 'test/test_integration.py']
        
        if args.test:
            pytest_cmd.extend(['-k', args.test])
        
        pytest_cmd.extend(['-m', 'integration'])
        
        if args.verbose:
            pytest_cmd.extend(['-v', '-s'])
        
        # Add coverage if available
        try:
            import pytest_cov
            pytest_cmd.extend(['--cov=site_wise_mcp_poc', '--cov-report=term-missing'])
        except ImportError:
            pass
        
        # Run tests
        logger.info("Running integration tests...")
        test_result = run_command(pytest_cmd, check=False)
        
        # Post-test cleanup
        logger.info("Running post-test cleanup...")
        run_command(cleanup_cmd, check=False)
        
        if test_result.returncode == 0:
            logger.info("✓ All tests passed successfully")
        else:
            logger.error("✗ Tests failed with exit code {}".format(test_result.returncode))
        
        return test_result.returncode
        
    except KeyboardInterrupt:
        logger.warning("Test run interrupted by user")
        
        # Emergency cleanup
        logger.info("Running emergency cleanup...")
        try:
            run_command([
                sys.executable, 'scripts/cleanup_test_resources.py',
                '--region', args.region,
                '--force'
            ], check=False)
        except Exception as e:
            logger.error("Emergency cleanup failed: {}".format(e))
        
        return 1
        
    except Exception as e:
        logger.error("Test run failed: {}".format(e))
        return 1


if __name__ == '__main__':
    sys.exit(main())
