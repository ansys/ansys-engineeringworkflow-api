from __future__ import annotations
from abc import ABC, abstractmethod
from os import PathLike
from typing import Union, Mapping, AbstractSet, Optional, Collection

from ansys.common.variableinterop import IVariableValue, CommonVariableMetadata
from .datatypes import *


class IAsyncWorkflowEngine(ABC):
    """Interface defines the common behavior for an engineering workflow engine that can run and monitor instances"""

    @abstractmethod
    async def get_server_info(self) -> WorkflowEngineInfo:
        ...


class IAsyncDesktopWorkflowEngine(IAsyncWorkflowEngine, ABC):
    """Extends IWorkflowEngine with calls that are relevant for a desktop workflow engine, such has handling local files"""

    @abstractmethod
    async def load_workflow(self, file_name: Union[PathLike, str]) -> IAsyncWorkflowInstance:
        ...


class IAsyncWorkflowInstance(ABC):
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
    async def get_root(self) -> IAsyncControlStatement:
        ...

    @abstractmethod
    async def get_element_by_id(self, element_id: str) -> IAsyncElement:
        ...


class IAsyncElement(ABC):
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


class IAsyncVariableContainer(ABC):
    """An abstract base class for something that can contain variables"""

    @abstractmethod
    async def get_variables(self) -> Collection[IAsyncVariable]:
        ...


class IAsyncControlStatement(IAsyncElement, IAsyncVariableContainer, ABC):
    """
    An element in the workflow that contains children and controls how those children will be executed.

    Examples are: sequential, parallel, looping, conditional, Trade Study.
    """

    @property
    @abstractmethod
    def control_type(self) -> str:
        ...

    @abstractmethod
    async def get_components(self) -> Collection[IAsyncElement]:
        ...


class IAsyncComponent(IAsyncElement, IAsyncVariableContainer, ABC):
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


class IAsyncVariable(IAsyncElement, ABC):
    """
    A runtime placeholder for some value of a particular type.

    Will change as the workflow runs and can be linked to other variables via direct links or equations
    """

    @abstractmethod
    async def get_metadata(self) -> CommonVariableMetadata:
        ...

    @abstractmethod
    async def get_value(self, hid: Optional[str]) -> VariableState:
        ...

    @abstractmethod
    async def set_value(self, value: VariableState) -> None:
        ...


