"""A pure Python implementation of the builtins module that relates to syntax.

1. `obj.attr` ➠ `builtins.getattr(obj, "attr")` (including `object.__getattribute__()`)

"""
# https://docs.python.org/3.8/library/builtins.html
from __future__ import annotations
import builtins

import typing
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    Literal,
    Sequence,
    Tuple,
    Type,
    Union,
)

# TODO:
#   - type()
#   - isinstance()
#   - issubclass()


_NOTHING = builtins.object()  # C: NULL


def _mro(type_: Type) -> Iterable[type]:
    """Fetch the MRO for a type."""
    # The MRO is calculated at class creation time and set to `__mro__`.
    # https://github.com/python/cpython/blob/v3.8.3/Objects/typeobject.c#L5338
    # The `mro()` method is only called during creation in case a type overrides
    # MRO calculation.
    return type_.__mro__


def _mro_getattr(type_: Type, attr: str) -> Any:
    """Get an attribute from a type based on its MRO."""
    for base in _mro(type_):
        if attr in base.__dict__:  # Pretend this is fetched directly from the object.
            return base.__dict__[attr]
    else:
        raise AttributeError(f"{type_.__name__!r} object has no attribute {attr!r}")


def getattr(obj: object, attr: str, default: Any = _NOTHING, /) -> Any:
    """Implement attribute access via  __getattribute__ and __getattr__."""
    # Python/bltinmodule.c:builtin_getattr
    if not isinstance(attr, str):
        raise TypeError("attribute name must be a 'str'")

    obj_type = builtins.type(obj)
    attr_exc = _NOTHING
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

    if default is not _NOTHING:
        return default
    else:
        raise attr_exc


def _index(obj: object, /) -> int:
    """Losslessly convert an object to an integer object.

    If obj is an instance of int, return it directly. Otherwise call __index__()
    and require it be a direct instance of int (raising TypeError if it isn't).
    """
    # https://github.com/python/cpython/blob/v3.8.3/Objects/abstract.c#L1260-L1302
    if isinstance(obj, int):
        return obj

    length_type = builtins.type(obj)
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
        raise TypeError(f"expected an 'int', not {builtins.type(index).__name__!r}")


def len(obj: object, /) -> int:
    """Return the number of items in a container."""
    # https://github.com/python/cpython/blob/v3.8.3/Python/bltinmodule.c#L1536-L1557
    # https://github.com/python/cpython/blob/v3.8.3/Objects/abstract.c#L45-L63
    # https://github.com/python/cpython/blob/v3.8.3/Objects/typeobject.c#L6184-L6209
    type_ = builtins.type(obj)
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
        raise ValueError(f"{type_.__name__}.__len__() should return >= 0")
    else:
        return index


def _is_true(obj: Any, /) -> bool:
    if obj is True:
        return True
    elif obj is False:
        return False
    elif obj is None:
        return False
    obj_type = builtins.type(obj)
    try:
        __bool__ = _mro_getattr(obj_type, "__bool__")
    except AttributeError:
        # Only try calling len() if it makes sense.
        try:
            __len__ = _mro_getattr(obj_type, "__len__")
        except AttributeError:
            # If all else fails...
            return True
        else:
            return True if len(obj) > 0 else False
    else:
        boolean = __bool__(obj)
        if isinstance(boolean, bool):
            # Coerce into True or False.
            return _is_true(boolean)
        else:
            raise TypeError(
                f"expected a 'bool' from {obj_type.__name__}.__bool__(), "
                f"not {builtins.type(boolean).__name__!r}"
            )


def any(iterable: Any, /) -> bool:
    """Return True if bool(x) is True for any x in the iterable.

    If the iterable is empty, return False.

    """
    for item in iterable:
        if item:
            return True
    else:
        return False


_SequenceItem = typing.TypeVar("_SequenceItem")


def _seq_iter(seq: Sequence[_SequenceItem]) -> Iterator[_SequenceItem]:
    """Yields the items of the sequence starting at 0."""
    # Python/iterobject.c:PySeqIter_Type
    # Slightly cheating as the CPython type supports pickling.
    index = 0
    while True:
        try:
            yield seq[index]
            index += 1
        except (IndexError, StopIteration):
            return


_CallableIter = typing.TypeVar("_CallableIter")


def _call_iter(
    callable: Callable[[], _CallableIter], sentinel: _CallableIter
) -> Iterator[_CallableIter]:
    """Yields values returned by 'callable' until a value equal to 'sentinel' is found."""
    # Python/iterobject.c:PyCallIter_Type
    # Slightly cheating as the CPython type supports pickling.
    while True:
        try:
            val = callable()
        except StopIteration:
            raise
        else:
            if val == sentinel:
                return
            else:
                yield val


