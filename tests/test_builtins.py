import builtins
import collections.abc
import types
import warnings

import pytest

import desugar.builtins


class NonDataProp:
    msg = "non-data property"

    def __get__(self, instance, owner=None):
        return self.msg


class NonDataPropSubclass(NonDataProp):
    pass


class SetDataProp(NonDataProp):
    msg = "__set__"

    def __set__(self, instance, value):
        return value


class DeleteDataProp(NonDataProp):
    msg = "__delete__"

    def __delete__(self, instance):
        return "__delete__"


class ObjectBaseExample:
    @property
    def data_prop(self):
        return "should never be reached (superclass non-data property)"

    superclass_attr = "superclass attribute"


class ObjectExample(ObjectBaseExample):
    @property
    def data_prop(self):
        return "data property"

    set_data_prop = SetDataProp()
    delete_data_prop = DeleteDataProp()

    def __init__(self):
        self.ins_attr = "instance attribute"
        self.__dict__["data_prop"] = self.__dict__["set_data_prop"] = self.__dict__[
            "delete_data_prop"
        ] = "Should never be reached (instance attribute)"

    non_data_prop = NonDataProp()
    non_data_prop_subclass = NonDataPropSubclass()

    class_attr = "class attribute"
    ins_attr = "should never be reached (class attribute)"


class GetattrExample(ObjectBaseExample):

    """Override object.__getattribute__()."""

    def __getattribute__(self, attr):
        return 42


class GetattrMissing:
    def __getattribute__(self, attr):
        raise AttributeError("uh-oh")

    def __getattr__(self, attr):
        return 42


@pytest.mark.parametrize("getattr", [builtins.getattr, desugar.builtins.getattr])
class TestGetattr:

    """Tests for getattr()."""

    def test_getattribute(self, getattr):
        """A class defining __getattribute__() has that method called."""
        assert getattr(ObjectExample(), "ins_attr") == "instance attribute"

    def test_getattribute_overriding(self, getattr):
        """A subclass' __getattribute__() gets called over the superclass."""
        assert getattr(GetattrExample(), "superclass_attr") == 42
        assert (
            object.__getattribute__(GetattrExample(), "superclass_attr")
            == "superclass attribute"
        )

    def test_getattribute_from_type(self, getattr):
        """__getattribute__() is not fetched from the instance."""
        ins = ObjectExample()
        ins.__getattribute__ = lambda self, attr: 42  # type: ignore
        assert getattr(ins, "ins_attr") == "instance attribute"

    def test_attr_type(self, getattr):
        """Only the str type is acceptable for the attribute name."""
        with pytest.raises(TypeError):
            getattr(GetattrExample(), 42)

    def test_AttributeError(self, getattr):
        with pytest.raises(AttributeError):
            getattr(ObjectExample(), "not_real")

    def test_getattr_method(self, getattr):
        assert getattr(GetattrMissing(), "not_real") == 42

    def test_default(self, getattr):
        assert getattr(ObjectExample(), "not_real", 42) == 42


class Len:
    def __init__(self, length):
        self._len = length

    def __len__(self):
        return self._len


class Index:
    def __init__(self, index):
        self._index = index

    def __index__(self):
        return self._index


@pytest.mark.parametrize("len", [builtins.len, desugar.builtins.len])
class TestLen:

    """Tests for len()."""

    def test_list(self, len):
        """Returns the length of a list."""
        example = [1, 2, 3, 4, 5]
        assert len(example) == 5

    def test_non_container(self, len):
        """TypeError is raised when called on an object that lacks __len__()."""
        with pytest.raises(TypeError):
            len(42)

    def test_int_subclass(self, len):
        """__len__() may return an int subclass."""

        class SubInt(int):
            def __repr__(self):
                return f"<SubInt of {int.__repr__(self)}>"

        sub_42 = SubInt(42)

        length = len(Len(sub_42))
        assert length == 42
        assert not isinstance(length, SubInt)
        assert isinstance(length, int)

    def test_index_on_non_int(self, len):
        """Call __index__() if the object returned by __len__() is not a subclass of int."""
        index = Index(42)
        length = Len(index)
        assert len(length) == 42

    def test_index_raises_on_non_int(self, len):
        """Raises TypeError when __index__() returns a non-int."""
        index = Index("42")
        length = Len(index)
        with pytest.raises(TypeError):
            len(length)

    def test_index_raises_on_int_subclass(self, len):
        """Raises TypeError if __index__() return an int subclass."""

        class SubInt(int):
            pass

        index = Index(SubInt(42))
        length = Len(index)
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            try:
                len(length)
            except (TypeError, DeprecationWarning):
                return
            pytest.fail(
                "__index__() returning an int subclass did not trigger a "
                "TypeError or DeprecationWarning"
            )

    def test_negative_length(self, len):
        """Raises ValueError if the index is < 0."""
        index = Index(-1)
        length = Len(index)
        with pytest.raises(ValueError):
            len(length)

    def test_negative_index(self, len):
        """Raises ValueError if the length is < 0."""
        length = Len(-1)
        with pytest.raises(ValueError):
            len(length)


