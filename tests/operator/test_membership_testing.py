import operator

import pytest

import desugar.operator


class Contains:
    def __contains__(self, item):
        return item


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

    def test_contains_non_bool(self, __contains__):
        """The return value of __contains__ is passed through operator.truth()."""
        assert __contains__(Contains(), 42) is True
        assert __contains__(Contains(), 0) is False

    def test_contains_none(self, __contains__):
        """__contains__ returning None raises a TypeError."""

        class ContainsNone:
            __contains__ = None
            # XXX iter

        with pytest.raises(TypeError):
            __contains__(ContainsNone, True)