def iter(
    obj: Union[Callable[[], _CallableIter], Iterable, Sequence],
    /,
    sentinel: _CallableIter = _NOTHING,
) -> Iterator:
    """Return an iterator for the object.

    If 'sentinel' is unspecified, the first argument must either be an iterable
    or a sequence. If the argument is a sequence, an iterator will be returned
    which will index into the argument starting at 0 and continue until
    IndexError or StopIteration is raised.

    With 'sentinel' specified, the first argument is expected to be a callable
    which takes no arguments. The returned iterator will execute the callable on
    each iteration until an object equal to 'sentinel' is returned.
    """
    # Python/bltinmodule.c:builtin_iter
    obj_type = builtins.type(obj)
    if sentinel is _NOTHING:
        # Python/abstract.c:PyObject_GetIter
        try:
            __iter__ = _mro_getattr(obj_type, "__iter__")
        except AttributeError:
            try:
                _mro_getattr(obj_type, "__getitem__")
            except AttributeError:
                raise TypeError(f"{obj_type.__name__!r} is not iterable")
            else:
                return _seq_iter(typing.cast(Sequence, obj))
        else:
            iterator = __iter__(obj)
            # Python/abstract.c:PyIter_Check()
            iterator_type = builtins.type(iterator)
            try:
                _mro_getattr(iterator_type, "__next__")
            except AttributeError:
                raise TypeError(
                    f"{obj_type.__name__!r}.__iter__() returned a non-iterator of type {builtins.type(__iter__)!r}"
                )
            else:
                return __iter__(obj)
    else:
        # Python/object.c:PyCallable_Check
        try:
            _mro_getattr(obj_type, "__call__")
        except AttributeError:
            raise TypeError(f"{obj_type.__name__!r} must be callable")
        else:
            return _call_iter(typing.cast(Callable, obj), sentinel)


_IteratorNext = typing.TypeVar("_IteratorNext")


def next(
    iterator: Iterator[_IteratorNext], /, default: Any = _NOTHING
) -> _IteratorNext:
    """Return the next value from the iterator by calling __next__().

    If a 'default' argument is provided, it is returned if StopIteration is
    raised by the iterator.
    """
    # Python/bltinmodule.c:builtin_next
    iterator_type = builtins.type(iterator)
    try:
        __next__ = _mro_getattr(iterator_type, "__next__")
    except AttributeError:
        raise TypeError(f"{iterator_type.__name__!r} is not an iterator")
    else:
        try:
            val = __next__(iterator)
        except StopIteration:
            if default is _NOTHING:
                raise
            else:
                return default
        else:
            return val


class type(typing.Type):

    __mro__: Tuple[Any]
    __name__: str

    def mro(self):
        """Return a type's method resolution order."""
        return self.__mro__


class object(type):
    def __getattribute__(self, attr: str, /) -> Any:
        """Attribute access."""
        # There should be no attribute access that isn't somehow justified in
        # _mro_getattr().
        # Objects/object.c:PyObject_GenericGetAttr
        self_type = builtins.type(self)
        if not isinstance(attr, str):
            raise TypeError(
                f"attribute name must be string, not {builtins.type(attr).__name__!r}"
            )

        type_attr = descriptor_type_get = _NOTHING
        try:
            type_attr = _mro_getattr(self_type, attr)
        except AttributeError:
            pass  # Hopefully an instance attribute.
        else:
            type_attr_type = builtins.type(type_attr)
            try:
                descriptor_type_get = _mro_getattr(type_attr_type, "__get__")
            except AttributeError:
                pass  # At least a class attribute.
            else:
                # At least a non-data descriptor.
                for base in _mro(type_attr_type):
                    if "__set__" in base.__dict__ or "__delete__" in base.__dict__:
                        # Data descriptor.
                        return descriptor_type_get(type_attr, self, self_type)

        if attr in self.__dict__:
            # Instance attribute.
            return self.__dict__[attr]
        elif descriptor_type_get is not _NOTHING:
            # Non-data descriptor.
            return typing.cast(Callable, descriptor_type_get)(
                type_attr, self, self_type
            )
        elif type_attr is not _NOTHING:
            # Class attribute.
            return type_attr
        else:
            raise AttributeError(f"{self.__name__!r} object has no attribute {attr!r}")


_NotImplementedType = builtins.type(NotImplemented)


def __eq__(self, other: Any, /) -> Union[Literal[True], _NotImplementedType]:
    """Implement equality via identity.

    If the objects are not equal then return NotImplemented to give the
    other object's __eq__ implementation a chance to participate in the
    comparison.

    """
    # https://github.com/python/cpython/blob/v3.8.3/Objects/typeobject.c#L3834-L3880
    return (self is other) or NotImplemented


def __ne__(self, other: Any, /) -> Union[bool, _NotImplementedType]:
    """Implement inequality by delegating to __eq__."""
    # https://github.com/python/cpython/blob/v3.8.3/Objects/typeobject.c#L3834-L3880
    result = self.__eq__(other)
    if result is not NotImplemented:
        return not result
    else:
        return NotImplemented
