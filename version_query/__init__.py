"""Package marker for version_query package."""

import logging
import os

if 'LOGGING_LEVEL' in os.environ:
    logging.basicConfig(level=getattr(logging, os.environ['LOGGING_LEVEL'].upper()))

import warnings
from .determine import determine_caller_version
from .increment import increment_caller_version
from .version import VersionOld

def generate_version_str(increment_if_repo_chnaged: bool = True) -> str:
    """Generate the version string for current/upcoming version of the package."""
    warnings.warn('function deprecated', DeprecationWarning, stacklevel=2)
    if increment_if_repo_chnaged:
        try:
            return VersionOld.generate_str(*increment_caller_version(2))
        except ValueError:
            pass
    return VersionOld.generate_str(*determine_caller_version(2))


from .query import query_version_str, predict_version_str
from .version import Version
