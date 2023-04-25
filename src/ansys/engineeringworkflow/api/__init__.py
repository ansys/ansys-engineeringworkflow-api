"""This package contains a common API specification for all automated \
engineering workflow engines at Ansys."""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

from .datatypes import *
from .exceptions import *
from .iasyncworkflow import *
from .iworkflow import *
