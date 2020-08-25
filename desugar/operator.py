"""A pure Python implementation of the parts of the 'operator' module that
pertain to syntax."""
# https://docs.python.org/3.8/library/operator.html

from __future__ import annotations

import typing

from . import builtins as debuiltins

if typing.TYPE_CHECKING:
    from typing import Any, Callable

    class _BinaryOp(typing.Protocol):

        """The interface for a callable implementing a binary arithmetic operation."""

        __doc__: str
        __name__: str
        __qualname__: str
        _operator: str

        def __call__(self, lhs: Any, rhs: Any, /) -> Any:
            ...


_MISSING = object()


def _create_binary_op(name: str, operator: str) -> _BinaryOp:
    """Create a binary operation function.

    The `name` parameter specifies the name of the special method used for the
    binary operation (e.g. `sub` for `__sub__`). The `operator` name is the
    token representing the binary operation (e.g. `-` for subtraction).

    """

    lhs_method_name = f"__{name}__"

    def binary_op(lhs: Any, rhs: Any, /) -> Any:
        """A closure implementing a binary operation in Python."""
        rhs_method_name = f"__r{name}__"

        # lhs.__*__
        lhs_type = type(lhs)
        try:
            lhs_method = debuiltins._mro_getattr(lhs_type, lhs_method_name)
        except AttributeError:
            lhs_method = _MISSING

        # lhs.__r*__ (for knowing if rhs.__r*__ should be called first)
        try:
            lhs_rmethod = debuiltins._mro_getattr(lhs_type, rhs_method_name)
        except AttributeError:
            lhs_rmethod = _MISSING

        # rhs.__r*__
        rhs_type = type(rhs)
        try:
            rhs_method = debuiltins._mro_getattr(rhs_type, rhs_method_name)
        except AttributeError:
            rhs_method = _MISSING

        call_lhs = lhs, lhs_method, rhs
        call_rhs = rhs, rhs_method, lhs

        if (
            rhs_type is not _MISSING  # Do we care?
            and rhs_type is not lhs_type  # Could RHS be a subclass?
            and issubclass(rhs_type, lhs_type)  # RHS is a subclass!
            and lhs_rmethod is not rhs_method  # Is __r*__ actually different?
        ):
            calls = call_rhs, call_lhs
        elif lhs_type is not rhs_type:
            calls = call_lhs, call_rhs
        else:
            calls = (call_lhs,)

        for first_obj, meth, second_obj in calls:
            if meth is _MISSING:
                continue
            value = meth(first_obj, second_obj)
            if value is not NotImplemented:
                return value
        else:
            exc = TypeError(
                f"unsupported operand type(s) for {operator}: {lhs_type!r} and {rhs_type!r}"
            )
            exc._binary_op = operator
            raise exc

    # This differs from the "real" 'operator' module, but it simplies the function
    # creation aspect by not having to specify alternative name when it would
    # clash with a keyword, or using the 'keyword' module to automatically
    # detect the clash.
    binary_op.__name__ = binary_op.__qualname__ = lhs_method_name
    binary_op._operator = operator  # For introspective __i*__ implementations.
    binary_op.__doc__ = f"""Implement the binary operation `a {operator} b`."""
    return binary_op


add = __add__ = _create_binary_op("add", "+")
sub = __sub__ = _create_binary_op("sub", "-")
mul = __mul__ = _create_binary_op("mul", "*")
matmul = __matmul__ = _create_binary_op("matmul", "@")
truediv = __truediv__ = _create_binary_op("truediv", "/")
floordiv = __floordiv__ = _create_binary_op("floordiv", "//")
mod = __mod__ = _create_binary_op("mod", "%")
pow = __pow__ = _create_binary_op("pow", "**")
lshift = __lshift__ = _create_binary_op("lshift", "<<")
rshift = __rshift__ = _create_binary_op("rshift", ">>")
and_ = __and__ = _create_binary_op("and", "&")
xor = __xor__ = _create_binary_op("xor", "^")
or_ = __or__ = _create_binary_op("or", "|")


def _create_binary_inplace_op(binary_op: _BinaryOp) -> Callable[[Any, Any], Any]:

    binary_operation_name = binary_op.__name__[2:-2]
    method_name = f"__i{binary_operation_name}__"
    operator = f"{binary_op._operator}="

    def binary_inplace_op(lvalue: Any, rvalue: Any, /) -> Any:
        lvalue_type = type(lvalue)
        try:
            method = debuiltins._mro_getattr(lvalue_type, method_name)
        except AttributeError:
            pass
        else:
            value = method(lvalue, rvalue)
            if value is not NotImplemented:
                return value
        try:
            return binary_op(lvalue, rvalue)
        except TypeError as exc:
            # If the TypeError is due to the binary arithmetic operator, suppress
            # it so we can raise the appropriate one for the agumented assignment.
            if exc._binary_op != binary_op._operator:
                raise
        raise TypeError(
            f"unsupported operand type(s) for {operator}: {lvalue_type!r} and {type(rvalue)!r}"
        )

    binary_inplace_op.__name__ = binary_inplace_op.__qualname__ = method_name
    binary_inplace_op.__doc__ = (
        f"""Implement the augmented arithmetic assignment `a {operator} b`."""
    )
    return binary_inplace_op


iadd = __iadd__ = _create_binary_inplace_op(__add__)
isub = __isub__ = _create_binary_inplace_op(__sub__)
imul = __imul__ = _create_binary_inplace_op(__mul__)
imatmul = __imatmul__ = _create_binary_inplace_op(__matmul__)
itruediv = __itruediv__ = _create_binary_inplace_op(__truediv__)
ifloordiv = __ifloordiv__ = _create_binary_inplace_op(__floordiv__)
imod = __imod__ = _create_binary_inplace_op(__mod__)
ipow = __ipow__ = _create_binary_inplace_op(__pow__)
ilshift = __ilshift__ = _create_binary_inplace_op(__lshift__)
irshift = __irshift__ = _create_binary_inplace_op(__rshift__)
iand = __iand__ = _create_binary_inplace_op(__and__)
ixor = __ixor__ = _create_binary_inplace_op(__xor__)
ior = __ior__ = _create_binary_inplace_op(__or__)
