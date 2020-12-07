import operator

import pytest

import desugar.operator


class Contains:
    def __contains__(self, item):
        return item


class Iterable:
    def __init__(self, iterator):
        self._iter = iterator

    def __iter__(self):
        yield from self._iter


@pytest.mark.parametrize(
    "__contains__", [operator.contains, desugar.operator.__contains__]
)
class TestMembershipTesting:
    def test_non_container(self, __contains__):
        """Raise TypeError when a non-container is checked against."""
        with pytest.raises(TypeError):
            __contains__(42, "does not matter")

    def test_contains(self, __contains__):
        """__contains__ returning True or False results in that being returned."""
        assert __contains__(Contains(), True) is True
        assert __contains__(Contains(), False) is False

    def test_contains_non_bool(self, __contains__):
        """The return value of __contains__ is passed through operator.truth()."""
        assert __contains__(Contains(), 42) is True
        assert __contains__(Contains(), 0) is False

    def test_contains_none(self, __contains__):
        """__contains__ returning None raises a TypeError."""

        class ContainsNone:
            __contains__ = None

            def __iter__(self):
                raise RuntimeError

        with pytest.raises(TypeError):
            __contains__(ContainsNone(), True)

    def test_iterable_id_success(self, __contains__):
        """Search via __iter__ for an object that matches via id()."""
        search_for = object()
        iterable = Iterable(iter([search_for]))
        assert __contains__(iterable, search_for) is True

    def test_iterable_eq_success(self, __contains__):
        """Search via __iter__ for an object that matches via equality."""

        class Equal:
            def __eq__(self, other):
                return other == 42

        iterable = Iterable(iter([Equal()]))
        assert __contains__(iterable, 42) is True

    def test_iterable_failure(self, __contains__):
        """Iterable does not contain the item."""
        iterable = Iterable(iter([]))
        assert __contains__(iterable, 42) is False

    def test_iterable_undefined(self, __contains__):
        """Defining neither __contains__ nor __iter__ results in a TypeError."""
        with pytest.raises(TypeError):
            __contains__(object(), 42)
