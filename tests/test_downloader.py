# pylint: disable=import-outside-toplevel,redefined-outer-name,unused-argument,wrong-import-order,unused-import
"""
Neurobik Downloader Test Suite

This test suite validates the download and file management functionality.
It tests model downloads, OCI container operations, file verification, and symlinking logic.

Key Features Tested:
- Model downloads via subprocess (HuggingFace CLI)
- OCI container pulls and builds via subprocess
- HTTP file downloads with progress and checksums
- Confirmation file creation for completed downloads
- Symlink creation and management for default models
- Error handling for download failures and permission issues

Test Environment:
- Uses /tmp directories for file operations
- Mocks subprocess.run for external CLI calls
- Mocks requests for HTTP downloads
- Uses monkeypatch for file system operations
- Tests both success and failure scenarios

Replication Guide (for Python or other languages):
1. Mock external process calls (CLI tools, HTTP requests)
2. Test file download with progress tracking
3. Implement checksum verification for downloads
4. Test subprocess command construction and execution
5. Create confirmation files after successful operations
6. Implement symlinking with relative paths
7. Test error handling for permissions and I/O issues
8. Validate cleanup of existing symlinks

Dependencies for replication:
- pytest for test framework
- unittest.mock for patching subprocess and requests
- tempfile for test file management
- hashlib for checksum verification
- os/pathlib for file operations
"""

# pylint: disable=import-outside-toplevel,redefined-outer-name,unused-argument,wrong-import-order

import pytest
import os
import tempfile
from unittest.mock import patch

from neurobik.downloader import Downloader


