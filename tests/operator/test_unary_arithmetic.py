import operator

import pytest

import desugar.operator


class UnaryOperator:

    """A class implementing all unary operators."""

    def __neg__(self):
        return "__neg__"

    def __pos__(self):
        return "__pos__"

    def __invert__(self):
        return "__invert__"


class NoOperator:

    """A class with no unary operators."""


class UnaryOperationTests:
    def test_called(self, op):
        """Test that the unary operator is called as appropriate."""
        assert op(UnaryOperator()) == self.method

    def test_no_method(self, op):
        """TypeError should be raised if the unary operator is missing."""
        with pytest.raises(TypeError):
            op(NoOperator())


@pytest.mark.parametrize("op", [operator.neg, desugar.operator.neg])
class TestNeg(UnaryOperationTests):

    """Tests for desugar.operator.__neg__()."""

    method = "__neg__"


@pytest.mark.parametrize("op", [operator.pos, desugar.operator.pos])
class TestPos(UnaryOperationTests):

    """Tests for desugar.operator.__pos__()."""

    method = "__pos__"


@pytest.mark.parametrize("op", [operator.invert, desugar.operator.invert])
class TestInvert(UnaryOperationTests):

    """Tests for desugar.operator.__invert__()."""

    method = "__invert__"
