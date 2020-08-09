from __future__ import annotations

import typing

from . import builtins as debuiltins

if typing.TYPE_CHECKING:
    from typing import Any


def sub(lhs: Any, rhs: Any, /) -> Any:
    """Subtraction: `a - b`."""
    rhs_type = type(rhs)
    lhs_type = type(lhs)
    if rhs_type is not lhs_type and issubclass(rhs_type, lhs_type):
        call_first = (rhs, rhs_type), "__rsub__", lhs
        call_second = (lhs, lhs_type), "__sub__", rhs
    else:
        call_first = (lhs, lhs_type), "__sub__", rhs
        call_second = (rhs, rhs_type), "__rsub__", lhs

    for first, meth, second_obj in (call_first, call_second):
        first_obj, first_type = first
        try:
            meth = debuiltins._mro_getattr(first_type, meth)
        except AttributeError:
            continue
        value = meth(first_obj, second_obj)
        if value is not NotImplemented:
            return value
    else:
        raise TypeError(
            f"unsupported operand type(s) for -: {lhs_type!r} and {rhs_type!r}"
        )
