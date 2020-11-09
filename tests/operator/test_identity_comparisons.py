import operator

import pytest

import desugar.operator


@pytest.mark.parametrize("is_", [operator.is_, desugar.operator.is_])
class TestIs:

    """Tests for identity comparison: `is`."""

    def test_same(self, is_):
        assert is_(1, 1)

    def test_different(self, is_):
        assert not is_(1, 2)

    def test_different_types(self, is_):
        assert not is_(1, "str")


@pytest.mark.parametrize("is_not", [operator.is_not, desugar.operator.is_not])
class TestIsNot:

    """Tests for identity difference: `is not`."""

    def test_different(self, is_not):
        assert is_not(1, 2)

    def test_same(self, is_not):
        assert not is_not(1, 1)

    def test_different_types(self, is_not):
        assert is_not(1, "str")
