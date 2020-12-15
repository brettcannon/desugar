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
