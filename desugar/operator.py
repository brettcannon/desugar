from __future__ import annotations

import typing

from . import builtins as debuiltins

if typing.TYPE_CHECKING:
    from typing import Any


def sub(lhs: Any, rhs: Any, /) -> Any:
    """Subtraction: `lhs - rhs`."""
    if issubclass(type(rhs), type(lhs)):
        call_first = rhs, "__rsub__", lhs
        call_second = lhs, "__sub__", rhs
    else:
        call_first = lhs, "__sub__", rhs
        call_second = rhs, "__rsub__", lhs

    for first, meth, second in (call_first, call_second):
        try:
            meth = debuiltins._type_getattr(first, meth)
        except AttributeError:
            continue
        value = meth(first, second)
        if value is not NotImplemented:
            return value
    else:
        raise TypeError(
            f"unsupported operand type(s) for -: {type(lhs)!r} and {type(rhs)!r}"
        )
