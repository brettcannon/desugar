import operator

import pytest

import desugar.operator

from . import common


class BinaryOperationTests:

    """Standard tests for binary operators.

    Subclasses are expected to provide the appropriate details to test a binary
    operation.

    """

    def test_lhs_called(self, op):
        """__*__ on the LHS when not a subclass is called."""
        assert op(common.LHS(), object()) == self.lhs_method

    def test_rhs_called(self, op):
        """__r*__ on the RHS is called when __*__ is not defined on the LHS."""
        assert op(object(), common.RHS()) == self.rhs_method

    def test_lhs_over_rhs(self, op):
        """__*__ should be called before __r*__ when RHS is not a subclass of the LHS."""
        rhs = common.RHSNotImplemented()
        assert op(common.LHS(), rhs) == self.lhs_method
        assert not rhs.rcalled

    def test_rhs_subclass_over_lhs(self, op):
        """If the RHS is a subclass of LHS then call __r*__ first."""
        assert op(common.LHS(), common.LHSRHS()) == self.rhs_method

    def test_rhs_subclass_with_same_methods(self, op):
        """If the RHS is a subclass of the LHS **but** __r*__ is the same object, call __*__ first."""
        assert op(common.LHSRHS(), common.LHSRHSSubclass()) == self.lhs_method

    def test_both_subclasses(self, op):
        """When both the LHS and RHS are of the same type, call LHS.__*__() first."""
        assert op(common.LHSRHS(), common.LHSRHS()) == self.lhs_method

    def test_rhs_subclass_but_not_implemented(self, op):
        """If the RHS is a subclass but returns NotImplemented, call lhs.__*__()."""
        lhs = common.LHS()
        rhs = common.LHSRHSNotImplemented()
        assert op(lhs, rhs) == self.lhs_method
        assert not rhs.called  # rhs.__*__() should not be called at any point.
        assert rhs.rcalled == 1

    def test_rhs_not_substituting_for_lhs(self, op):
        """If the RHS defines __*__ but not the LHS, it is still not called."""
        with pytest.raises(TypeError):
            op(object(), common.LHS())

    def test_lhs_not_substituting_for_rhs(self, op):
        """If the LHS defines __r*__ but not the RHS, it is still not called."""
        with pytest.raises(TypeError):
            op(common.RHS(), object())

    def test_lhs_not_implemented(self, op):
        """If the LHS returns NotImplemented, raise TypeError."""
        lhs = common.LHSNotImplemented()
        with pytest.raises(TypeError):
            op(lhs, object())
        assert lhs.called == 1

    def test_rhs_not_implemented(self, op):
        """If the RHS returns NotImplemented, raise TypeError."""
        rhs = common.RHSNotImplemented()
        with pytest.raises(TypeError):
            op(object(), rhs)
        assert rhs.rcalled == 1

    def test_lhs_not_implemented_but_rhs_is(self, op):
        """If lhs.__*__() returns NotImplemented, call RHS.__r*__()."""
        lhs = common.LHSNotImplemented()
        assert op(lhs, common.RHS()) == self.rhs_method
        assert lhs.called == 1

    def test_both_sides_not_implemented(self, op):
        """If both lhs.__*__() and rhs.__r*__() return NotImplemented, raise TypeError."""
        lhs = common.LHSNotImplemented()
        rhs = common.RHSNotImplemented()
        with pytest.raises(TypeError):
            op(lhs, rhs)
        assert lhs.called == 1
        assert rhs.rcalled == 1

    def test_all_methods_not_implemented_same_type(self, op):
        """If all related methods return NotImplemented, TypeError is raised.

        When the types of both sides are the same then only lhs.__*__ is called.

        """
        lhs = common.LHSRHSNotImplemented()
        rhs = common.LHSRHSNotImplemented()
        with pytest.raises(TypeError):
            op(lhs, rhs)
        assert lhs.called == 1
        assert not lhs.rcalled
        assert not rhs.called
        assert not rhs.rcalled

    def test_all_methods_not_implemented_different_types(self, op):
        lhs = common.LHSRHSNotImplemented()
        rhs = common.LHSRHSNotImplementedSubclass()
        with pytest.raises(TypeError):
            op(lhs, rhs)
        assert lhs.called == 1
        assert not lhs.rcalled
        assert not rhs.called
        assert rhs.rcalled == 1

    def test_function_name(self, op):
        """The method's name should be appropriate."""
        op_name = self.lhs_method[2:-2]
        assert op_name in op.__name__
        assert op_name in op.__qualname__


