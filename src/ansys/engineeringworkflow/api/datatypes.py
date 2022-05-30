from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from ansys.common.variableinterop import IVariableValue


@dataclass(frozen=True)
class WorkflowEngineInfo:
    """Information about a workflow engine as collected by get_server_info call"""

    # TODO: this style documentation does not appear to be working?
    release_year: int
    """The year portion of the release, such as 2022"""
    release_id: int
    """release_id"""
    build: int
    """The build number"""
    is_release_build: bool
    """True for production releases. False for development, alpha, beta, and other releases"""
    build_type: str
    """The build type. Must be blank for production releases. May include arbitrary information
    like the branch a development build was built from."""
    version_as_string: str
    """The version of the workflow engine encoded for human consumption. For example: 
    2022r1 build 333 ALPHA"""
    server_type: str
    """What server type is responding to this request. Will be a string similar to
    'optiSLang' or 'ModelCenter'"""


@dataclass(frozen=True)
class DesktopWorkflowEngineInfo(WorkflowEngineInfo):
    """Information about a workflow engine that is specific to a desktop product installation"""
    install_location: str


@dataclass(frozen=True)
class ServerWorkflowEngineInfo(WorkflowEngineInfo):
    """Information about a workflow engine that is specific to a cloud product installation"""
    base_url: str  # Should this be some type of URL class?


class WorkflowInstanceState(Enum):
    """The state that a workflow instance can be in"""
    UNKNOWN = 0
    INVALID = 1
    RUNNING = 2
    PAUSED = 3
    FAILED = 4
    SUCCESS = 5


class VariableValueInvalidException(AttributeError):
    """TODO: This belongs in variableinterop"""
    pass


@dataclass(frozen=True)
class VariableState:
    """TODO: This belongs in variableinterop"""
    is_valid: bool
    value: IVariableValue

    @property
    def safe_value(self) -> IVariableValue:
        if not self.is_valid:
            raise VariableValueInvalidException()
        return self.value


@dataclass(frozen=True)
class Property:
    """
    A configurable setting on some component or algorithm in the workflow.

    Cannot be linked to other variables or properties. Unless a property is explicitly, documented as supporting it, these values
    should not be changed while the workflow is running. Examples that may support modification would be convergence criteria for
    an optimization algorithm.
    """

    parent_element_id: str
    property_name: str
    property_value: IVariableValue

