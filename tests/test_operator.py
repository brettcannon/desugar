import operator

import pytest

import desugar.operator


class LHSSub:
    def __sub__(self, other):
        return "__sub__"


class LHSSubNotImplemented:
    def __init__(self):
        self.called = False

    def __sub__(self, other):
        self.called = True
        return NotImplemented


class RHSSub:
    def __rsub__(self, other):
        return "__rsub__"


class RHSSubNotImplemented:
    def __init__(self):
        self.rcalled = False

    def __rsub__(self, other):
        self.rcalled = True
        return NotImplemented


class LHSRHSSub(LHSSub, RHSSub):
    pass


class LHSRHSNotImplementedSub(LHSSubNotImplemented, LHSSub, RHSSubNotImplemented):
    """A subclass for RHS which always returns NotImplemented."""


@pytest.mark.parametrize("sub", [operator.sub, desugar.operator.sub])
class TestSub:

    """Test desugar.operator.sub()."""

    def test_lhs_called(self, sub):
        """__sub__ on the LHS when not a subclass is called."""
        assert sub(LHSSub(), object()) == "__sub__"

    def test_rhs_called(self, sub):
        """__rsub__ on the RHS is called when __sub__ is not defined on the LHS."""
        assert sub(object(), RHSSub()) == "__rsub__"

    def test_lhs_over_rhs(self, sub):
        """__sub__ should be called before __rsub__ when RHS is not a subclass of the LHS."""
        rhs = RHSSubNotImplemented()
        assert sub(LHSSub(), rhs) == "__sub__"
        assert not rhs.rcalled

    def test_rhs_subclass_over_lhs(self, sub):
        """If the RHS is a subclass of LHS then call __rsub__ first."""
        assert sub(LHSSub(), LHSRHSSub()) == "__rsub__"

    def test_rhs_subclass_but_not_implemented(self, sub):
        """If the RHS is a subclass but returns NotImplemented, call lhs.__sub__()."""
        lhs = LHSSub()
        rhs = LHSRHSNotImplementedSub()
        assert sub(lhs, rhs) == "__sub__"
        assert not rhs.called
        assert rhs.rcalled

    def test_rhs_not_substituting_for_lhs(self, sub):
        """If the RHS defines __sub__ but not the LHS, it is still not called."""
        with pytest.raises(TypeError):
            sub(object(), LHSSub())

    def test_lhs_not_substituting_for_rhs(self, sub):
        """If the LHS defines __rsub__ but not the RHS, it is still not called."""
        with pytest.raises(TypeError):
            sub(RHSSub(), object())

    def test_lhs_not_implemented(self, sub):
        """If the LHS returns NotImplemented, raise TypeError."""
        with pytest.raises(TypeError):
            sub(LHSSubNotImplemented(), object())

    def test_rhs_not_implemented(self, sub):
        """If the RHS returns NotImplemented, raise TypeError."""
        with pytest.raises(TypeError):
            sub(object(), RHSSubNotImplemented())

    def test_lhs_not_implemented_but_rhs_is(self, sub):
        """If lhs.__sub__() returns NotImplemented, call RHS.__rsub__()."""
        lhs = LHSSubNotImplemented()
        assert sub(lhs, RHSSub()) == "__rsub__"
        assert lhs.called

    def test_both_sides_not_implemented(self, sub):
        """If both lhs.__sub__() and rhs.__rsub__() return NotImplemented, raise TypeError."""
        lhs = LHSSubNotImplemented()
        rhs = RHSSubNotImplemented()
        with pytest.raises(TypeError):
            sub(lhs, rhs)
