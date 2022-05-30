from __future__ import annotations

from abc import ABC, abstractmethod
from os import PathLike
from typing import AbstractSet, Collection, Mapping, Optional, Union

from ansys.common.variableinterop import CommonVariableMetadata, IVariableValue

from .datatypes import *


class IWorkflowEngine(ABC):
    """Interface defines the common behavior for an engineering workflow engine that can run and
     monitor instances"""

    @abstractmethod
    def get_server_info(self) -> WorkflowEngineInfo:
        ...


class IDesktopWorkflowEngine(IWorkflowEngine, ABC):
    """Extends IWorkflowEngine with calls that are relevant for a desktop workflow engine, such
     has handling local files"""

    @abstractmethod
    def load_workflow(self, file_name: Union[PathLike, str]) -> IWorkflowInstance:
        ...


class IWorkflowInstance(ABC):
    """Representation of an instantiated workflow instance"""

    @abstractmethod
    def get_state(self) -> WorkflowInstanceState:
        ...

    @abstractmethod
    def run(self, inputs: Mapping[str, VariableState], reset: bool,
            validation_ids: AbstractSet[str]) -> Mapping[str, VariableState]:
        ...

    @abstractmethod
    def start_run(self, inputs: Mapping[str, VariableState], reset: bool,
                  validation_ids: AbstractSet[str]) -> str:
        ...

    # TODO: How to wait for finish in second case?

    @abstractmethod
    def get_root(self) -> IControlStatement:
        ...

    @abstractmethod
    def get_element_by_id(self, element_id: str) -> IElement:
        ...


# TODO: Use UUID for ids?

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
    def get_property(self, property_name: str) -> Property:
        ...

    @abstractmethod
    def get_properties(self) -> Collection[Property]:
        ...

    @abstractmethod
    def set_property(self, property_name: str, property_value: IVariableValue) -> None:
        ...


# TODO: Should control statements extend component?

class IVariableContainer(ABC):
    """An abstract base class for something that can contain variables"""

    @abstractmethod
    def get_variables(self) -> Collection[IVariable]:
        ...


class IControlStatement(IElement, IVariableContainer, ABC):
    """
    An element in the workflow that contains children and controls how those children
     will be executed.

    Examples are: sequential, parallel, looping, conditional, Trade Study.
    """

    @property
    @abstractmethod
    def control_type(self) -> str:
        ...

    @abstractmethod
    def get_components(self) -> Collection[IElement]:
        ...


class IComponent(IElement, IVariableContainer, ABC):
    """
    A black box analysis is defined as taking a set of inputs, executing, and resulting in a set
     of outputs.

    May be a solver, simulation, co-simulation, calculation, or other third party analysis. While
    state may be kept as an optimization to help performance for slow to start tools, the
    component definition does not require it so that we can parallelize the work onto an
    HPC cluster. Synonymous in our context with Integrations and Analysis. This is the
    preferred go forward term to use in APIs and documentation about Engineering Workflow
    """

    @property
    @abstractmethod
    def pacz_url(self):
        ...

# TODO: We may want specific variable types that refine get/set value to specific
#  variableinterop types?


class IVariable(IElement, ABC):
    """
    A runtime placeholder for some value of a particular type.

    Will change as the workflow runs and can be linked to other variables via direct
    links or equations
    """

    @abstractmethod
    def get_metadata(self) -> CommonVariableMetadata:
        ...

    @abstractmethod
    def get_value(self, hid: Optional[str]) -> VariableState:
        ...

    @abstractmethod
    def set_value(self, value: VariableState) -> None:
        ...
