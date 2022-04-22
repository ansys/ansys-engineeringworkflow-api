from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from os import PathLike
from typing import Union, Mapping, AbstractSet, Optional, Collection

from ansys.common.variableinterop import IVariableValue, CommonVariableMetadata


@dataclass(frozen=True)
class WorkflowEngineInfo:
    """TODO: Document"""

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
    install_location: str


@dataclass(frozen=True)
class ServerWorkflowEngineInfo(WorkflowEngineInfo):
    base_url: str  # Should this be some type of URL class?


class IWorkflowEngine(ABC):
    @abstractmethod
    async def get_server_info(self) -> WorkflowEngineInfo:
        ...


class IDesktopWorkflowEngine(IWorkflowEngine, ABC):
    @abstractmethod
    async def load_workflow(self, file_name: Union[PathLike, str]) -> IWorkflowInstance:
        ...


class WorkflowInstanceState(Enum):
    UNKNOWN = 0
    INVALID = 1
    RUNNING = 2
    PAUSED = 3
    FAILED = 4
    SUCCESS = 5


class VariableValueInvalidException(AttributeError):
    pass


@dataclass(frozen=True)
class VariableState:
    is_valid: bool
    value: IVariableValue

    @property
    def safe_value(self) -> IVariableValue:
        if not self.is_valid:
            raise VariableValueInvalidException()
        return self.value


class IWorkflowInstance(ABC):
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
    parent_element_id: str
    property_name: str
    property_value: IVariableValue


class IElement(ABC):
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
    @abstractmethod
    async def get_variables(self) -> Collection[IVariable]:
        ...


class IControlStatement(IElement, IVariableContainer, ABC):
    @property
    @abstractmethod
    def control_type(self) -> str:
        ...

    @abstractmethod
    async def get_components(self) -> Collection[IElement]:
        ...


class IComponent(IElement, IVariableContainer, ABC):
    @property
    @abstractmethod
    def pacz_url(self):
        ...


class IVariable(IElement, ABC):
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
