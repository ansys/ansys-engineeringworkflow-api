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
"""Exception types, which allow for handling expressive errors in common situations."""


class EngineInternalError(Exception):
    """
    Indicates that the workflow engine has encountered an internal error.

    An error of this type means that something has gone wrong with the workflow engine itself during
    the requested operation. Such an error should not usually be encountered and may indicate the
    presence of a bug that should be reported to the engine maintainer.
    """


class NameCollisionError(ValueError):
    """
    Indicates that an operation has failed because of a name collision.

    An error of this type means that the name requested is already in use and cannot be reused.

    Engine maintainers should only raise this error if the operation in question is otherwise valid
    and could be retried successfully with a different, unique name.
    """


class ValueOutOfRangeError(ValueError):
    """
    Indicates that an operation has failed because the requested value is out of range.

    An error of this type is most commonly used when an attempt to set a datapin value fails
    for one of these reasons:

    - The requested value violates the datapin's boundaries.
    - The datapin has enumerated values and the requested value is not in the enumeration.
    """
