from pathlib import Path
from unittest import mock
import os

from container_detect.core import is_inside_container


def test_detects_via_dockerenv():
    """Test detection via /.dockerenv file."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=(path_str == "/.dockerenv"))
        return mock_path

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=FileNotFoundError()), \
         mock.patch.dict(os.environ, {}, clear=True):
        assert is_inside_container(force_refresh=True) is True


def test_detects_via_containerenv():
    """Test detection via /.containerenv file (Podman)."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=(path_str == "/.containerenv"))
        return mock_path

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=FileNotFoundError()), \
         mock.patch.dict(os.environ, {}, clear=True):
        assert is_inside_container(force_refresh=True) is True


def test_detects_via_run_containerenv():
    """Test detection via /run/.containerenv file (Podman)."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=(path_str == "/run/.containerenv"))
        return mock_path

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=FileNotFoundError()), \
         mock.patch.dict(os.environ, {}, clear=True):
        assert is_inside_container(force_refresh=True) is True


def test_detects_via_cgroup_docker():
    """Test detection via cgroup file with docker keyword."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=False)
        return mock_path

    def file_open(path, mode="rt"):
        if path == "/proc/self/cgroup":
            return mock.mock_open(read_data="xxx docker yyyy")(path, mode)
        raise FileNotFoundError()

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=file_open), \
         mock.patch.dict(os.environ, {}, clear=True):
        assert is_inside_container(force_refresh=True) is True


def test_detects_via_cgroup_kubepods():
    """Test detection via cgroup file with kubepods keyword."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=False)
        return mock_path

    def file_open(path, mode="rt"):
        if path == "/proc/self/cgroup":
            return mock.mock_open(read_data="kubepods/burstable/pod123")(path, mode)
        raise FileNotFoundError()

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=file_open), \
         mock.patch.dict(os.environ, {}, clear=True):
        assert is_inside_container(force_refresh=True) is True


def test_detects_via_cgroup_podman():
    """Test detection via cgroup file with podman keyword."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=False)
        return mock_path

    def file_open(path, mode="rt"):
        if path == "/proc/1/cgroup":
            return mock.mock_open(read_data="libpod-podman")(path, mode)
        raise FileNotFoundError()

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=file_open), \
         mock.patch.dict(os.environ, {}, clear=True):
        assert is_inside_container(force_refresh=True) is True


def test_detects_via_mountinfo():
    """Test detection via mountinfo file."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=False)
        return mock_path

    def file_open(path, mode="rt"):
        if path == "/proc/self/cgroup":
            return mock.mock_open(read_data="0::/")(path, mode)  # Cgroups v2 format
        if path == "/proc/self/mountinfo":
            return mock.mock_open(read_data="1234 24 0:6 /docker/containers/abc123/hostname /etc/hostname rw,nosuid")(path, mode)
        raise FileNotFoundError()

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=file_open), \
         mock.patch.dict(os.environ, {}, clear=True):
        assert is_inside_container(force_refresh=True) is True


def test_detects_via_kubernetes_env():
    """Test detection via KUBERNETES_SERVICE_HOST environment variable."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=False)
        return mock_path

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=FileNotFoundError()), \
         mock.patch.dict(os.environ, {"KUBERNETES_SERVICE_HOST": "10.0.0.1"}):
        assert is_inside_container(force_refresh=True) is True


def test_detects_via_docker_container_env():
    """Test detection via DOCKER_CONTAINER environment variable."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=False)
        return mock_path

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=FileNotFoundError()), \
         mock.patch.dict(os.environ, {"DOCKER_CONTAINER": "true"}):
        assert is_inside_container(force_refresh=True) is True


def test_detects_via_podman_container_env():
    """Test detection via PODMAN_CONTAINER environment variable."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=False)
        return mock_path

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=FileNotFoundError()), \
         mock.patch.dict(os.environ, {"PODMAN_CONTAINER": "1"}):
        assert is_inside_container(force_refresh=True) is True


def test_detects_via_ecs_env():
    """Test detection via ECS_CONTAINER_METADATA_URI environment variable."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=False)
        return mock_path

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=FileNotFoundError()), \
         mock.patch.dict(os.environ, {"ECS_CONTAINER_METADATA_URI": "http://169.254.170.2/v3/metadata"}):
        assert is_inside_container(force_refresh=True) is True


def test_not_inside_container():
    """Test negative case - not inside container."""
    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)
        mock_path.exists = mock.Mock(return_value=False)
        return mock_path

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=FileNotFoundError()), \
         mock.patch.dict(os.environ, {}, clear=True):
        assert is_inside_container(force_refresh=True) is False


def test_returns_false_on_non_linux_platforms():
    """Test that is_inside_container returns False on non-Linux platforms."""
    with mock.patch("sys.platform", "darwin"):  # macOS
        assert is_inside_container(force_refresh=True) is False
        assert is_inside_container() is False

    with mock.patch("sys.platform", "win32"):  # Windows
        assert is_inside_container(force_refresh=True) is False
        assert is_inside_container() is False


def test_caching_works_correctly():
    """Test that caching works correctly - subsequent calls use cache."""
    stat_call_count = 0
    read_call_count = 0

    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)

        def exists():
            nonlocal stat_call_count
            stat_call_count += 1
            return False

        def file_open(path, mode="rt"):
            nonlocal read_call_count
            read_call_count += 1
            if path == "/proc/self/cgroup":
                return mock.mock_open(read_data="xxx docker yyyy")(path, mode)
            raise FileNotFoundError()

        mock_path.exists = mock.Mock(side_effect=exists)
        return mock_path

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=file_open), \
         mock.patch.dict(os.environ, {}, clear=True):
        # First call - force refresh to start fresh
        assert is_inside_container(force_refresh=True) is True
        assert stat_call_count >= 1
        assert read_call_count >= 1

        # Second call - should use cache
        assert is_inside_container() is True
        initial_stat_count = stat_call_count
        initial_read_count = read_call_count

        # Third call - should still use cache
        assert is_inside_container() is True
        assert stat_call_count == initial_stat_count  # Should not increase
        assert read_call_count == initial_read_count  # Should not increase


def test_force_refresh_clears_cache_and_rechecks():
    """Test that force_refresh=True actually clears cache and re-runs the check."""
    from container_detect.core import _is_inside_container_cached

    check_count = 0

    def path_constructor(*args, **kwargs):
        path_str = str(args[0]) if args else ""
        mock_path = mock.MagicMock(spec=Path)
        mock_path.__str__ = mock.Mock(return_value=path_str)

        def exists():
            nonlocal check_count
            check_count += 1
            return (path_str == "/.dockerenv")

        mock_path.exists = mock.Mock(side_effect=exists)
        return mock_path

    with mock.patch("sys.platform", "linux"), \
         mock.patch("container_detect.core.Path", side_effect=path_constructor), \
         mock.patch("builtins.open", side_effect=FileNotFoundError()), \
         mock.patch.dict(os.environ, {}, clear=True):
        # Clear any existing cache first
        _is_inside_container_cached.cache_clear()

        # First call - should check
        assert is_inside_container() is True
        assert check_count == 1

        # Second call - should use cache
        assert is_inside_container() is True
        assert check_count == 1  # Should not increase

        # Third call with force_refresh - should clear cache and re-check
        assert is_inside_container(force_refresh=True) is True
        assert check_count == 2  # Should increase

        # Fourth call - should use cache again
        assert is_inside_container() is True
        assert check_count == 2  # Should not increase
