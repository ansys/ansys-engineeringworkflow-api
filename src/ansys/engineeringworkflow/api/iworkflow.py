from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from os import PathLike
from typing import Union, Mapping, AbstractSet, Optional, Collection

from ansys.common.variableinterop import IVariableValue, CommonVariableMetadata


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


class IWorkflowEngine(ABC):
    """Interface defines the common behavior for an engineering workflow engine that can run and monitor instances"""
    @abstractmethod
    async def get_server_info(self) -> WorkflowEngineInfo:
        ...


class IDesktopWorkflowEngine(IWorkflowEngine, ABC):
    """Extends IWorkflowEngine with calls that are relevant for a desktop workflow engine, such has handling local files"""
    @abstractmethod
    async def load_workflow(self, file_name: Union[PathLike, str]) -> IWorkflowInstance:
        ...


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


class IWorkflowInstance(ABC):
    """Representation of an instantiated workflow instance"""
    
    @abstractmethod
    async def get_state(self) -> WorkflowInstanceState:
        ...

    @abstractmethod
    async def run(self, inputs: Mapping[str, VariableState], reset: bool,
                  validation_ids: AbstractSet[str]) -> Mapping[str, VariableState]:
        ...

    @abstractmethod
    async def start_run(self, inputs: Mapping[str, VariableState], reset: bool,
                        validation_ids: AbstractSet[str]) -> str:
        ...

    # TODO: How to wait for finish in second case?

    @abstractmethod
    async def get_root(self) -> IControlStatement:
        ...

    @abstractmethod
    async def get_element_by_id(self, element_id: str) -> IElement:
        ...


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


class IElement(ABC):
    """Any one of Component, Control Statement, or Variable"""
    
    @property
    @abstractmethod
    def element_id(self) -> str:
        ...

    @property
    @abstractmethod
    def parent_element_id(self) -> str:
        ...

    @property
    @abstractmethod
    def name(self):
        ...

    @abstractmethod
    async def get_property(self, property_name: str) -> Property:
        ...

    @abstractmethod
    async def get_properties(self) -> Collection[Property]:
        ...

    @abstractmethod
    async def set_property(self, property_name: str, property_value: IVariableValue) -> None:
        ...


# TODO: Should control statements extend component?


class IVariableContainer(ABC):
    """An abstract base class for somethign that can contain variables"""
    @abstractmethod
    async def get_variables(self) -> Collection[IVariable]:
        ...


class IControlStatement(IElement, IVariableContainer, ABC):
    """
    An element in the workflow that contains children and controls how those children will be executed. 
    
    Examples are: sequential, parallel, looping, conditional, Trade Study.
    """
    
    @property
    @abstractmethod
    def control_type(self) -> str:
        ...

    @abstractmethod
    async def get_components(self) -> Collection[IElement]:
        ...


class IComponent(IElement, IVariableContainer, ABC):
    """
    A black box analysis is defined as taking a set of inputs, executing, and resulting in a set of outputs. 
    
    May be a solver, simulation, co-simulation, calculation, or other third party analysis. While state may be kept as an optimization to help 
    performance for slow to start tools, the component definition does not require it so that we can parallelize the work onto an HPC cluster.
    Synonymous in our context with Integrations and Analysis. This is the preferred go forward term to use in APIs and documentation about 
    Engineering Workflow
    """

    @property
    @abstractmethod
    def pacz_url(self):
        ...

# TODO: We may want specific variable types that refine get/set value to specific variableinterop types?


class IVariable(IElement, ABC):
    """
    A runtime placeholder for some value of a particular type. 
    
    Will change as the workflow runs and can be linked to other variables via direct links or equations
    """
    
    @property
    @abstractmethod
    def metadata(self) -> CommonVariableMetadata:
        ...

    @abstractmethod
    async def get_value(self, hid: Optional[str]) -> VariableState:
        ...

    @abstractmethod
    async def set_value(self, value: VariableState) -> None:
        ...
