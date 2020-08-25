import operator
import sys

import pytest

import desugar.operator
from . import common


class AugmentedAssignmentTests:

    """Tests for augmented arithmetic assignment.

    Subclasses are expected to provide the actual assignment to test.

    """

    def test_inplace(self, op):
        """Providing __i*__ should work."""
        assert op(common.Lvalue(), object()) == self.lvalue_method

    def test_lhs_fallback(self, op):
        """If __i*__ is not defined, fallback to __*__."""
        assert op(common.LHS(), object()) == self.lhs_method

    def test_lhs_fallback_from_not_implemented(self, op):
        """If __i*__ returned NotImplemented fall back to __*__."""
        # https://bugs.python.org/issue38302
        if sys.version_info[:2] < (3, 10) and op.__name__ == "ipow":
            pytest.skip("CPython's **= implementation does not call __pow__")
        lvalue = common.LvalueNotImplementedLHS()
        result = op(lvalue, object())
        assert result == self.lhs_method
        assert lvalue.icalled == 1

    def test_rhs_fallback(self, op):
        """If __i*__ and __*__ are not defined, fallback to __r*__."""
        assert op(object(), common.RHS()) == self.rhs_method

    def test_no_methods(self, op):
        """TypeError is raised if no appropriate methods are available."""
        with pytest.raises(TypeError):
            op(object(), object())

    def test_all_not_implemented(self, op):
        """TypeError is raised if all appropriate methods return NotImplemented.

        When the LHS and RHS are the same type then only __i*__ and __*__ are
        called.

        """
        lvalue = common.LvalueLHSRHSNotImplemented()
        rvalue = common.LvalueLHSRHSNotImplemented()
        with pytest.raises(TypeError):
            op(lvalue, rvalue)
        assert lvalue.icalled == 1
        # https://bugs.python.org/issue38302
        if sys.version_info[:2] < (3, 10) and op.__name__ == "ipow":
            return
        assert lvalue.called == 1
        assert not lvalue.rcalled
        assert not rvalue.icalled
        assert not rvalue.called
        assert not rvalue.rcalled

    def test_inplace_when_others_not_implemented(self, op):
        """__i*__ used when __*__ and __r*__ return NotImplemented."""
        op(common.LHSRHSNotImplementedLvalue(), object()) == self.lvalue_method

    def test_function_name(self, op):
        short_name = self.lhs_method[2:-2]
        assert short_name in op.__name__
        assert short_name in op.__qualname__


@pytest.mark.parametrize("op", [operator.iadd, desugar.operator.iadd])
class TestAdditionInPlace(AugmentedAssignmentTests):

    lvalue_method = "__iadd__"
    lhs_method = "__add__"
    rhs_method = "__radd__"


@pytest.mark.parametrize("op", [operator.isub, desugar.operator.isub])
class TestSubtractionInPlace(AugmentedAssignmentTests):

    lvalue_method = "__isub__"
    lhs_method = "__sub__"
    rhs_method = "__rsub__"


@pytest.mark.parametrize("op", [operator.imul, desugar.operator.imul])
class TestMultiplicationInPlace(AugmentedAssignmentTests):

    lvalue_method = "__imul__"
    lhs_method = "__mul__"
    rhs_method = "__rmul__"


@pytest.mark.parametrize("op", [operator.imatmul, desugar.operator.imatmul])
class TestMatrixMultiplicationInPlace(AugmentedAssignmentTests):

    lvalue_method = "__imatmul__"
    lhs_method = "__matmul__"
    rhs_method = "__rmatmul__"


@pytest.mark.parametrize("op", [operator.itruediv, desugar.operator.itruediv])
class TestTrueDivisionInPlace(AugmentedAssignmentTests):

    lvalue_method = "__itruediv__"
    lhs_method = "__truediv__"
    rhs_method = "__rtruediv__"


@pytest.mark.parametrize("op", [operator.ifloordiv, desugar.operator.ifloordiv])
class TestFloorDivisionInPlace(AugmentedAssignmentTests):

    lvalue_method = "__ifloordiv__"
    lhs_method = "__floordiv__"
    rhs_method = "__rfloordiv__"


@pytest.mark.parametrize("op", [operator.imod, desugar.operator.imod])
class TestModuloInPlace(AugmentedAssignmentTests):

    lvalue_method = "__imod__"
    lhs_method = "__mod__"
    rhs_method = "__rmod__"


@pytest.mark.parametrize("op", [operator.ipow, desugar.operator.ipow])
class TestPowerInPlace(AugmentedAssignmentTests):

    lvalue_method = "__ipow__"
    lhs_method = "__pow__"
    rhs_method = "__rpow__"


@pytest.mark.parametrize("op", [operator.ilshift, desugar.operator.ilshift])
class TestLeftShiftInPlace(AugmentedAssignmentTests):

    lvalue_method = "__ilshift__"
    lhs_method = "__lshift__"
    rhs_method = "__rlshift__"


@pytest.mark.parametrize("op", [operator.irshift, desugar.operator.irshift])
class TestRightShiftInPlace(AugmentedAssignmentTests):

    lvalue_method = "__irshift__"
    lhs_method = "__rshift__"
    rhs_method = "__rrshift__"


@pytest.mark.parametrize("op", [operator.iand, desugar.operator.iand])
class TestAndInPlace(AugmentedAssignmentTests):

    lvalue_method = "__iand__"
    lhs_method = "__and__"
    rhs_method = "__rand__"


@pytest.mark.parametrize("op", [operator.ixor, desugar.operator.ixor])
class TestExclusiveOrInPlace(AugmentedAssignmentTests):

    lvalue_method = "__ixor__"
    lhs_method = "__xor__"
    rhs_method = "__rxor__"


@pytest.mark.parametrize("op", [operator.ior, desugar.operator.ior])
class TestOrInPlace(AugmentedAssignmentTests):

    lvalue_method = "__ior__"
    lhs_method = "__or__"
    rhs_method = "__ror__"
