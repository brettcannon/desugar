import textwrap

import pytest
import redbaron

from desugar import syntax


class TestBinaryArithmetic:
    def _test_binary_op(self, op, method, unravel):
        given = f"a {op} b"
        expect = f"operator.{method}(a, b)"
        result = unravel(redbaron.RedBaron(given)[0])
        assert result.dumps() == expect

    def test_add(self):
        self._test_binary_op("+", "__add__", syntax.unravel_add)

    def test_sub(self):
        self._test_binary_op("-", "__sub__", syntax.unravel_sub)

    def test_mul(self):
        self._test_binary_op("*", "__mul__", syntax.unravel_mul)

    def test_matmul(self):
        self._test_binary_op("@", "__matmul__", syntax.unravel_matmul)

    def test_truediv(self):
        self._test_binary_op("/", "__truediv__", syntax.unravel_truediv)

    def test_floordiv(self):
        self._test_binary_op("//", "__floordiv__", syntax.unravel_floordiv)

    def test_mod(self):
        self._test_binary_op("%", "__mod__", syntax.unravel_mod)

    def test_pow(self):
        self._test_binary_op("**", "__pow__", syntax.unravel_pow)

    def test_lshift(self):
        self._test_binary_op("<<", "__lshift__", syntax.unravel_lshift)

    def test_rshift(self):
        self._test_binary_op(">>", "__rshift__", syntax.unravel_rshift)

    def test_and(self):
        self._test_binary_op("&", "__and__", syntax.unravel_and)

    def test_xor(self):
        self._test_binary_op("^", "__xor__", syntax.unravel_xor)

    def test_or(self):
        self._test_binary_op("|", "__or__", syntax.unravel_or)


class TestAugmentedAssignment:
    def _test_aug_assign(self, op, method, unravel):
        given = f"a {op}= b"
        expect = f"a = operator.{method}(a, b)"
        result = unravel(redbaron.RedBaron(given)[0])
        assert result.dumps() == expect

    def test_iadd(self):
        self._test_aug_assign("+", "__iadd__", syntax.unravel_iadd)

    def test_isub(self):
        self._test_aug_assign("-", "__isub__", syntax.unravel_isub)

    def test_imul(self):
        self._test_aug_assign("*", "__imul__", syntax.unravel_imul)

    def test_imatmul(self):
        self._test_aug_assign("@", "__imatmul__", syntax.unravel_imatmul)

    def test_itruediv(self):
        self._test_aug_assign("/", "__itruediv__", syntax.unravel_itruediv)

    def test_ifloordiv(self):
        self._test_aug_assign("//", "__ifloordiv__", syntax.unravel_ifloordiv)

    def test_imod(self):
        self._test_aug_assign("%", "__imod__", syntax.unravel_imod)

    def test_ipow(self):
        self._test_aug_assign("**", "__ipow__", syntax.unravel_ipow)

    def test_ilshift(self):
        self._test_aug_assign("<<", "__ilshift__", syntax.unravel_ilshift)

    def test_irshift(self):
        self._test_aug_assign(">>", "__irshift__", syntax.unravel_irshift)

    def test_iand(self):
        self._test_aug_assign("&", "__iand__", syntax.unravel_iand)

    def test_ixor(self):
        self._test_aug_assign("^", "__ixor__", syntax.unravel_ixor)

    def test_ior(self):
        self._test_aug_assign("|", "__ior__", syntax.unravel_ior)


class TestUnaryOp:
    def _test_unary_op(self, op, method, unravel):
        given = f"{op} a"
        expect = f"operator.{method}(a)"
        result = unravel(redbaron.RedBaron(given)[0])
        assert result.dumps() == expect

    def test_invert(self):
        self._test_unary_op("~", "__invert__", syntax.unravel_invert)

    def test_neg(self):
        self._test_unary_op("-", "__neg__", syntax.unravel_neg)

    def test_pos(self):
        self._test_unary_op("+", "__pos__", syntax.unravel_pos)

    def test_not(self):
        self._test_unary_op("not", "not_", syntax.unravel_not)


