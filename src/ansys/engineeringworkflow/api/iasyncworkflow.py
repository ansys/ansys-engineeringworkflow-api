# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Asynchronous API definitions.

This module contains the common API for all Ansys workflow engines, written in an
asynchronous style. It has the exact same API as the ``IWorkflow`` module and any
changes to one file must be made to the other.

Generally speaking, in addition to the exceptions already noted, implementations of
this API may raise the :class:`.exceptions.EngineInternalError` class to indicate
that an internal error has been encountered and should be reported to the engine
implementation maintainer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from os import PathLike
from typing import AbstractSet, Collection, Mapping, Optional, Union

from ansys.tools.variableinterop import CommonVariableMetadata, IVariableValue, VariableState

from .datatypes import Property, WorkflowEngineInfo, WorkflowInstanceState


class IAsyncWorkflowEngine(ABC):
    """
    Provides the interface defining the common behavior for an engineering workflow engine.

    This interface can run and monitor instances.
    """

    @abstractmethod
    async def get_server_info(self) -> WorkflowEngineInfo:
        """
        Get information about the server that is serving the request.

        Returns
        -------
        WorkflowEngineInfo
            Object with the information about the server that is serving the
            request.
        """
        ...


class IAsyncFileBasedWorkflowEngine(IAsyncWorkflowEngine, ABC):
    """
    Extends the ``IWorkflowEngine`` module with calls.

    The calls must be relevant for loading files from a local filesystem.
    """

    @abstractmethod
    async def load_workflow(self, file_name: Union[PathLike, str]) -> IAsyncWorkflowInstance:
        """Load a workflow from a local file into the engine."""
        ...


class IAsyncWorkflowInstance(ABC):
    """Represents an instantiated workflow instance."""

    @abstractmethod
    async def get_state(self) -> WorkflowInstanceState:
        """Get the state of the workflow instance."""
        ...

    @abstractmethod
    async def run(
        self,
        inputs: Mapping[str, VariableState] = {},
        reset: bool = False,
        validation_names: AbstractSet[str] = set(),
        collect_names: AbstractSet[str] = set(),
    ) -> Mapping[str, VariableState]:
        """
        Set a workflow's input datapins and run it.

        Parameters
        ----------
        inputs : Mapping[str, VariableState]
            Map of datapin names to ``VariableState`` objects for all inputs to
            set before running the workflow.
        reset : bool, default: False
            Whether to reset the workflow before running. If this parameter is set
            to ``True``, all run components and data links become invalid so that the
            workflow runs from the beginning. However, it does not reset any input values
            that have been set to non-default values. Note that setting datapin values
            could also implicitly reset the states of some components.
        validation_names : AbstractSet[str]
            Names of the specific datapins or components that are required to be valid.
            Setting names may enable the workflow engine to shortcut evaluation of the
            workflow. If the set is non-empty, the workflow engine may choose which
            portions of the workflow are run to satisfy the given datapins with the
            minimum runtime.
        collect_names : AbstractSet[str]
            Names of the specific datapins or elements that are to cause the method
            to return these values after running. If an element is specified, all
            child datapins are recursively included.

        Raises
        ------
        ValueOutOfRangeError
            If one of the input values violates its datapin's bounds or enumerated values.
        """
        ...

    @abstractmethod
    async def start_run(
        self, inputs: Mapping[str, VariableState], reset: bool, validation_names: AbstractSet[str]
    ) -> str:
        """
        Set a workflow's input datapins and start running the workflow.

        Parameters
        ----------
        inputs : Mapping[str, VariableState]
            Map of datapin names to ``VariableState`` objects for all inputs to
            set before running the workflow.
        reset : bool
            Whether to reset the workflow before running. If this parameter is set
            to ``True``, all run components and data links become invalid so that the
            workflow runs from the beginning. However, it does not reset any input values
            that have been set to non-default values. Note that setting datapin values
            could also implicitly reset some the states of some components.
        validation_names : AbstractSet[str]
            Names of the specific datapins or components that are required to be valid.
            Setting names may enable the workflow engine to shortcut evaluation of the
            workflow. If the set is non-empty, the workflow engine may choose which
            portions of the workflow are run to satisfy the given datapins with the
            minimum runtime.

        Raises
        ------
        ValueOutOfRangeError
            If one of the input values violates its datapin's bounds or enumerated values.
        """
        ...

    # TODO: How to wait for finish in second case?

    @abstractmethod
    async def get_root(self) -> IAsyncControlStatement:
        """Get the root element of the workflow instance."""
        ...

    @abstractmethod
    async def get_element_by_name(self, element_name: str) -> IAsyncElement:
        """
        Get an element of the workflow instance by name.

        Parameters
        ----------
        element_name : str
            Name of the element to retrieve in dotted notation. For example,
            ``'Root.Component.Thing'``.
        """
        ...


