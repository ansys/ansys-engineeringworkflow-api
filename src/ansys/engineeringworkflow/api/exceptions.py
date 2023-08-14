"""Defines exception types that allow for more expressive error handling in common
situations."""


class EngineInternalError(Exception):
    """
    Raised to indicate that the workflow engine has encountered an internal error.

    Errors of this type indicate that something has gone wrong with the workflow engine
    itself during the requested operation. These errors should not usually be
    encountered and may indicate the presence of a bug that should be reported to the
    engine maintainer.
    """


class NameCollisionError(ValueError):
    """
    Raised to indicate that the requested operation failed because of a name collision.

    This means that the name requested is already in use and cannot be re-used.

    Engine maintainers should only raise this error if the operation in question is
    otherwise valid and could be retried successfully with a different, unique name.
    """


class ValueOutOfRangeError(ValueError):
    """
    Raised to indicate that an operation failed because the requested value is out of
    range.

    This is most commonly used when an attempt to set a datapin value fails because the
    requested value violates the datapin's boundaries or the datapin has enumerated
    values and the requested value is not in the enumeration.
    """
