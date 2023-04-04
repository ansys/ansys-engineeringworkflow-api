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
            validation_names: AbstractSet[str]) -> Mapping[str, VariableState]:
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
        validation_names : AbstractSet[str]
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
                  validation_names: AbstractSet[str]) -> None:
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
        validation_names : AbstractSet[str]
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


class IElement(ABC):
    """Any one of Component, Control Statement, or Variable"""

    @property
    @abstractmethod
    def element_id(self) -> str:
        """A unique ID for this element, assigned by the system."""
        ...

    @property
    @abstractmethod
    def parent_element_id(self) -> str:
        """The parent element's id, or a blank string if this is the root
           element of the workflow."""
        ...

    @abstractmethod
    def get_parent_element(self) -> IElement:
        """Returns the parent object of this element, or None if this is
           the root element of the workflow."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of this element."""
        ...

    @property
    @abstractmethod
    def full_name(self) -> str:
        """The full name of this element in dotted notation starting from the root of the workflow."""
        ...

    @abstractmethod
    def get_property(self, property_name: str) -> Property:
        """Gets a property by its property name."""
        ...

    @abstractmethod
    def get_properties(self) -> Collection[Property]:
        """Gets all of the properties of this element."""
        ...

    @abstractmethod
    def set_property(self, property_name: str, property_value: IVariableValue) -> None:
        """
        Creates or sets a property on this element.

        Parameters
        ----------
        property_name: str
           The name of the property to create or set
        property_value: IVariableValue
           The value of the property
        """
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
    def get_elements(self) -> Collection[IElement]:
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

    #TODO: Is there a URL type in Python instead of using string below?

    @property
    @abstractmethod
    def pacz_url(self) -> str:
        """The URL Reference to the PACZ file or directory. May be an absolute or a relative
        URL. If relative, it is relative to the workflow definition. While all components will be
        represented by PACZ definitions, in the short term many components are not currently
        defined this way. If there is not a PACZ definition of this component, this method 
        will throw an exception. In those cases you will have to fall back on the engine specific
        methods to determine what type of component this is."""
        ...

# TODO: This API needs to be udpated with respect to the latest thinking on variables and
#  structures of variables, including change to the datapin terminology.
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

    @property
    @abstractmethod
    def is_input_to_component(self) -> bool:
        """Get whether this variable is an input in the context of the component it is on."""

    @property
    @abstractmethod
    def is_input_to_workflow(self) -> bool:
        """
        Get whether this variable is an input in the context of the overall workflow.

        Variables which are inputs in the context of their component will not be in the
        overall workflow if they are the target of a link.
        """