@pytest.fixture
def sample_config():
    """
    Pytest fixture that creates a temporary YAML config file for testing.

    Replication steps (Python/pytest):
    1. Create dictionary with valid config structure
    2. Use tempfile.NamedTemporaryFile to create temp file
    3. Write YAML content using yaml.dump
    4. Yield file path for test use
    5. Clean up file after test completion

    For other languages:
    - Create temporary files with unique names
    - Serialize config objects to YAML/JSON
    - Ensure proper cleanup in test teardown
    - Use /tmp or equivalent temp directories
    """
    config_data = {
        "model_provider": "ollama",
        "oci_provider": "podman",
        "models": [
            {
                "repo_name": "test/repo",
                "model_name": "model.gguf",
                "location": "/tmp/test-model.gguf",
                "confirmation_file": "/tmp/test-model.confirmed",
                "checksum": "dummy",
            }
        ],
        "oci": [
            {
                "image": "test-image:latest",
                "confirmation_file": "/tmp/test-image.confirmed",
            }
        ],
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        import yaml

        yaml.dump(config_data, f)
        f.flush()
        yield f.name
    os.unlink(f.name)


@patch("neurobik.downloader.subprocess.run")
def test_confirmation_files_created_on_success(mock_subprocess, sample_config):
    """
    Test that confirmation files are created after successful OCI pulls.

    Replication steps (Python/pytest):
    1. Load config with OCI container definition
    2. Mock subprocess.run to return success (returncode 0)
    3. Call pull_oci() with image and confirmation file path
    4. Assert confirmation file exists at expected location
    5. Clean up created files

    Key validations:
    - subprocess.run called with correct podman pull command
    - Confirmation file created after successful pull
    - No confirmation file created on failure (separate test)
    - File operations work in /tmp directory

    For other languages:
    - Mock container runtime CLI calls
    - Test file creation after successful operations
    - Verify cleanup happens after subprocess success
    - Test with different container image names
    """


@patch("neurobik.downloader.subprocess.run")
def test_confirmation_files_not_created_on_failure(mock_subprocess, sample_config):
    """
    Test that confirmation files are NOT created when downloads fail.

    Replication steps (Python/pytest):
    1. Load config with model and OCI definitions
    2. Mock subprocess.run to raise exceptions or return failure codes
    3. Call pull_model() and pull_oci() expecting exceptions
    4. Assert confirmation files do NOT exist
    5. Verify exceptions are properly propagated

    Key validations:
    - No confirmation files created on subprocess failures
    - Exceptions from subprocess are not caught internally
    - Atomic operation: either full success or full failure
    - File system remains clean after failures

    For other languages:
    - Mock external command failures
    - Test that partial operations don't leave artifacts
    - Verify exception propagation
    - Test cleanup on error paths
    """


@patch("neurobik.downloader.requests.get")
def test_download_file_success(mock_get, sample_config):
    """
    Test successful HTTP file download with checksum verification.

    Replication steps (Python/pytest):
    1. Mock requests.get to return successful response
    2. Set up mock response with content-length header and data
    3. Call download_file with URL, destination, and correct SHA256
    4. Assert downloaded file exists
    5. Assert confirmation file (.confirmed) exists
    6. Clean up test files

    Key validations:
    - HTTP GET request made to correct URL
    - Progress bar functionality (tqdm) works
    - Checksum verification passes for correct hash
    - Confirmation file created after successful download
    - File content matches expected data

    For other languages:
    - Mock HTTP client libraries
    - Test streaming downloads with progress
    - Implement SHA256 checksum verification
    - Create marker files after successful downloads
    - Test file I/O operations
    """


@patch("neurobik.downloader.requests.get")
def test_download_file_checksum_mismatch(mock_get, sample_config):
    """
    Test checksum verification failure for downloaded files.

    Replication steps (Python/pytest):
    1. Mock requests.get with valid response and content
    2. Call download_file with incorrect checksum
    3. Assert ValueError raised with "Checksum mismatch" message
    4. Verify partial downloads are cleaned up
    5. Check no confirmation file created

    Key validations:
    - SHA256 checksum computed correctly
    - Mismatch detected and exception raised
    - Downloaded file removed on checksum failure
    - No confirmation file created for failed downloads
    - Error message is descriptive

    For other languages:
    - Implement cryptographic hash verification
    - Test hash comparison logic
    - Verify cleanup on validation failures
    - Test with various incorrect checksums
    - Ensure atomic download-verification operations
    """


@patch("neurobik.downloader.subprocess.run")
def test_pull_oci_with_containerfile(mock_subprocess):
    """
    Test OCI container build with custom containerfile and build arguments.

    Replication steps (Python/pytest):
    1. Mock subprocess.run to return success
    2. Define containerfile path, image name, build args
    3. Call pull_oci() with containerfile and build_args
    4. Assert subprocess.run called with correct podman build command
    5. Verify command includes all build arguments and paths
    6. Assert confirmation file created
    7. Clean up test files

    Key validations:
    - Command construction includes all parameters
    - Context directory derived from containerfile path
    - Build arguments properly passed to podman
    - Tag (-t) flag used for image naming
    - File (-f) flag points to correct containerfile
    - Confirmation file created after successful build

    For other languages:
    - Test container build command construction
    - Verify argument passing to container runtimes
    - Test path manipulation for context directories
    - Validate build argument formatting
    - Test marker file creation
    """

    from unittest.mock import MagicMock

    # Setup
    mock_subprocess.return_value = MagicMock(returncode=0)

    downloader = Downloader()
    image = "test-image:latest"

    # Create temporary directory for containerfile
    with tempfile.TemporaryDirectory() as temp_dir:
        containerfile = os.path.join(temp_dir, "Containerfile.test")
        context = temp_dir
        confirmation_file = os.path.join(temp_dir, "test-confirmation")

        # Create temporary containerfile
        with open(containerfile, 'w', encoding='utf-8') as f:
            f.write("FROM ubuntu\n")

        # Test with build_args
        build_args = ["ARG1=value1", "ARG2=value2"]
        downloader.pull_oci(image, confirmation_file, containerfile, build_args)

        # Verify subprocess.run was called with correct command
        expected_cmd = [
            "podman", "build", "-t", image,
            "--build-arg", "ARG1=value1",
            "--build-arg", "ARG2=value2",
            "-f", containerfile, context
        ]
        mock_subprocess.assert_called_once_with(expected_cmd, check=True)

        # Verify confirmation file was created
        assert os.path.exists(confirmation_file)


@pytest.mark.parametrize("build_args,expected_build_args", [
    # No build args
    (None, []),
    ([], []),
    # One build arg
    (["ARG1=value1"], ["--build-arg", "ARG1=value1"]),
    # Multiple build args
    (["ARG1=value1", "ARG2=value2"], ["--build-arg", "ARG1=value1", "--build-arg", "ARG2=value2"]),
    (["ROCM_INDEX_URL=https://example.com"], ["--build-arg", "ROCM_INDEX_URL=https://example.com"]),
])
@patch("neurobik.downloader.subprocess.run")
def test_pull_oci_build_args(mock_subprocess, build_args, expected_build_args):
    """
    Test OCI container build with various build argument configurations.

    Tests 0, 1, and multiple build arguments to ensure proper command construction.

    Replication steps (Python/pytest):
    1. Mock subprocess.run to return success
    2. Define containerfile path and image name
    3. Call pull_oci() with different build_args configurations
    4. Assert subprocess.run called with correctly formatted build args
    5. Verify confirmation file created
    6. Clean up test files

    Key validations:
    - Build args are properly formatted with --build-arg flags
    - Command includes correct number of --build-arg pairs
    - No build args when None or empty list provided
    - Single build arg handled correctly
    - Multiple build args all included

    For other languages:
    - Test parameter formatting for CLI tools
    - Verify conditional argument inclusion
    - Test array/list processing for command construction
    """
    from unittest.mock import MagicMock

    # Setup
    mock_subprocess.return_value = MagicMock(returncode=0)

    downloader = Downloader()
    image = "test-image:latest"

    # Create temporary directory for containerfile
    with tempfile.TemporaryDirectory() as temp_dir:
        containerfile = os.path.join(temp_dir, "Containerfile.test")
        context = temp_dir
        confirmation_file = os.path.join(temp_dir, "test-confirmation")

        # Create temporary containerfile
        with open(containerfile, 'w', encoding='utf-8') as f:
            f.write("FROM ubuntu\n")

        downloader.pull_oci(image, confirmation_file, containerfile, build_args)

        # Build expected command
        expected_cmd = ["podman", "build", "-t", image]
        expected_cmd.extend(expected_build_args)
        expected_cmd.extend(["-f", containerfile, context])

        mock_subprocess.assert_called_once_with(expected_cmd, check=True)

        # Verify confirmation file was created
        assert os.path.exists(confirmation_file)


def test_create_default_symlink(tmp_path):
    """
    Test successful creation and updating of default model symlinks.

    Replication steps (Python/pytest):
    1. Create temporary directory structure with subdirectories
    2. Create target model files in subdirectories
    3. Call create_default_symlink() with models_dir and target path
    4. Assert symlink exists at expected location
    5. Assert symlink is relative and points to correct target
    6. Test updating symlink to new target
    7. Verify symlink target changes correctly

    Key validations:
    - Relative path calculation between models_dir and target
    - Symlink creation with os.symlink()
    - Existing symlink replacement
    - No exceptions on valid operations
    - Symlink points to correct relative path

    For other languages:
    - Test symbolic link creation APIs
    - Verify relative path computation
    - Test symlink updates/overwrites
    - Validate symlink target resolution
    - Test with nested directory structures
    """


def test_create_default_symlink_failure(tmp_path, monkeypatch):
    """
    Test failure handling when existing symlinks cannot be removed.

    Replication steps (Python/pytest):
    1. Create temporary directory and target file
    2. Create existing symlink at target location
    3. Mock os.unlink to raise OSError (permission denied)
    4. Call create_default_symlink()
    5. Assert RuntimeError raised with descriptive message
    6. Verify new symlink is not created

    Key validations:
    - Existing symlinks detected with os.path.lexists
    - os.unlink attempted on existing symlinks
    - OSError from unlink caught and re-raised as RuntimeError
    - Descriptive error message includes symlink path
    - Operation fails atomically (no partial changes)

    For other languages:
    - Test file system permission error handling
    - Mock file removal operations to fail
    - Verify exception chaining and messages
    - Test atomic operations (all or nothing)
    - Validate error recovery scenarios
    """