class TestComparison:
    def _test_comparison(self, op, method, unravel):
        given = f"a {op} b"
        expect = f"operator.{method}(a, b)"
        result = unravel(redbaron.RedBaron(given)[0])
        assert result.dumps() == expect

    def test_eq(self):
        self._test_comparison("==", "__eq__", syntax.unravel_eq)

    def test_ne(self):
        self._test_comparison("!=", "__ne__", syntax.unravel_ne)

    def test_lt(self):
        self._test_comparison("<", "__lt__", syntax.unravel_lt)

    def test_le(self):
        self._test_comparison("<=", "__le__", syntax.unravel_le)

    def test_gt(self):
        self._test_comparison(">", "__gt__", syntax.unravel_gt)

    def test_ge(self):
        self._test_comparison(">=", "__ge__", syntax.unravel_ge)

    def test_is(self):
        self._test_comparison("is", "is_", syntax.unravel_is)

    def test_is_not(self):
        self._test_comparison("is not", "is_not", syntax.unravel_is_not)


class TestContainment:
    def test_in(self):
        given = "a in b"
        expect = "operator.__contains__(b, a)"
        result = syntax.unravel_in(redbaron.RedBaron(given)[0])
        assert result.dumps() == expect

    def test_not_int(self):
        given = "a not in b"
        expect = "operator.not_(operator.__contains__(b, a))"
        result = syntax.unravel_not_in(redbaron.RedBaron(given)[0])
        assert result.dumps() == expect


class TestBooleanExpressions:
    def test_or(self):
        given = "a or b"
        expect = "_temp if (_temp := a) else b"
        with pytest.raises(NotImplementedError):
            result = syntax.unravel_boolean_or(
                redbaron.RedBaron(given)[0], temp_var="_temp"
            )
            assert result.dumps() == expect

    def test_and(self):
        given = "a and b"
        expect = "_temp if not (_temp := a) else b"
        with pytest.raises(NotImplementedError):
            result = syntax.unravel_boolean_and(
                redbaron.RedBaron(given)[0], temp_var="_temp"
            )
            assert result.dumps() == expect


class TestImport:
    def _test_import(self, given, expect):
        result = syntax.unravel_import(redbaron.RedBaron(given)[0])

        assert [stmt.dumps() for stmt in result] == expect

    def test_top_level(self):
        given = "import a"
        expect = ["a = __import__('a', globals(), locals())"]
        self._test_import(given, expect)

    def test_submodule(self):
        given = "import a.b"
        expect = ["a = __import__('a.b', globals(), locals())"]
        self._test_import(given, expect)

    def test_top_level_as(self):
        given = "import a as b"
        expect = ["b = __import__('a', globals(), locals())"]
        self._test_import(given, expect)

    def test_submodule_as(self):
        given = "import a.b.c as d"
        expect = ["d = __import__('a.b', globals(), locals(), ['c']).c"]
        self._test_import(given, expect)

    def test_from_single(self):
        given = "from a import b"
        expect = ["b = __import__('a', globals(), locals(), ['b'], 0).b"]
        self._test_import(given, expect)

    def test_from_deep(self):
        given = "from a.b import c"
        expect = ["c = __import__('a.b', globals(), locals(), ['c'], 0).c"]
        self._test_import(given, expect)

    def test_from_multiple(self):
        given = "from a import b, c"
        expect = [
            "b = __import__('a', globals(), locals(), ['b'], 0).b",
            "c = __import__('a', globals(), locals(), ['c'], 0).c",
        ]
        self._test_import(given, expect)

    def test_from_dot(self):
        given = "from .a import b"
        expect = ["b = __import__('a', globals(), locals(), ['b'], 1).b"]
        self._test_import(given, expect)

    def test_from_single_as(self):
        given = "from a import b as c"
        expect = ["c = __import__('a', globals(), locals(), ['b'], 0).b"]
        self._test_import(given, expect)


class TestAssert:
    def test_no_message(self):
        given = "assert a"
        expect = textwrap.dedent(
            """
            if __debug__:
                if a:
                    raise AssertionError
            """
        ).strip()
        print(expect)
        result = syntax.unravel_assert(redbaron.RedBaron(given)[0])
        assert result.dumps().strip() == expect

    def test_str_message(self):
        given = 'assert a, "oh no!"'
        expect = textwrap.dedent(
            """
            if __debug__:
                if a:
                    raise AssertionError("oh no!")
            """
        ).strip()
        print(expect)
        result = syntax.unravel_assert(redbaron.RedBaron(given)[0])
        assert result.dumps().strip() == expect

    def test_var_message(self):
        given = "assert a, b"
        expect = textwrap.dedent(
            """
            if __debug__:
                if a:
                    raise AssertionError(b)
            """
        ).strip()
        print(expect)
        result = syntax.unravel_assert(redbaron.RedBaron(given)[0])
        assert result.dumps().strip() == expect
