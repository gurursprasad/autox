from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("autox")
except PackageNotFoundError:
    # When running from source (not installed), fall back to a sensible default.
    __version__ = "0.1.0"

from .config import config

__all__ = ["__version__", "config"]
