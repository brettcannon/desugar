import operator

import pytest

import desugar.operator


class LHS:

    """__*__ methods returning their own name."""

    def __add__(self, _):
        return "__add__"

    def __sub__(self, _):
        return "__sub__"

    def __mul__(self, _):
        return "__mul__"

    def __matmul__(self, _):
        return "__matmul__"

    def __truediv__(self, _):
        return "__truediv__"

    def __floordiv__(self, _):
        return "__floordiv__"

    def __mod__(self, _):
        return "__mod__"

    def __pow__(self, _):
        return "__pow__"

    def __lshift__(self, _):
        return "__lshift__"

    def __rshift__(self, _):
        return "__rshift__"

    def __and__(self, _):
        return "__and__"

    def __xor__(self, _):
        return "__xor__"

    def __or__(self, _):
        return "__or__"


class LHSNotImplemented:

    """__*__ methods returning NotImplemented."""

    def __init__(self):
        super().__init__()
        self.called = 0

    def __add__(self, _):
        self.called += 1
        return NotImplemented

    def __sub__(self, _):
        self.called += 1
        return NotImplemented

    def __mul__(self, _):
        self.called += 1
        return NotImplemented

    def __matmul__(self, _):
        self.called += 1
        return NotImplemented

    def __truediv__(self, _):
        self.called += 1
        return NotImplemented

    def __floordiv__(self, _):
        self.called += 1
        return NotImplemented

    def __mod__(self, _):
        self.called += 1
        return NotImplemented

    def __pow__(self, _):
        self.called += 1
        return NotImplemented

    def __lshift__(self, _):
        self.called += 1
        return NotImplemented

    def __rshift__(self, _):
        self.called += 1
        return NotImplemented

    def __and__(self, _):
        self.called += 1
        return NotImplemented

    def __xor__(self, _):
        self.called += 1
        return NotImplemented

    def __or__(self, _):
        self.called += 1
        return NotImplemented


class RHS:

    """__r*__ methods returning their name."""

    def __radd__(self, _):
        return "__radd__"

    def __rsub__(self, _):
        return "__rsub__"

    def __rmul__(self, _):
        return "__rmul__"

    def __rmatmul__(self, _):
        return "__rmatmul__"

    def __rtruediv__(self, _):
        return "__rtruediv__"

    def __rfloordiv__(self, _):
        return "__rfloordiv__"

    def __rmod__(self, _):
        return "__rmod__"

    def __rpow__(self, _):
        return "__rpow__"

    def __rlshift__(self, _):
        return "__rlshift__"

    def __rrshift__(self, _):
        return "__rrshift__"

    def __rand__(self, _):
        return "__rand__"

    def __rxor__(self, _):
        return "__rxor__"

    def __ror__(self, _):
        return "__ror__"


class RHSNotImplemented:

    """__r*__ methods returning NotImplemented."""

    def __init__(self):
        super().__init__()
        self.rcalled = 0

    def __radd__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __rsub__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __rmul__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __rmatmul__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __rtruediv__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __rfloordiv__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __rmod__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __rpow__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __rlshift__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __rrshift__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __rand__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __rxor__(self, _):
        self.rcalled += 1
        return NotImplemented

    def __ror__(self, _):
        self.rcalled += 1
        return NotImplemented


class LHSRHS(LHS, RHS):

    """Class that implements both __*__ and __r*__."""


class LHSRHSSubclass(LHSRHS):

    """A subclass implementing both __*__ and __r*__ which does not differ from its superclass."""


class LHSRHSNotImplemented(LHSNotImplemented, LHS, RHSNotImplemented):

    """A subclass which always returns NotImplemented."""


class LHSRHSNotImplementedSubclass(LHSRHSNotImplemented):

    """A subclass which always returns NotImplemented that is a different type
    of the superclass."""


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

    def test_rhs_subclass_with_same_methods(self, op):
        """If the RHS is a subclass of the LHS **but** __r*__ is the same object, call __*__ first."""
        assert op(LHSRHS(), LHSRHSSubclass()) == self.lhs_method

    def test_both_subclasses(self, op):
        """When both the LHS and RHS are of the same type, call LHS.__*__() first."""
        assert op(LHSRHS(), LHSRHS()) == self.lhs_method

    def test_rhs_subclass_but_not_implemented(self, op):
        """If the RHS is a subclass but returns NotImplemented, call lhs.__*__()."""
        lhs = LHS()
        rhs = LHSRHSNotImplemented()
        assert op(lhs, rhs) == self.lhs_method
        assert not rhs.called  # rhs.__*__() should not be called at any point.
        assert rhs.rcalled == 1

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
        lhs = LHSNotImplemented()
        with pytest.raises(TypeError):
            op(lhs, object())
        assert lhs.called == 1

    def test_rhs_not_implemented(self, op):
        """If the RHS returns NotImplemented, raise TypeError."""
        rhs = RHSNotImplemented()
        with pytest.raises(TypeError):
            op(object(), rhs)
        assert rhs.rcalled == 1

    def test_lhs_not_implemented_but_rhs_is(self, op):
        """If lhs.__*__() returns NotImplemented, call RHS.__r*__()."""
        lhs = LHSNotImplemented()
        assert op(lhs, RHS()) == self.rhs_method
        assert lhs.called == 1

    def test_both_sides_not_implemented(self, op):
        """If both lhs.__*__() and rhs.__r*__() return NotImplemented, raise TypeError."""
        lhs = LHSNotImplemented()
        rhs = RHSNotImplemented()
        with pytest.raises(TypeError):
            op(lhs, rhs)
        assert lhs.called == 1
        assert rhs.rcalled == 1

    def test_all_methods_not_implemented_same_type(self, op):
        """If all related methods return NotImplemented, TypeError is raised.

        When the types of both sides are the same then only lhs.__*__ is called.

        """
        lhs = LHSRHSNotImplemented()
        rhs = LHSRHSNotImplemented()
        with pytest.raises(TypeError):
            op(lhs, rhs)
        assert lhs.called == 1
        assert not lhs.rcalled
        assert not rhs.called
        assert not rhs.rcalled

    def test_all_methods_not_implemented_different_types(self, op):
        lhs = LHSRHSNotImplemented()
        rhs = LHSRHSNotImplementedSubclass()
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


