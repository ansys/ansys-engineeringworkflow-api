"""
Synchronous API definitions.

This module contains the common API for all Ansys workflow engines, written in a
synchronous style. It has the exact same API as iasyncworkflow module and any
changes to one file must be made to the other.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from os import PathLike
from typing import AbstractSet, Collection, Mapping, Union

from ansys.common.variableinterop import CommonVariableMetadata, VariableState

from .datatypes import *


class IWorkflowEngine(ABC):
    """Interface defines the common behavior for an engineering workflow engine that can run and
     monitor instances"""

    @abstractmethod
    def get_server_info(self) -> WorkflowEngineInfo:
        """
        Gets information about the server that is serving this request.

        Returns
        -------
        A WorkflowEngineInfo object with information about the server that is serving this request
        """
        ...


class IFileBasedWorkflowEngine(IWorkflowEngine, ABC):
    """Extends IWorkflowEngine with calls that are relevant for loading files from a local
    filesystem. """

    @abstractmethod
    def load_workflow(self, file_name: Union[PathLike, str]) -> IWorkflowInstance:
        ...


class IWorkflowInstance(ABC):
    """Representation of an instantiated workflow instance"""

    @abstractmethod
    def get_state(self) -> WorkflowInstanceState:
        """Gets the state of the workflow instance."""
        ...

    # TODO: probably should not pre-emptively return all outputs as that could
    # be quite expensive.
    @abstractmethod
    def run(self, inputs: Mapping[str, VariableState], reset: bool,
            validation_ids: AbstractSet[str]) -> Mapping[str, VariableState]:
        """
        Sets a workflow's input variables and runs it.
     
        Parameters
        ----------
        inputs : Mapping[str, VariableState]
            A map of variable name to a VariableState object for all inputs to
            be set before running.
        reset : bool
            Setting this to true will cause the workflow to be reset before running. 
            Note that setting variable values could also implicitly reset some component's states
        validation_ids : AbstractSet[str]
            Supplying the names of the specific variables or components that are
            required to be valid may enable the workflow engine to shortcut
            evaluation of the workflow. If this list is non-empty, the workflow
            engine may choose which portions of the workflow are run to satisfy
            the given variables with the minimum runtime.
        
        Returns
        -------
        Mapping[str, VariableState] : A map of output variable names to VariableState objects for each output.
        """
        ...

    @abstractmethod
    def start_run(self, inputs: Mapping[str, VariableState], reset: bool,
                  validation_ids: AbstractSet[str]) -> None:
        """
        Sets a workflow's input variables and starts the workflow running.
     
        Parameters
        ----------
        inputs : Mapping[str, VaraibleState]
            A map of variable name to a VariableState object for all inputs to
            be set before running.
        reset : bool
            Setting this to true will cause the workflow to be reset before running. 
            Note that setting variable values could also implicitly reset some component's states
        validation_ids : AbstractSet[str]
            Supplying the names of the specific variables or components that are
            required to be valid may enable the workflow engine to shortcut
            evaluation of the workflow. If this list is non-empty, the workflow
            engine may choose which portions of the workflow are run to satisfy
            the given variables with the minimum runtime.
        """
        ...

    # TODO: How to wait for finish in second case?

    @abstractmethod
    def get_root(self) -> IControlStatement:
        """Gets the root element of the workflow instance."""
        ...

    @abstractmethod
    def get_element_by_name(self, element_name: str) -> IElement:
        """
        Gets an element of the workflow instance by name.

        Parameters
        ----------
        element_name : str
            The name of the element to retrieve in dotted notation, e.g. "Root.Component.Thing".
        """
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
