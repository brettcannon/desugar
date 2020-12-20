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