class IAsyncElement(ABC):
    """Provides a component, control statement, or datapin."""

    @property
    @abstractmethod
    def element_id(self) -> str:
        """Unique ID for the element that is assigned by the system."""
        ...

    @property
    @abstractmethod
    def parent_element_id(self) -> str:
        """
        Parent element's ID.

        If this is the root element of the workflow, the parent ID is a blank string.
        """
        ...

    @abstractmethod
    async def get_parent_element(self) -> IAsyncElement:
        """
        Get the parent object of the element.

        If this is the root element of the workflow, the method returns ``None``.
        """
        ...

    @property
    @abstractmethod
    def name(self):
        """Name of the element."""
        ...

    @property
    @abstractmethod
    def full_name(self) -> str:
        """
        Full name of the element.

        The full name is returned in dotted notation, starting from the root of the workflow.
        """
        ...

    @abstractmethod
    async def get_property(self, property_name: str) -> Property:
        """Get a property by name."""
        ...

    @abstractmethod
    async def get_property_names(self) -> AbstractSet[str]:
        """Get the names of all properties."""
        ...

    @abstractmethod
    async def get_properties(self) -> Mapping[str, Property]:
        """Get all properties of the element."""
        ...

    @abstractmethod
    async def set_property(self, property_name: str, property_value: IVariableValue) -> None:
        """
        Create or set a property on the element.

        Parameters
        ----------
        property_name : str
           Name of the property to create or set.
        property_value : IVariableValue
           Value of the property.
        """
        ...


class IAsyncDatapinContainer(ABC):
    """Provides an abstract base class for something that can contain datapins."""

    @abstractmethod
    async def get_datapins(self) -> Collection[IAsyncDatapin]:
        """
        Get the datapins in the container.

        Returns
        -------
        Mapping[str, IDatapin]
            Map of the datapins in the container. The keys in the map are the short names of the
            datapins (relative to the container's name).
        """
        ...


class IAsyncControlStatement(IAsyncElement, IAsyncDatapinContainer, ABC):
    """
    Provides an element in the workflow that contains children and how they are executed.

    For example, it can be a sequential, parallel, looping, or conditional element or a trade study.
    """

    @property
    @abstractmethod
    def control_type(self) -> str:
        """Type of the control statement."""
        ...

    @abstractmethod
    async def get_elements(self) -> Collection[IAsyncElement]:
        """Get all elements of the control statement."""
        ...


class IAsyncComponent(IAsyncElement, IAsyncDatapinContainer, ABC):
    """
    Provides for a black box analysis.

    A black box analysis is defined as taking a set of inputs, executing, and then returning a set
    of outputs.

    The black box may be a solver, simulation, co-simulation, calculation, or other third-party
    analysis. While state may be kept as an optimization to help performance for slow-to-start
    tools, the component definition does not require it so that the work can be parallelize onto an
    HPC cluster.

    The "black box" term is synonymous with integration and analysis. It is the preferred term used
    in the Ansys Engineering Workflow API and documentation.
    """

    @property
    @abstractmethod
    def pacz_url(self) -> Optional[str]:
        """
        URL to the PACZ file or directory.

        The URL may be absolute or relative. If relative, the URL must be relative to the workflow
        definition. While all components are represented by PACZ definitions, in the short term,
        many components are not currently defined in this way. If there is not a PACZ definition of
        the component, the method returns ``None``. In such cases, you must fall back on
        engine-specific methods to determine what the component type is.
        """
        ...


class IAsyncDatapin(IAsyncElement, ABC):
    """
    Provides a runtime placeholder for some value of a particular type.

    The placeholder changes as the workflow runs. It can be linked to other datapins via direct
    links or equations.
    """

    @abstractmethod
    async def get_metadata(self) -> CommonVariableMetadata:
        """Get the metadata for the datapin."""
        ...

    @abstractmethod
    async def get_state(self, hid: Optional[str] = None) -> VariableState:
        """Get the state of the datapin."""
        ...

    @abstractmethod
    async def set_state(self, state: VariableState) -> None:
        """Set the state of the datapin."""
        ...
