# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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
"""API datatype definitions."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ansys.tools.variableinterop import IVariableValue


@dataclass(frozen=True)
class WorkflowEngineInfo:
    """Stores workflow engine information collected by the ``get_server_info`` call."""

    # TODO: this style documentation does not appear to be working?
    release_year: int
    """Year portion of the release, such as ``2022``."""
    release_id: int
    """ID portion of the release, such as ``2`` for 2022 R2."""
    build: int
    """Build number."""
    is_release_build: bool
    """
    Flag indicating if the release is a production release.

    The value is ``False`` for development, alpha, beta, and other releases.
    """
    build_type: str
    """
    Build type.

    This attribute must be blank for a production release. For other release types, it may include
    arbitrary information like the branch that a development build was built from.
    """
    version_as_string: str
    """
    Version of the workflow engine encoded for human consumption.

    For example, ```2022r1 build 333 ALPHA```.
    """
    server_type: str
    """
    Type of server that is responding to the request.

    The value is a string similar to ``'ModelCenter'`` or ``'optiSLang'``.
    """
    install_location: Optional[str]
    """
    Installation directory.

    If the client is on the same box as the workflow engine, this optional attribute may provide the
    installation folder.

    Typically server-based products do not provide this field for security reasons.
    """
    base_url: Optional[str]
    """
    Base URL for clients to connect to.

    If this is a server-based product ready to receive incoming connections from remote clients,
    this optional attribute may provide the base URL for clients to connect to.
    """


class WorkflowInstanceState(Enum):
    """Provides an enum with the states that a workflow instance can be in."""

    UNKNOWN = 0
    INVALID = 1
    RUNNING = 2
    PAUSED = 3
    FAILED = 4
    SUCCESS = 5


@dataclass(frozen=True)
class Property:
    """
    Provides a configurable setting on some component or algorithm in the workflow.

    This configurable setting cannot be linked to other variables or properties. Unless a property
    is explicitly documented as supporting it, values should not be changed while the workflow is
    running. Examples that may support modification would be convergence criteria for an
    optimization algorithm.
    """

    parent_element_id: str
    property_name: str
    property_value: IVariableValue
