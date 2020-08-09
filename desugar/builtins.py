# Based on https://github.com/python/cpython/tree/v3.8.3.
from __future__ import annotations
import builtins

import typing

if typing.TYPE_CHECKING:
    from typing import Any

    class Object(typing.Protocol):

        """Protocol for all objects."""

        def __getattribute__(self, name: str) -> Any:
            ...


NOTHING = builtins.object()  # C: NULL


def _type_getattr(obj, attr):
    """Get an attribute for an object from its type."""
    obj_type_mro = type(obj).mro()
    for base in obj_type_mro:
        if attr in base.__dict__:
            return base.__dict__[attr]
    else:
        raise AttributeError(f"{obj.__name__!r} object has no attribute {attr!r}")


def getattr(obj: Object, attr: str, default: Any = NOTHING, /) -> Any:
    """Implement attribute access via  __getattribute__ and __getattr__."""
    # Python/bltinmodule.c:builtin_getattr
    if not isinstance(attr, str):
        raise TypeError("getattr(): attribute name must be string")

    obj_type_mro = type(obj).mro()
    attr_exc = NOTHING
    getattribute = _type_getattr(obj, "__getattribute__")
    try:
        return getattribute(obj, attr)
    except AttributeError as exc:
        attr_exc = exc
    # Objects/typeobject.c:slot_tp_getattr_hook
    # It is cheating to do this here as CPython actually rebinds the tp_getattro
    # slot with a wrapper that handles __getattr__() when present.
    try:
        getattr_ = _type_getattr(obj, "__getattr__")
    except AttributeError:
        pass
    else:
        return getattr_(obj, attr)

    if default is not NOTHING:
        return default
    else:
        raise attr_exc


class object:
    def __getattribute__(self: Any, attr: str, /) -> Any:
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
                    if "__set__" in type_attr_type.__dict__:
                        # Data descriptor.
                        return descriptor_type_get(type_attr, self, self_type)
                    else:
                        break  # Non-data descriptor.
                else:
                    break  # Plain object.

        if attr in self.__dict__:
            return self.__dict__[attr]
        elif type_attr is not NOTHING:
            if descriptor_type_get is not NOTHING:
                return descriptor_type_get(type_attr, self, self_type)
            else:
                return type_attr
        else:
            raise AttributeError(f"{self.__name__!r} object has no attribute {attr!r}")
