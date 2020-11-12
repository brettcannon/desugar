"""A pure Python implementation of the builtins module that relates to syntax.

1. `obj.attr` ➠ `builtins.getattr(obj, "attr")` (including `object.__getattribute__()`)

"""
# https://docs.python.org/3.8/library/builtins.html
from __future__ import annotations
import builtins

import typing

if typing.TYPE_CHECKING:
    from typing import Any, Iterable, Literal, Union

    class Object(typing.Protocol):

        """Protocol for objects."""

        __dict__: dict[str, Any]

        def __getattribute__(self, name: str) -> Any:
            ...

    class Type(typing.Protocol):

        """Protocol for types."""

        __name__: str
        __dict__: dict[str, Any]

        def mro() -> Iterable[Type]:
            # https://docs.python.org/3.8/library/stdtypes.html?highlight=mro#class.mro
            ...


# TODO:
#   - type()
#   - isinstance()
#   - issubclass()


NOTHING = builtins.object()  # C: NULL


def _mro_getattr(type_: Type, attr: str) -> Any:
    """Get an attribute from a type based on its MRO."""
    for base in type_.mro():
        if attr in base.__dict__:
            return base.__dict__[attr]
    else:
        raise AttributeError(f"{type_.__name__!r} object has no attribute {attr!r}")


def getattr(obj: Object, attr: str, default: Any = NOTHING, /) -> Any:
    """Implement attribute access via  __getattribute__ and __getattr__."""
    # Python/bltinmodule.c:builtin_getattr
    if not isinstance(attr, str):
        raise TypeError("getattr(): attribute name must be string")

    obj_type = type(obj)
    attr_exc = NOTHING
    getattribute = _mro_getattr(obj_type, "__getattribute__")
    try:
        return getattribute(obj, attr)
    except AttributeError as exc:
        attr_exc = exc
    # Objects/typeobject.c:slot_tp_getattr_hook
    # It is cheating to do this here as CPython actually rebinds the tp_getattro
    # slot with a wrapper that handles __getattr__() when present.
    try:
        getattr_ = _mro_getattr(obj_type, "__getattr__")
    except AttributeError:
        pass
    else:
        return getattr_(obj, attr)

    if default is not NOTHING:
        return default
    else:
        raise attr_exc


class object:
    def __getattribute__(self, attr: str, /) -> Any:
        """Attribute access."""
        # Objects/object.c:PyObject_GenericGetAttr
        self_type = type(self)
        if not isinstance(attr, str):
            raise TypeError(
                f"attribute name must be string, not {type(attr).__name__!r}"
            )

        type_attr = descriptor_type_get = NOTHING
        for base in self_type.mro():
            if attr in base.__dict__:
                type_attr = base.__dict__[attr]
                type_attr_type = type(type_attr)
                if "__get__" in type_attr_type.__dict__:
                    descriptor_type_get = type_attr_type.__dict__["__get__"]
                    # Include/descrobject.h:PyDescr_IsData
                    if (
                        "__set__" in type_attr_type.__dict__
                        or "__delete__" in type_attr_type.__dict__
                    ):
                        # Data descriptor.
                        return descriptor_type_get(type_attr, self, self_type)
                    else:
                        break  # Non-data descriptor.
                else:
                    break  # Plain object.

        if attr in self.__dict__:
            return self.__dict__[attr]
        elif descriptor_type_get is not NOTHING:
            return descriptor_type_get(type_attr, self, self_type)
        elif type_attr is not NOTHING:
            return type_attr
        else:
            raise AttributeError(f"{self_type.__name__!r} object has no attribute {attr!r}")

    def __eq__(self, other, /) -> Union[Literal[True], NotImplemented]:
        """Implement equality via identity.

        If the objects are not equal then return NotImplemented to give the
        other object's __eq__ implementation a chance to participate in the
        comparison.

        """
        # https://github.com/python/cpython/blob/v3.8.3/Objects/typeobject.c#L3834-L3880
        return (self is other) or NotImplemented

    def __ne__(self, other, /) -> Union[bool, NotImplemented]:
        """Implement inequality by delegating to __eq__."""
        # https://github.com/python/cpython/blob/v3.8.3/Objects/typeobject.c#L3834-L3880
        result = self.__eq__(other)
        if result is not NotImplemented:
            return not result
        else:
            return NotImplemented

    # TODO: def mro(self) -> Iterable[Type]: ...
