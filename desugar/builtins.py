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


def _index(obj: Any, /) -> int:
    """Losslessly convert an object to an integer object.

    If obj is an instance of int, return it directly. Otherwise call __index__()
    and require it be a direct instance of int (raising TypeError if it isn't).
    """
    # https://github.com/python/cpython/blob/v3.8.3/Objects/abstract.c#L1260-L1302
    if isinstance(obj, int):
        return obj

    length_type = type(obj)
    try:
        __index__ = _mro_getattr(length_type, "__index__")
    except AttributeError:
        msg = (
            f"{length_type!r} cannot be interpreted as an integer "
            "(must be either a subclass of 'int' or have an __index__() method)"
        )
        raise TypeError(msg)
    index = __index__(obj)
    # Returning a subclass of int is deprecated in CPython.
    if index.__class__ is int:
        return index
    else:
        raise TypeError(
            f"the __index__() method of {length_type!r} returned an object of "
            "type {type(index)!r}, not 'int'"
        )


def len(obj: Any, /) -> int:
    """Return the number of items in a container."""
    # https://github.com/python/cpython/blob/v3.8.3/Python/bltinmodule.c#L1536-L1557
    # https://github.com/python/cpython/blob/v3.8.3/Objects/abstract.c#L45-L63
    # https://github.com/python/cpython/blob/v3.8.3/Objects/typeobject.c#L6184-L6209
    type_ = type(obj)
    try:
        __len__ = _mro_getattr(type_, "__len__")
    except AttributeError:
        raise TypeError(f"type {type!r} does not have a __len__() method")
    length = __len__(obj)
    # Due to len() using PyObject_Size() (which returns Py_ssize_t),
    # the returned value is always a direct instance of int via
    # PyLong_FromSsize_t().
    index = int(_index(length))
    if index < 0:
        raise ValueError("__len__() should return >= 0")
    else:
        return index


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
        try:
            type_attr = _mro_getattr(self_type, attr)
        except AttributeError:
            pass  # Hopefully an instance attribute.
        else:
            type_attr_type = type(type_attr)
            try:
                descriptor_type_get = _mro_getattr(type_attr_type, "__get__")
            except AttributeError:
                pass  # At least a class attribute.
            else:
                # At least a non-data descriptor.
                for base in type_attr_type.mro():
                    if "__set__" in base.__dict__ or "__delete__" in base.__dict__:
                        # Data descriptor.
                        return descriptor_type_get(type_attr, self, self_type)

        if attr in self.__dict__:
            # Instance attribute.
            return self.__dict__[attr]
        elif descriptor_type_get is not NOTHING:
            # Non-data descriptor.
            return descriptor_type_get(type_attr, self, self_type)
        elif type_attr is not NOTHING:
            # Class attribute.
            return type_attr
        else:
            raise AttributeError(f"{self.__name__!r} object has no attribute {attr!r}")

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
