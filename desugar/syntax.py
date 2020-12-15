import redbaron
from redbaron import nodes


def _create_binary_op_unraveling(op, method):
    def unravel(node: nodes.BinaryOperatorNode) -> nodes.AtomtrailersNode:
        """Convert `a + b` to `operator.__add__(a, b)`."""
        left = node.first.dumps()
        right = node.second.dumps()
        top_node = redbaron.RedBaron(f"operator.{method}({left}, {right})")
        return top_node[0]

    unravel.__name__ = unravel.__qualname__ = f"unravel_{method[2:-2]}"
    unravel.__doc__ = f"Convert `a {op} b` to `operator.{method}(a, b)`."
    return unravel


unravel_add = _create_binary_op_unraveling("+", "__add__")
unravel_sub = _create_binary_op_unraveling("-", "__sub__")
unravel_mul = _create_binary_op_unraveling("*", "__mul__")
unravel_matmul = _create_binary_op_unraveling("@", "__matmul__")
unravel_truediv = _create_binary_op_unraveling("/", "__truediv__")
unravel_floordiv = _create_binary_op_unraveling("//", "__floordiv__")
unravel_mod = _create_binary_op_unraveling("%", "__mod__")
unravel_pow = _create_binary_op_unraveling("**", "__pow__")
unravel_lshift = _create_binary_op_unraveling("<<", "__lshift__")
unravel_rshift = _create_binary_op_unraveling(">>", "__rshift__")
unravel_and = _create_binary_op_unraveling("&", "__and__")
unravel_xor = _create_binary_op_unraveling("^", "__xor__")
unravel_or = _create_binary_op_unraveling("|", "__or__")
