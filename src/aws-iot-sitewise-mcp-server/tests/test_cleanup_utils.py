"""
Resource cleanup utilities for AWS IoT SiteWise integration tests.

This module provides comprehensive cleanup functionality to ensure no AWS resources
are leaked during integration testing.
"""

import atexit
import logging
import signal
import threading
import time
from contextlib import contextmanager

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global registry for cleanup on exit
_global_cleanup_registry = []
_cleanup_lock = threading.Lock()


def _emergency_cleanup():
    """Emergency cleanup function called on exit or signal."""
    with _cleanup_lock:
        if _global_cleanup_registry:
            logger.warning("Emergency cleanup triggered - cleaning up registered resources")
            for tracker in _global_cleanup_registry:
                try:
                    tracker.cleanup_all()
                except Exception as e:
                    logger.error("Emergency cleanup failed for tracker: {}".format(e))
            _global_cleanup_registry[:] = []


def _signal_handler(signum, frame):
    """Handle termination signals."""
    logger.warning("Received signal {} - triggering emergency cleanup".format(signum))
    _emergency_cleanup()
    exit(1)


# Register signal handlers and exit handler
signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)
atexit.register(_emergency_cleanup)


def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    """Retry a function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            # Don't retry on certain errors
            if error_code in [
                "ResourceNotFoundException",
                "AccessDeniedException",
                "UnauthorizedOperation",
                "InvalidRequestException",
            ]:
                raise

            if attempt == max_retries - 1:
                raise

            delay = base_delay * (2**attempt)
            logger.warning(
                "Attempt {} failed: {}. Retrying in {}s...".format(attempt + 1, e, delay)
            )
            time.sleep(delay)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2**attempt)
            logger.warning(
                "Attempt {} failed: {}. Retrying in {}s...".format(attempt + 1, e, delay)
            )
            time.sleep(delay)


class SiteWiseResourceTracker:
    """Track and cleanup AWS IoT SiteWise resources created during tests."""

    def __init__(self, region="us-east-1", test_prefix="mcp-test"):
        self.region = region
        self.test_prefix = test_prefix
        self._client = None
        self._client_error = None

        # Track resources created during tests
        self.created_assets = set()
        self.created_asset_models = set()
        self.created_portals = set()
        self.created_projects = set()
        self.created_dashboards = set()
        self.created_gateways = set()
        self.created_access_policies = set()
        self.created_time_series = set()

        # Track associations that need to be cleaned up
        self.asset_associations = []
        self.time_series_associations = []

        # Register for emergency cleanup
        with _cleanup_lock:
            _global_cleanup_registry.append(self)

    @property
    def client(self):
        """Lazy initialization of boto3 client with error handling."""
        if self._client is None and self._client_error is None:
            try:
                self._client = boto3.client("iotsitewise", region_name=self.region)
                # Test the client with a simple call
                self._client.describe_default_encryption_configuration()
            except (NoCredentialsError, Exception) as e:
                if "UnrecognizedClientException" in str(e):
                    self._client_error = "Invalid AWS credentials: {}".format(e)
                else:
                    self._client_error = "AWS client error: {}".format(e)
                logger.error(self._client_error)

        if self._client_error:
            raise RuntimeError(self._client_error)

        return self._client

    def is_aws_available(self):
        """Check if AWS is available for testing."""
        try:
            _ = self.client
            return True
        except RuntimeError:
            return False

    def register_asset(self, asset_id):
        """Register an asset for cleanup."""
        self.created_assets.add(asset_id)
        logger.info("Registered asset for cleanup: {}".format(asset_id))

    def register_asset_model(self, asset_model_id):
        """Register an asset model for cleanup."""
        self.created_asset_models.add(asset_model_id)
        logger.info("Registered asset model for cleanup: {}".format(asset_model_id))

    def register_portal(self, portal_id):
        """Register a portal for cleanup."""
        self.created_portals.add(portal_id)
        logger.info("Registered portal for cleanup: {}".format(portal_id))

    def register_project(self, project_id):
        """Register a project for cleanup."""
        self.created_projects.add(project_id)
        logger.info("Registered project for cleanup: {}".format(project_id))

    def register_dashboard(self, dashboard_id):
        """Register a dashboard for cleanup."""
        self.created_dashboards.add(dashboard_id)
        logger.info("Registered dashboard for cleanup: {}".format(dashboard_id))

    def register_gateway(self, gateway_id):
        """Register a gateway for cleanup."""
        self.created_gateways.add(gateway_id)
        logger.info("Registered gateway for cleanup: {}".format(gateway_id))

    def register_access_policy(self, policy_id):
        """Register an access policy for cleanup."""
        self.created_access_policies.add(policy_id)
        logger.info("Registered access policy for cleanup: {}".format(policy_id))

    def register_time_series(self, time_series_id):
        """Register a time series for cleanup."""
        self.created_time_series.add(time_series_id)
        logger.info("Registered time series for cleanup: {}".format(time_series_id))

    def register_asset_association(self, parent_asset_id, hierarchy_id, child_asset_id):
        """Register an asset association for cleanup."""
        association = {
            "parent_asset_id": parent_asset_id,
            "hierarchy_id": hierarchy_id,
            "child_asset_id": child_asset_id,
        }
        self.asset_associations.append(association)
        logger.info(
            "Registered asset association for cleanup: {} -> {}".format(
                parent_asset_id, child_asset_id
            )
        )

    def wait_for_resource_state(self, resource_type, resource_id, target_states, timeout=300):
        """Wait for a resource to reach a target state."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                if resource_type == "asset":
                    response = self.client.describe_asset(assetId=resource_id)
                    current_state = response["assetStatus"]["state"]
                elif resource_type == "asset_model":
                    response = self.client.describe_asset_model(assetModelId=resource_id)
                    current_state = response["assetModelStatus"]["state"]
                elif resource_type == "portal":
                    response = self.client.describe_portal(portalId=resource_id)
                    current_state = response["portalStatus"]["state"]
                else:
                    logger.warning(
                        "Unknown resource type for state checking: {}".format(resource_type)
                    )
                    return True

                if current_state in target_states:
                    logger.info(
                        "{} {} reached state: {}".format(resource_type, resource_id, current_state)
                    )
                    return True

                logger.debug(
                    "Waiting for {} {} to reach {}, current: {}".format(
                        resource_type, resource_id, target_states, current_state
                    )
                )
                time.sleep(5)

            except ClientError as e:
                if e.response["Error"]["Code"] == "ResourceNotFoundException":
                    logger.info("{} {} no longer exists".format(resource_type, resource_id))
                    return True
                logger.error("Error checking {} {} state: {}".format(resource_type, resource_id, e))
                time.sleep(5)

        logger.warning(
            "Timeout waiting for {} {} to reach {}".format(
                resource_type, resource_id, target_states
            )
        )
        return False

    def cleanup_asset_associations(self):
        """Clean up asset associations."""
        if not self.is_aws_available():
            logger.warning("AWS not available - skipping asset association cleanup")
            return

        logger.info("Cleaning up asset associations...")

        for association in self.asset_associations[
            :
        ]:  # Copy list to avoid modification during iteration
            try:
                self.client.disassociate_assets(
                    assetId=association["parent_asset_id"],
                    hierarchyId=association["hierarchy_id"],
                    childAssetId=association["child_asset_id"],
                )
                logger.info(
                    "Disassociated assets: {} -> {}".format(
                        association["parent_asset_id"], association["child_asset_id"]
                    )
                )
                self.asset_associations.remove(association)
            except ClientError as e:
                if e.response["Error"]["Code"] in [
                    "ResourceNotFoundException",
                    "InvalidRequestException",
                ]:
                    logger.info(
                        "Asset association no longer exists: {} -> {}".format(
                            association["parent_asset_id"], association["child_asset_id"]
                        )
                    )
                    self.asset_associations.remove(association)
                else:
                    logger.error(
                        "Failed to disassociate assets {} -> {}: {}".format(
                            association["parent_asset_id"], association["child_asset_id"], e
                        )
                    )
            except Exception as e:
                logger.error(
                    "Unexpected error disassociating assets {} -> {}: {}".format(
                        association["parent_asset_id"], association["child_asset_id"], e
                    )
                )

    def cleanup_assets(self):
        """Clean up assets with retry logic."""
        if not self.is_aws_available():
            logger.warning("AWS not available - skipping asset cleanup")
            return

        logger.info("Cleaning up assets...")

        for asset_id in list(self.created_assets):
            try:

                def delete_asset():
                    self.wait_for_resource_state("asset", asset_id, ["ACTIVE", "FAILED"])
                    self.client.delete_asset(assetId=asset_id)
                    logger.info("Deleted asset: {}".format(asset_id))
                    self.wait_for_resource_state("asset", asset_id, ["DELETING"])

                retry_with_backoff(delete_asset)

            except ClientError as e:
                if e.response["Error"]["Code"] != "ResourceNotFoundException":
                    logger.error("Failed to delete asset {}: {}".format(asset_id, e))
            except Exception as e:
                logger.error("Unexpected error deleting asset {}: {}".format(asset_id, e))
            finally:
                self.created_assets.discard(asset_id)

    def cleanup_asset_models(self):
        """Clean up asset models with retry logic."""
        if not self.is_aws_available():
            logger.warning("AWS not available - skipping asset model cleanup")
            return

        logger.info("Cleaning up asset models...")

        for asset_model_id in list(self.created_asset_models):
            try:

                def delete_asset_model():
                    self.wait_for_resource_state(
                        "asset_model", asset_model_id, ["ACTIVE", "FAILED"]
                    )
                    self.client.delete_asset_model(assetModelId=asset_model_id)
                    logger.info("Deleted asset model: {}".format(asset_model_id))
                    self.wait_for_resource_state("asset_model", asset_model_id, ["DELETING"])

                retry_with_backoff(delete_asset_model)

            except ClientError as e:
                if e.response["Error"]["Code"] != "ResourceNotFoundException":
                    logger.error("Failed to delete asset model {}: {}".format(asset_model_id, e))
            except Exception as e:
                logger.error(
                    "Unexpected error deleting asset model {}: {}".format(asset_model_id, e)
                )
            finally:
                self.created_asset_models.discard(asset_model_id)

    def cleanup_portals(self):
        """Clean up portals."""
        if not self.is_aws_available():
            logger.warning("AWS not available - skipping portal cleanup")
            return

        logger.info("Cleaning up portals...")

        for portal_id in list(self.created_portals):
            try:
                self.wait_for_resource_state("portal", portal_id, ["ACTIVE", "FAILED"])
                self.client.delete_portal(portalId=portal_id)
                logger.info("Deleted portal: {}".format(portal_id))
                self.wait_for_resource_state("portal", portal_id, ["DELETING"])
            except ClientError as e:
                if e.response["Error"]["Code"] != "ResourceNotFoundException":
                    logger.error("Failed to delete portal {}: {}".format(portal_id, e))
            finally:
                self.created_portals.discard(portal_id)

    def cleanup_all(self):
        """Clean up all tracked resources in the correct order."""
        if not self.is_aws_available():
            logger.warning("AWS not available - skipping all cleanup")
            return

        logger.info("Starting comprehensive resource cleanup...")

        cleanup_errors = []

        try:
            # Clean up in reverse dependency order
            cleanup_methods = [
                ("asset_associations", self.cleanup_asset_associations),
                ("portals", self.cleanup_portals),
                ("assets", self.cleanup_assets),
                ("asset_models", self.cleanup_asset_models),  # Last, as assets depend on models
            ]

            for resource_type, cleanup_method in cleanup_methods:
                try:
                    cleanup_method()
                except Exception as e:
                    error_msg = "Failed to cleanup {}: {}".format(resource_type, e)
                    logger.error(error_msg)
                    cleanup_errors.append(error_msg)

            if cleanup_errors:
                logger.warning(
                    "Resource cleanup completed with {} errors".format(len(cleanup_errors))
                )
                for error in cleanup_errors:
                    logger.warning("  - {}".format(error))
            else:
                logger.info("Resource cleanup completed successfully")

        except Exception as e:
            logger.error("Critical error during resource cleanup: {}".format(e))
            raise
        finally:
            # Remove from global registry
            with _cleanup_lock:
                if self in _global_cleanup_registry:
                    _global_cleanup_registry.remove(self)

    def find_and_cleanup_test_resources(self):
        """Find and clean up any test resources that may have been left behind."""
        if not self.is_aws_available():
            logger.warning("AWS not available - skipping orphaned resource scan")
            return

        logger.info("Scanning for orphaned test resources...")

        # Call the actual cleanup implementation
        self.cleanup_orphaned_test_resources()

    def cleanup_orphaned_test_resources(self):
        """Find and clean up any test resources that may have been left behind."""
        if not self.is_aws_available():
            logger.warning("AWS not available - skipping orphaned resource scan")
            return

        logger.info("Scanning for orphaned test resources...")

        try:
            # Find test asset models first (these can be listed without restrictions)
            try:
                response = self.client.list_asset_models(maxResults=250)
                for model in response["assetModelSummaries"]:
                    if model["name"].startswith(self.test_prefix):
                        logger.warning("Found orphaned test asset model: {}".format(model["id"]))
                        self.register_asset_model(model["id"])

                        # For each test asset model, check for assets
                        try:
                            asset_response = self.client.list_assets(
                                assetModelId=model["id"], maxResults=250
                            )
                            for asset in asset_response["assetSummaries"]:
                                if asset["name"].startswith(self.test_prefix):
                                    logger.warning(
                                        "Found orphaned test asset: {}".format(asset["id"])
                                    )
                                    self.register_asset(asset["id"])
                        except ClientError as e:
                            logger.error(
                                "Failed to list assets for model {}: {}".format(model["id"], e)
                            )

            except ClientError as e:
                logger.error("Failed to list asset models: {}".format(e))

            # Find test portals
            try:
                response = self.client.list_portals(maxResults=250)
                for portal in response["portalSummaries"]:
                    if portal["name"].startswith(self.test_prefix):
                        logger.warning("Found orphaned test portal: {}".format(portal["id"]))
                        self.register_portal(portal["id"])
            except ClientError as e:
                logger.error("Failed to list portals: {}".format(e))

            # Clean up any found resources
            if self.created_assets or self.created_asset_models or self.created_portals:
                logger.info("Cleaning up orphaned test resources...")
                self.cleanup_all()
            else:
                logger.info("No orphaned test resources found")

        except Exception as e:
            logger.error("Error scanning for orphaned resources: {}".format(e))


