# Container Detect

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/ysskrishna/container-detect/blob/main/LICENSE)
[![Tests](https://github.com/ysskrishna/container-detect/actions/workflows/test.yml/badge.svg)](https://github.com/ysskrishna/container-detect/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/container-detect)](https://pypi.org/project/container-detect/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/container-detect?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/container-detect)
[![Author site](https://img.shields.io/badge/author-ysskrishna.space-informational)](https://ysskrishna.space)
[![Context7](https://img.shields.io/badge/Context7-docs-18181B)](https://context7.com/ysskrishna/container-detect)
[![Ask DeepWiki](https://img.shields.io/badge/DeepWiki-ask-18181B)](https://deepwiki.com/ysskrishna/container-detect)

Detect if your Python process is running inside a container. Supports Docker, Podman, Kubernetes, containerd, LXC, and more. Inspired by the popular [is-inside-container](https://github.com/sindresorhus/is-inside-container) npm package. Supports cached results with optional refresh.

## Features

- Fast and reliable container detection for multiple container types
- Supports Docker, Podman, Kubernetes, containerd, LXC, and more
- Multiple detection methods for robustness
- Cached results for performance optimization
- Zero dependencies, minimal overhead
- Type hints for better IDE support
- Graceful error handling

## Supported Container Types

- **Docker** - Classic Docker containers
- **Podman** - Podman containers
- **Kubernetes** - Kubernetes pods
- **containerd** - containerd containers
- **LXC** - Linux Containers
- **CRI-O** - Container Runtime Interface
- **AWS ECS** - Amazon Elastic Container Service
- And more container runtimes

## Installation

```bash
pip install container-detect
```

Or using `uv`:

```bash
uv add container-detect
```

## Usage

### Check if running inside a container

```python
from container_detect import is_inside_container

if is_inside_container():
    print("Running inside a container")
else:
    print("Not running inside a container")
```

### Force refresh cache

```python
from container_detect import is_inside_container

# Use cached result (default)
is_inside_container()  # Fast, uses cache

# Force a fresh check, bypassing cache
is_inside_container(force_refresh=True)  # Performs new detection
```


## API Reference

Install with `pip install container-detect` and import from `container_detect`. Signatures and descriptions below match the source code of `container_detect`.

### `is_inside_container(force_refresh: bool = False) -> bool`

Return True if the current process is running inside a container.

Detects multiple container types including Docker, Podman, Kubernetes,
containerd, LXC, and others.

Linux-only detection. Returns False on macOS and Windows.

**Parameters**

- `force_refresh`: If True, bypass the cache and perform a fresh check. Defaults to False.

**Returns**

- True if running inside a container, False otherwise.

**Example**

```python
from container_detect import is_inside_container

is_inside_container()  # False  (Uses cache)
is_inside_container(force_refresh=True)  # False  (Bypasses cache)
```

## Credits

This package is inspired by the [is-inside-container](https://github.com/sindresorhus/is-inside-container) ([npm](https://www.npmjs.com/package/is-inside-container)) npm package by [Sindre Sorhus](https://github.com/sindresorhus).

## Contributing

Contributions are welcome! Please read our [Contributing Guide](https://github.com/ysskrishna/container-detect/blob/main/CONTRIBUTING.md) for details on our code of conduct, development setup, and the process for submitting pull requests.

## Built and maintained by

Container Detect is built and maintained by:

| | Name | GitHub | Role |
|---|------|--------|------|
| <img src="https://github.com/ysskrishna.png?size=120" width="60" height="60" alt="Y. Siva Sai Krishna"> | **Y. Siva Sai Krishna** | [@ysskrishna](https://github.com/ysskrishna) | Creator |

## Changelog

See [CHANGELOG](CHANGELOG.md) for release history.

## Support

If you find this library helpful:

- ⭐ Star the repository
- 🐛 [Report issues](https://github.com/ysskrishna/container-detect/issues)
- 🔀 Submit pull requests
- 💝 [Sponsor on GitHub](https://github.com/sponsors/ysskrishna)

## License

MIT © [Y. Siva Sai Krishna](https://github.com/ysskrishna) — see [LICENSE](LICENSE) for details.

---

<p align="left">
  <a href="https://github.com/ysskrishna">Author's GitHub</a> •
  <a href="https://linkedin.com/in/ysskrishna">Author's LinkedIn</a> •
  <a href="https://ysskrishna.space">Author's site</a> •
  <a href="https://pypi.org/project/container-detect/">Package on PyPI</a> •
  <a href="https://github.com/ysskrishna/container-detect/issues">Report Issues</a>
</p>