@pytest.mark.parametrize("any", [builtins.any, desugar.builtins.any])
class TestAny:
    def test_success(self, any):
        """Return True if the iterable has the object."""
        assert any([42]) is True

    def test_failure(self, any):
        """Return False if the iterable is missing the object."""
        assert any([0]) is False

    def test_empty(self, any):
        """Return False if the iterable is empty."""
        assert any([]) is False

    def test_non_iterable(self, any):
        """Raise TypeError if given a non-iterable."""
        with pytest.raises(TypeError):
            any(42)


@pytest.mark.parametrize(
    "__getattribute__",
    [builtins.object.__getattribute__, desugar.builtins.object.__getattribute__],
)
class TestObjectGetattribute:

    """Tests for  object.__getattribute__()."""

    def test_full_data_descriptor(self, __getattribute__):
        """A data descriptor on the class will be found."""
        assert __getattribute__(ObjectExample(), "data_prop") == "data property"

    def test_set_data_descriptor(self, __getattribute__):
        assert __getattribute__(ObjectExample(), "set_data_prop") == "__set__"

    def test_delete_data_descriptor(self, __getattribute__):
        assert __getattribute__(ObjectExample(), "delete_data_prop") == "__delete__"

    def test_instance_attr(self, __getattribute__):
        """An attribute on the instance will be found."""
        assert __getattribute__(ObjectExample(), "ins_attr") == "instance attribute"

    def test_non_data_descriptor(self, __getattribute__):
        """A non-data descriptor on the class will be found."""
        assert __getattribute__(ObjectExample(), "non_data_prop") == "non-data property"

    def test_non_data_descriptor_subclass(self, __getattribute__):
        """A subclass of a non-data descriptor should work."""
        assert (
            __getattribute__(ObjectExample(), "non_data_prop_subclass")
            == "non-data property"
        )

    def test_class_attr(self, __getattribute__):
        """An attribute on the class will be found."""
        assert __getattribute__(ObjectExample(), "class_attr") == "class attribute"

    def test_superclass_attr(self, __getattribute__):
        """An attribute on a superclass will be found."""
        assert (
            __getattribute__(ObjectExample(), "superclass_attr")
            == "superclass attribute"
        )

    def test_missing_attr(self, __getattribute__):
        """AttributeError is raised when an attribute is missing."""
        with pytest.raises(AttributeError):
            __getattribute__(ObjectExample(), "missing_attr")

    def test_bad_attr_name_type(self, __getattribute__):
        """Only strings are acceptable as the attribute name."""
        with pytest.raises(TypeError):
            __getattribute__(ObjectExample(), 42)


@pytest.mark.parametrize(
    "__eq__", [builtins.object.__eq__, desugar.builtins.object.__eq__]
)
class TestEq:
    def test_same(self, __eq__):
        """Same objects result in True."""
        ob = object()
        assert __eq__(ob, ob) is True

    def test_different(self, __eq__):
        """Different objects result in NotImplemented."""
        assert __eq__(object(), object()) is NotImplemented


@pytest.mark.parametrize(
    "__ne__", [builtins.object.__ne__, desugar.builtins.object.__ne__]
)
class TestNe:
    def test_same(self, __ne__):
        """Same objects result in False."""
        ob = object()
        assert __ne__(ob, ob) is False

    def test_different(self, __ne__):
        """Different objects, by default, result in NotImplemented."""
        assert __ne__(object(), object()) is NotImplemented

    def test_defer_to_eq(self, __ne__):
        """__ne__ differs and and negates what __eq__ returns.

        This only applies if the result is not NotImplemented.

        """

        class ImplementEq:
            def __init__(self):
                self.called = False

            def __eq__(self, _):
                self.called = True
                return True

        ob = ImplementEq()

        assert not __ne__(ob, object())
        assert ob.called

    def test_defer_to_eq_not_implemented(self, __ne__):
        """if __eq__ returns NotImplemented, so does __ne__."""

        class EqNotImplemented:
            def __eq__(self, _):
                return NotImplemented

        assert __ne__(EqNotImplemented(), EqNotImplemented()) is NotImplemented

    def test_coercion_false(self, __ne__):
        """If __eq__ does not return NotImplemented and a true value, then
        __ne__ always returns False."""

        class EqTrueNumber:
            def __eq__(self, _):
                return 42

        assert __ne__(EqTrueNumber(), EqTrueNumber()) is False

    def test_coercion_true(self, __ne__):
        """If __eq__ does not return NotImplemented and a false value, then
        __ne__ always returns True."""

        class EqFalseNumber:
            def __eq__(self, _):
                return 0

        assert __ne__(EqFalseNumber(), EqFalseNumber()) is True