@contextmanager
def sitewise_test_resources(region="us-east-1", test_prefix="mcp-test"):
    """
    Context manager for managing SiteWise test resources with automatic cleanup.

    Usage:
        with sitewise_test_resources() as tracker:
            # Create resources and register them
            asset_id = create_test_asset()
            tracker.register_asset(asset_id)

            # Test code here

        # Resources are automatically cleaned up when exiting the context
    """
    tracker = SiteWiseResourceTracker(region=region, test_prefix=test_prefix)

    try:
        # Check if AWS is available before proceeding
        if not tracker.is_aws_available():
            logger.warning("AWS not available - tests will be skipped")
            yield tracker
            return

        # Clean up any orphaned resources from previous failed tests
        try:
            tracker.find_and_cleanup_test_resources()
        except Exception as e:
            logger.warning("Failed to clean up orphaned resources: {}".format(e))

        yield tracker

    except KeyboardInterrupt:
        logger.warning("Test interrupted - performing cleanup...")
        try:
            tracker.cleanup_all()
        except Exception as e:
            logger.error("Failed to clean up resources after interruption: {}".format(e))
        raise

    except Exception as e:
        logger.error("Test failed with error: {}".format(e))
        # Still try to clean up
        try:
            tracker.cleanup_all()
        except Exception as cleanup_error:
            logger.error(
                "Failed to clean up resources after test failure: {}".format(cleanup_error)
            )
        raise

    finally:
        # Always clean up resources, even if test fails
        try:
            tracker.cleanup_all()
        except Exception as e:
            logger.error("Failed to clean up resources in finally block: {}".format(e))
            # Don't re-raise to avoid masking original test failures