class Lvalue:

    """Implement __i*__ methods."""

    def __iadd__(self, _):
        return "__iadd__"

    def __isub__(self, _):
        return "__isub__"


class LvalueNotImplemented:

    """__i*__ methods which return NotImplemented."""

    def __init__(self):
        super().__init__()
        self.icalled = 0

    def __iadd__(self, _):
        self.icalled += 1
        return NotImplemented

    def __isub__(self, _):
        self.icalled += 1
        return NotImplemented


class LvalueNotImplementedLHS(LvalueNotImplemented, LHS):

    """__i*__ returns NotImplemented, __*__ implemented."""


class LvalueLHSRHSNotImplemented(
    LvalueNotImplemented, LHSNotImplemented, RHSNotImplemented
):

    """__*__, __r*__, and __i*__ all return NotImplemented."""


class LHSRHSNotImplementedLvalue(LHSRHSNotImplemented, Lvalue):

    """__i*__ implemented, __*__, __r*__ return NotImplemented."""


class AugmentedAssignmentTests:

    """Tests for augmented arithmetic assignment.

    Subclasses are expected to provide the actual assignment to test.

    """

    def test_inplace(self, op):
        """Providing __i*__ should work."""
        assert op(Lvalue(), object()) == self.lvalue_method

    def test_lhs_fallback(self, op):
        """If __i*__ is not defined, fallback to __*__."""
        assert op(LHS(), object()) == self.lhs_method

    def test_lhs_fallback_from_not_implemented(self, op):
        """If __i*__ returned NotImplemented fall back to __*__."""
        lvalue = LvalueNotImplementedLHS()
        assert op(lvalue, object()) == self.lhs_method
        assert lvalue.icalled == 1

    def test_rhs_fallback(self, op):
        """If __i*__ and __*__ are not defined, fallback to __r*__."""
        assert op(object(), RHS()) == self.rhs_method

    def test_no_methods(self, op):
        """TypeError is raised if no appropriate methods are available."""
        with pytest.raises(TypeError):
            op(object(), object())

    def test_all_not_implemented(self, op):
        """TypeError is raised if all appropriate methods return NotImplemented.

        When the LHS and RHS are the same type then only __i*__ and __*__ are
        called.

        """
        lvalue = LvalueLHSRHSNotImplemented()
        rvalue = LvalueLHSRHSNotImplemented()
        with pytest.raises(TypeError):
            op(lvalue, rvalue)
        assert lvalue.icalled == 1
        assert lvalue.called == 1
        assert not lvalue.rcalled
        assert not rvalue.icalled
        assert not rvalue.called
        assert not rvalue.rcalled

    def test_inplace_when_others_not_implemented(self, op):
        """__i*__ used when __*__ and __r*__ return NotImplemented."""
        op(LHSRHSNotImplementedLvalue(), object()) == self.lvalue_method

    def test_function_name(self, op):
        short_name = self.lhs_method[2:-2]
        assert short_name in op.__name__
        assert short_name in op.__qualname__


@pytest.mark.parametrize("op", [operator.iadd, desugar.operator.iadd])
class TestAdditionInplace(AugmentedAssignmentTests):

    lvalue_method = "__iadd__"
    lhs_method = "__add__"
    rhs_method = "__radd__"


@pytest.mark.parametrize("op", [operator.isub, desugar.operator.isub])
class TestSubtractionInplace(AugmentedAssignmentTests):

    lvalue_method = "__isub__"
    lhs_method = "__sub__"
    rhs_method = "__rsub__"


# @pytest.mark.parametrize("op", [operator.iXXX, desugar.operator.iXXX])
# class TestXXXInplace(AugmentedAssignmentTests):

#     lvalue_method = "__iXXX__"
#     lhs_method = "__XXX__"
#     rhs_method = "__rXXX__"