@pytest.mark.parametrize("iter", [builtins.iter, desugar.builtins.iter])
class TestIter:
    def test_iterable(self, iter):
        """Return tp.__iter__(obj) when available."""

        iterator = builtins.iter([])

        class Iterable:
            def __iter__(self):
                return iterator

        assert iter(Iterable()) is iterator

    def test_non_iterator(self, iter):
        """TypeError is raised if __iter__() returns a non-iterator."""

        class NonIterable:
            def __iter__(self):
                return 42

        with pytest.raises(TypeError):
            iter(NonIterable())

    def test_iter_is_None(self, iter):
        """If __iter__() is set to None, raise TypeError."""

        class NotIterable:
            __iter__ = None

        with pytest.raises(TypeError):
            iter(NotIterable())

    def test_sequence(self, iter):
        """Create an iterator to go through a sequence, stopping on IndexError."""

        class Sequence:
            def __getitem__(self, index):
                if index < 3:
                    return index
                else:
                    raise IndexError

        iterator = iter(Sequence())

        assert builtins.next(iterator) == 0
        assert builtins.next(iterator) == 1
        assert builtins.next(iterator) == 2
        with pytest.raises(StopIteration):
            builtins.next(iterator)

    def test_sequence_StopIteration(self, iter):
        """Sequence iterator stops on StopIteration."""

        class Sequence:
            def __getitem__(self, index):
                if index < 3:
                    return index
                else:
                    raise StopIteration

        iterator = iter(Sequence())

        assert builtins.next(iterator) == 0
        assert builtins.next(iterator) == 1
        assert builtins.next(iterator) == 2
        with pytest.raises(StopIteration):
            builtins.next(iterator)
        with pytest.raises(StopIteration):
            builtins.next(iterator)

    def test_raise_TypeError(self, iter):
        """With no sentinel, raise TypeError if __iter__() or __getitem__() not defined."""

        def func():
            pass

        with pytest.raises(TypeError):
            iter(func)

    def test_callable(self, iter):
        """If a sentinel is provided, then keep calling the argument until the sentinel is seen."""
        count = -1

        def callable():
            nonlocal count
            count += 1
            return count

        iterator = iter(callable, 3)

        assert builtins.next(iterator) == 0
        assert builtins.next(iterator) == 1
        assert builtins.next(iterator) == 2
        with pytest.raises(StopIteration):
            builtins.next(iterator)
        with pytest.raises(StopIteration):
            builtins.next(iterator)

    def test_callable_StopIteration(self, iter):
        """Callable can raise StopIteration."""
        count = -1

        def callable():
            nonlocal count
            if count >= 3:
                raise StopIteration
            count += 1
            return count

        iterator = iter(callable, 3)

        assert builtins.next(iterator) == 0
        assert builtins.next(iterator) == 1
        assert builtins.next(iterator) == 2
        with pytest.raises(StopIteration):
            builtins.next(iterator)
        with pytest.raises(StopIteration):
            builtins.next(iterator)

    def test_uncallable(self, iter):
        """TypeError is raise if the argument isn't callable."""
        with pytest.raises(TypeError):
            iter(object(), 42)


@pytest.mark.parametrize("next", [builtins.next, desugar.builtins.next])
class TestNext:
    def test_next(self, next):
        """Calls __next__()."""
        iterator = builtins.iter(range(3))

        assert next(iterator) == 0
        assert next(iterator) == 1
        assert next(iterator) == 2
        with pytest.raises(StopIteration):
            next(iterator)

    def test_missing_next(self, next):
        """Raises TypeError if __next__() isn't defined."""
        with pytest.raises(TypeError):
            next(42)

    def test_default(self, next):
        """If 'default' is given, then it is returned when StopIteration is raised."""
        iterator = builtins.iter(range(3))

        default = object()
        assert next(iterator, default) == 0
        assert next(iterator, default) == 1
        assert next(iterator, default) == 2
        assert next(iterator, default) == default


class TestAwait:

    def test_await(self):
        """An object defining `__await__` has that awaited on."""
        class Await(collections.abc.Awaitable):

            def __await__(self):
                yield from range(3)

        assert list(range(3)) == list(desugar.builtins._await(Await()))

    def test_coroutine(self):
        """An object marked as a coroutine can be awaited on."""
        @types.coroutine
        def coro():
            yield from range(3)

        assert list(range(3)) == list(desugar.builtins._await(coro()))

    def test_not_coroutine(self):
        """An object that isn't awaitable triggers a TypeError."""
        with pytest.raises(TypeError):
            list(desugar.builtins._await(None))
