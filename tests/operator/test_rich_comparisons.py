import operator

import pytest

import desugar.operator

from . import common


class RichComparisonTests:
    def test_method_only(self, op):
        """When only the method is defined, use that method."""
        assert op(self.cls(), object()) == self.method

    def test_method_first(self, op):
        """When both the method and its reflection are defined, call the method first."""
        assert op(self.cls(), self.reflected_cls()) == self.method

    def test_reflected_only(self, op):
        """When only the reflected method is defined, use that method."""
        assert op(object(), self.reflected_cls()) == self.reflected_method

    def test_method_not_implemented(self, op):
        """When only the method is implemented and it returns NotImplemented, raise TypeError."""
        call_order = []
        lhs = common.ComparisonsNotImplemented(call_order)

        if self.generally is None:
            with pytest.raises(TypeError):
                op(lhs, object())
        else:
            assert self.generally == op(lhs, object())
        assert call_order == [(lhs, self.method)]

    def test_reflection_not_implemented(self, op):
        """When only the reflection is defined and it returns NotImplemented, raise TypeError."""
        call_order = []
        rhs = common.ComparisonsNotImplemented(call_order)

        if self.generally is None:
            with pytest.raises(TypeError):
                op(object(), rhs)
        else:
            assert self.generally == op(object(), rhs)
        assert call_order == [(rhs, self.reflected_method)]

    def test_method_then_reflection(self, op):
        """When different types, call the method first and then its reflection."""
        call_order = []
        lhs = common.ComparisonsNotImplemented(call_order)
        rhs = common.DifferentComparisonsNotImplemented(call_order)

        if self.generally is None:
            with pytest.raises(TypeError):
                op(lhs, rhs)
        else:
            assert self.generally == op(lhs, rhs)
        assert call_order == [(lhs, self.method), (rhs, self.reflected_method)]

    def test_method_then_reflection_same_class(self, op):
        """When same type, call the method first and then its reflection."""
        call_order = []
        lhs = common.ComparisonsNotImplemented(call_order)
        rhs = common.ComparisonsNotImplemented(call_order)

        if self.generally is None:
            with pytest.raises(TypeError):
                op(lhs, rhs)
        else:
            assert self.generally == op(lhs, rhs)
        assert call_order == [(lhs, self.method), (rhs, self.reflected_method)]

    def test_reflection_then_method_subclasses(self, op):
        """When the RHS is a proper subclass, call the reflected method first."""
        call_order = []
        lhs = common.ComparisonsNotImplemented(call_order)
        rhs = common.ComparisonsNotImplementedSubclass(call_order)

        if self.generally is None:
            with pytest.raises(TypeError):
                op(lhs, rhs)
        else:
            assert self.generally == op(lhs, rhs)
        assert call_order == [(rhs, self.reflected_method), (lhs, self.method)]

    def test_function_name(self, op):
        if op.__module__ != desugar.operator.__name__:
            pytest.skip("only check function names for desugar")
        assert op.__name__ == self.method
        assert op.__qualname__ == self.method


@pytest.mark.parametrize("op", [operator.gt, desugar.operator.__gt__])
class TestGreaterThan(RichComparisonTests):

    method = "__gt__"
    cls = common.GtEqGeComparisons
    reflected_method = "__lt__"
    reflected_cls = common.LtNeLeComparisons
    generally = None


@pytest.mark.parametrize("op", [operator.lt, desugar.operator.__lt__])
class TestLessThan(RichComparisonTests):

    method = "__lt__"
    cls = common.LtNeLeComparisons
    reflected_method = "__gt__"
    reflected_cls = common.GtEqGeComparisons
    generally = None


@pytest.mark.parametrize("op", [operator.ge, desugar.operator.__ge__])
class TestGreaterThanEqual(RichComparisonTests):

    method = "__ge__"
    cls = common.GtEqGeComparisons
    reflected_method = "__le__"
    reflected_cls = common.LtNeLeComparisons
    generally = None


@pytest.mark.parametrize("op", [operator.le, desugar.operator.__le__])
class TestLessThan(RichComparisonTests):

    method = "__le__"
    cls = common.LtNeLeComparisons
    reflected_method = "__ge__"
    reflected_cls = common.GtEqGeComparisons
    generally = None


@pytest.mark.parametrize("op", [operator.eq, desugar.operator.__eq__])
class TestEquals(RichComparisonTests):

    method = "__eq__"
    cls = common.GtEqGeComparisons
    reflected_method = "__eq__"
    reflected_cls = common.GtEqGeComparisons
    generally = False


@pytest.mark.parametrize("op", [operator.ne, desugar.operator.__ne__])
class TestNotEquals(RichComparisonTests):

    method = "__ne__"
    cls = common.LtNeLeComparisons
    reflected_method = "__ne__"
    reflected_cls = common.LtNeLeComparisons
    generally = True