def generate_test_name(base_name, test_prefix="mcp-test"):
    """Generate a unique test resource name."""
    import uuid

    timestamp = int(time.time())
    short_uuid = str(uuid.uuid4())[:8]
    return "{}-{}-{}-{}".format(test_prefix, base_name, timestamp, short_uuid)


def wait_for_asset_active(client, asset_id, timeout=300):
    """Wait for an asset to become ACTIVE."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = client.describe_asset(assetId=asset_id)
            state = response["assetStatus"]["state"]

            if state == "ACTIVE":
                return True
            elif state == "FAILED":
                logger.error("Asset {} failed to activate".format(asset_id))
                return False

            time.sleep(5)

        except ClientError as e:
            logger.error("Error checking asset {} status: {}".format(asset_id, e))
            time.sleep(5)

    logger.error("Timeout waiting for asset {} to become ACTIVE".format(asset_id))
    return False


def wait_for_asset_model_active(client, asset_model_id, timeout=300):
    """Wait for an asset model to become ACTIVE."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = client.describe_asset_model(assetModelId=asset_model_id)
            state = response["assetModelStatus"]["state"]

            if state == "ACTIVE":
                return True
            elif state == "FAILED":
                logger.error("Asset model {} failed to activate".format(asset_model_id))
                return False

            time.sleep(5)

        except ClientError as e:
            logger.error("Error checking asset model {} status: {}".format(asset_model_id, e))
            time.sleep(5)

    logger.error("Timeout waiting for asset model {} to become ACTIVE".format(asset_model_id))
    return False
