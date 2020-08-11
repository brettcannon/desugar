from __future__ import annotations

import typing
from typing import Callable

from . import builtins as debuiltins

if typing.TYPE_CHECKING:
    from typing import Any


def _create_binary_op(name: str, operator: str) -> Callable[[Any, Any], Any]:
    """Create a binary operation function.

    The `name` parameter specifies the name of the special method used for the
    binary operation (e.g. `sub` for `__sub__`). The `operator` name is the
    token representing the binary operation (e.g. `-` for subtraction).

    """

    def binary_op(lhs: Any, rhs: Any, /) -> Any:
        """A closure implementing a binary operation in Python."""
        rhs_type = type(rhs)
        lhs_type = type(lhs)
        if rhs_type is not lhs_type and issubclass(rhs_type, lhs_type):
            call_first = (rhs, rhs_type), f"__r{name}__", lhs
            call_second = (lhs, lhs_type), f"__{name}__", rhs
        else:
            call_first = (lhs, lhs_type), f"__{name}__", rhs
            call_second = (rhs, rhs_type), f"__r{name}__", lhs

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
                f"unsupported operand type(s) for {operator}: {lhs_type!r} and {rhs_type!r}"
            )

    binary_op.__name__ = binary_op.__qualname__ = name
    binary_op.__doc__ = f"""Implement the binary operation `a {operator} b`."""
    return binary_op


add = _create_binary_op("add", "+")
sub = _create_binary_op("sub", "-")
mul = _create_binary_op("mul", "*")
matmul = _create_binary_op("matmul", "@")
truediv = _create_binary_op("truediv", "/")
floordiv = _create_binary_op("floordiv", "//")
mod = _create_binary_op("mod", "%")
pow = _create_binary_op("pow", "**")
lshift = _create_binary_op("lshift", "<<")