@pytest.mark.parametrize("op", [operator.add, desugar.operator.add])
class TestAddition(BinaryOperationTests):

    """Tests for desugar.operator.add()."""

    lhs_method = "__add__"
    rhs_method = "__radd__"


@pytest.mark.parametrize("op", [operator.sub, desugar.operator.sub])
class TestSubtraction(BinaryOperationTests):

    """Tests for desugar.operator.sub()."""

    lhs_method = "__sub__"
    rhs_method = "__rsub__"


@pytest.mark.parametrize("op", [operator.mul, desugar.operator.mul])
class TestMultiplicaiton(BinaryOperationTests):

    """Tests for desugar.operator.mul()."""

    lhs_method = "__mul__"
    rhs_method = "__rmul__"


@pytest.mark.parametrize("op", [operator.matmul, desugar.operator.matmul])
class TestMatrixMultiplication(BinaryOperationTests):

    """Tests for desugar.operator.matmul()."""

    lhs_method = "__matmul__"
    rhs_method = "__rmatmul__"


@pytest.mark.parametrize("op", [operator.truediv, desugar.operator.truediv])
class TestTrueDivision(BinaryOperationTests):

    """Tests for desugar.operator.truediv()."""

    lhs_method = "__truediv__"
    rhs_method = "__rtruediv__"


@pytest.mark.parametrize("op", [operator.floordiv, desugar.operator.floordiv])
class TestFloorDivision(BinaryOperationTests):

    """Tests for desugar.operator.floordiv()."""

    lhs_method = "__floordiv__"
    rhs_method = "__rfloordiv__"


@pytest.mark.parametrize("op", [operator.mod, desugar.operator.mod])
class TestModulo(BinaryOperationTests):

    """Tests for desugar.operator.mod()."""

    lhs_method = "__mod__"
    rhs_method = "__rmod__"


@pytest.mark.parametrize("op", [operator.pow, desugar.operator.pow])
class TestPower(BinaryOperationTests):

    """Tests for desugar.operator.pow()."""

    lhs_method = "__pow__"
    rhs_method = "__rpow__"


@pytest.mark.parametrize("op", [operator.lshift, desugar.operator.lshift])
class TestLeftShift(BinaryOperationTests):

    """Tests for desugar.operator.lshift()."""

    lhs_method = "__lshift__"
    rhs_method = "__rlshift__"


@pytest.mark.parametrize("op", [operator.rshift, desugar.operator.rshift])
class TestRightShift(BinaryOperationTests):

    """Tests for desugar.operator.rshift()."""

    lhs_method = "__rshift__"
    rhs_method = "__rrshift__"


@pytest.mark.parametrize("op", [operator.and_, desugar.operator.and_])
class TestAnd(BinaryOperationTests):

    """Tests for desugar.operator.and_()."""

    lhs_method = "__and__"
    rhs_method = "__rand__"


@pytest.mark.parametrize("op", [operator.xor, desugar.operator.xor])
class TestExclusiveOr(BinaryOperationTests):

    """Tests for desugar.operator.xor()."""

    lhs_method = "__xor__"
    rhs_method = "__rxor__"


@pytest.mark.parametrize("op", [operator.or_, desugar.operator.or_])
class TestOr(BinaryOperationTests):

    """Tests for desugar.operator.or_()."""

    lhs_method = "__or__"
    rhs_method = "__ror__"
