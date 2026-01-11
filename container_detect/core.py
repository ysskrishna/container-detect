"""Core container detection functionality."""
import os
from functools import lru_cache
from pathlib import Path
import sys


@lru_cache(maxsize=1)
def _is_inside_container_cached() -> bool:
    """
    Internal cached implementation of container detection.
    
    Returns:
        True if running inside a container, False otherwise.
    """
    if not sys.platform.startswith("linux"):
        return False

    # 1. Check for /.dockerenv (Docker classic, some Podman)
    if Path("/.dockerenv").exists():
        return True

    # 2. Check for container-specific files
    container_files = [
        "/.containerenv",  # Podman
        "/run/.containerenv",  # Podman alternative location
    ]
    if any(Path(f).exists() for f in container_files):
        return True

    # 3. Check cgroup (works for Docker, Kubernetes, containerd, Podman, LXC)
    cgroup_files = ["/proc/self/cgroup", "/proc/1/cgroup"]
    keywords = (
        "docker",
        "kubepods",
        "kubelet",
        "containerd",
        "podman",
        "libpod",
        "cri-o",
        "lxc",
        "garden",
    )

    for cgroup_file in cgroup_files:
        try:
            with open(cgroup_file, "rt") as f:
                content = f.read()
                if any(k in content.lower() for k in keywords):
                    return True
        except (FileNotFoundError, PermissionError, OSError):
            continue

    # 4. Check mountinfo for container filesystem patterns
    try:
        with open("/proc/self/mountinfo", "rt") as f:
            content = f.read()
            if any(k in content for k in ("docker", "kubelet", "containerd", "podman")):
                return True
    except (FileNotFoundError, PermissionError, OSError):
        pass

    # 5. Environment variables commonly set in containers
    container_env_vars = (
        "KUBERNETES_SERVICE_HOST",  # Kubernetes
        "KUBERNETES_PORT",  # Kubernetes
        "container",  # systemd-based containers
        "DOCKER_CONTAINER",  # Sometimes set
        "PODMAN_CONTAINER",  # Podman
        "ECS_CONTAINER_METADATA_URI",  # AWS ECS
    )
    if any(var in os.environ for var in container_env_vars):
        return True

    return False


def is_inside_container(force_refresh: bool = False) -> bool:
    """
    Return True if the current process is running inside a container.
    
    Detects multiple container types including Docker, Podman, Kubernetes,
    containerd, LXC, and others.
    
    Linux-only detection. Returns False on macOS and Windows.
    
    Args:
        force_refresh: If True, bypass the cache and perform a fresh check.
                       Defaults to False.
    
    Returns:
        True if running inside a container, False otherwise.
    
    Examples:
        >>> is_inside_container()  # Uses cache
        False
        >>> is_inside_container(force_refresh=True)  # Bypasses cache
        False
    """
    if force_refresh:
        _is_inside_container_cached.cache_clear()
    return _is_inside_container_cached()
