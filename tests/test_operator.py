import operator

import pytest

import desugar.operator


class LHS:
    def __add__(self, _):
        return "__add__"

    def __sub__(self, _):
        return "__sub__"

    def __mul__(self, _):
        return "__mul__"

    def __matmul__(self, _):
        return "__matmul__"


class LHSNotImplemented:
    def __init__(self):
        self.called = False

    def __add__(self, _):
        self.called = True
        return NotImplemented

    def __sub__(self, _):
        self.called = True
        return NotImplemented

    def __mul__(self, _):
        self.called = True
        return NotImplemented

    def __matmul__(self, _):
        self.called = True
        return NotImplemented


class RHS:
    def __radd__(self, _):
        return "__radd__"

    def __rsub__(self, _):
        return "__rsub__"

    def __rmul__(self, _):
        return "__rmul__"

    def __rmatmul__(self, _):
        return "__rmatmul__"


class RHSNotImplemented:
    def __init__(self):
        self.rcalled = False

    def __radd__(self, _):
        self.rcalled = True
        return NotImplemented

    def __rsub__(self, _):
        self.rcalled = True
        return NotImplemented

    def __rmul__(self, _):
        self.rcalled = True
        return NotImplemented

    def __rmatmul__(self, _):
        self.rcalled = True
        return NotImplemented


class LHSRHS(LHS, RHS):
    pass


class LHSRHSNotImplemented(LHSNotImplemented, LHS, RHSNotImplemented):
    """A subclass for RHS which always returns NotImplemented."""


class BinaryOperationTests:

    """Standard tests for binary operators.

    Subclasses are expected to provide the appropriate details to test a binary
    operation.

    """

    def test_lhs_called(self, op):
        """__*__ on the LHS when not a subclass is called."""
        assert op(LHS(), object()) == self.lhs_method

    def test_rhs_called(self, op):
        """__r*__ on the RHS is called when __*__ is not defined on the LHS."""
        assert op(object(), RHS()) == self.rhs_method

    def test_lhs_over_rhs(self, op):
        """__*__ should be called before __r*__ when RHS is not a subclass of the LHS."""
        rhs = RHSNotImplemented()
        assert op(LHS(), rhs) == self.lhs_method
        assert not rhs.rcalled

    def test_rhs_subclass_over_lhs(self, op):
        """If the RHS is a subclass of LHS then call __r*__ first."""
        assert op(LHS(), LHSRHS()) == self.rhs_method

    def test_both_subclasses(self, op):
        """When both the LHS and RHS are of the same type, call LHS.__*__() first."""
        assert op(LHSRHS(), LHSRHS()) == self.lhs_method

    def test_rhs_subclass_but_not_implemented(self, op):
        """If the RHS is a subclass but returns NotImplemented, call lhs.__*__()."""
        lhs = LHS()
        rhs = LHSRHSNotImplemented()
        assert op(lhs, rhs) == self.lhs_method
        assert not rhs.called  # rhs.__*__() should not be called at any point.
        assert rhs.rcalled

    def test_rhs_not_substituting_for_lhs(self, op):
        """If the RHS defines __*__ but not the LHS, it is still not called."""
        with pytest.raises(TypeError):
            op(object(), LHS())

    def test_lhs_not_substituting_for_rhs(self, op):
        """If the LHS defines __r*__ but not the RHS, it is still not called."""
        with pytest.raises(TypeError):
            op(RHS(), object())

    def test_lhs_not_implemented(self, op):
        """If the LHS returns NotImplemented, raise TypeError."""
        with pytest.raises(TypeError):
            op(LHSNotImplemented(), object())

    def test_rhs_not_implemented(self, op):
        """If the RHS returns NotImplemented, raise TypeError."""
        with pytest.raises(TypeError):
            op(object(), RHSNotImplemented())

    def test_lhs_not_implemented_but_rhs_is(self, op):
        """If lhs.__*__() returns NotImplemented, call RHS.__r*__()."""
        lhs = LHSNotImplemented()
        assert op(lhs, RHS()) == self.rhs_method
        assert lhs.called

    def test_both_sides_not_implemented(self, op):
        """If both lhs.__*__() and rhs.__r*__() return NotImplemented, raise TypeError."""
        lhs = LHSNotImplemented()
        rhs = RHSNotImplemented()
        with pytest.raises(TypeError):
            op(lhs, rhs)


@pytest.mark.parametrize("op", [operator.add, desugar.operator.add])
class TestAddition(BinaryOperationTests):

    """Tests for desugar.operator.add()."""

    lhs_method = "__add__"
    rhs_method = "__radd__"


@pytest.mark.parametrize("op", [operator.sub, desugar.operator.sub])
class TestSubtaction(BinaryOperationTests):

    """Tests for desugar.operator.sub()."""

    lhs_method = "__sub__"
    rhs_method = "__rsub__"


@pytest.mark.parametrize("op", [operator.mul, desugar.operator.mul])
class TestMultiplicaiton(BinaryOperationTests):

    """Tests for desugar.operator.mul()."""

    lhs_method = "__mul__"
    rhs_method = "__rmul__"


@pytest.mark.parametrize("op", [operator.matmul, desugar.operator.matmul])
class TestMatrixMultiplicaiton(BinaryOperationTests):

    """Tests for desugar.operator.matmul()."""

    lhs_method = "__matmul__"
    rhs_method = "__rmatmul__"
