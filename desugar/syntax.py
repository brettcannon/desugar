from typing import Callable

import redbaron
from redbaron import nodes


def _create_binary_op(
    op: str, method: str
) -> Callable[[nodes.BinaryOperatorNode], nodes.AtomtrailersNode]:
    def unravel(node: nodes.BinaryOperatorNode) -> nodes.AtomtrailersNode:
        """Convert `a {op} b` to `operator.{method}(a, b)`."""
        left = node.first.dumps()
        right = node.second.dumps()
        top_node = redbaron.RedBaron(f"operator.{method}({left}, {right})")
        return top_node[0]

    unravel.__name__ = unravel.__qualname__ = f"unravel_{method[2:-2]}"
    unravel.__doc__ = f"Convert `a {op} b` to `operator.{method}(a, b)`."
    return unravel


unravel_add = _create_binary_op("+", "__add__")
unravel_sub = _create_binary_op("-", "__sub__")
unravel_mul = _create_binary_op("*", "__mul__")
unravel_matmul = _create_binary_op("@", "__matmul__")
unravel_truediv = _create_binary_op("/", "__truediv__")
unravel_floordiv = _create_binary_op("//", "__floordiv__")
unravel_mod = _create_binary_op("%", "__mod__")
unravel_pow = _create_binary_op("**", "__pow__")
unravel_lshift = _create_binary_op("<<", "__lshift__")
unravel_rshift = _create_binary_op(">>", "__rshift__")
unravel_and = _create_binary_op("&", "__and__")
unravel_xor = _create_binary_op("^", "__xor__")
unravel_or = _create_binary_op("|", "__or__")


def _create_aug_assign(
    op: str, method: str
) -> Callable[[nodes.AssignmentNode], nodes.AssignmentNode]:
    def unravel(node: nodes.AssignmentNode) -> nodes.AssignmentNode:
        """Convert `a {op}= b` to `a = operator.{method}(a, b)`."""
        new_node = node.copy()
        new_node.operator = ""
        left = node.target.dumps()
        right = node.value.dumps()
        lhs = redbaron.RedBaron(f"operator.{method}({left}, {right})")[0]
        new_node.value = lhs
        return new_node

    unravel.__name__ = unravel.__qualname__ = f"unravel_{method[2:-2]}"
    unravel.__doc__ = f"Convert `a {op}= b` to `a = operator.{method}(a, b)`."
    return unravel


unravel_inplace_add = _create_aug_assign("+", "__iadd__")
unravel_inplace_sub = _create_aug_assign("-", "__isub__")
unravel_inplace_mul = _create_aug_assign("*", "__imul__")
unravel_inplace_matmul = _create_aug_assign("@", "__imatmul__")
unravel_inplace_truediv = _create_aug_assign("/", "__itruediv__")
unravel_inplace_floordiv = _create_aug_assign("//", "__ifloordiv__")
unravel_inplace_mod = _create_aug_assign("%", "__imod__")
unravel_inplace_pow = _create_aug_assign("**", "__ipow__")
unravel_inplace_lshift = _create_aug_assign("<<", "__ilshift__")
unravel_inplace_rshift = _create_aug_assign(">>", "__irshift__")
unravel_inplace_and = _create_aug_assign("&", "__iand__")
unravel_inplace_xor = _create_aug_assign("^", "__ixor__")
unravel_inplace_or = _create_aug_assign("|", "__ior__")

# 1. `~ a` ➠ `operator.__invert__(a)`
# 1. `- a` ➠ `operator.__neg__(a)`
# 1. `+ a` ➠ `operator.__pos__(a)`
# 1. `a == b` ➠ `operator.__eq__(a, b)`  (including `object.__eq__()`)
# 1. `a != b` ➠ `operator.__ne__(a, b)`  (including `object.__ne__()`)
# 1. `a < b` ➠ `operator.__lt__(a, b)`
# 1. `a <= b` ➠ `operator.__le__(a, b)`
# 1. `a > b` ➠ `operator.__gt__(a, b)`
# 1. `a >= b` ➠ `operator.__ge__(a, b)`
# 1. `a is b` ➠ `operator.is_(a, b)`
# 1. `a is not b` ➠ `operator.is_not(a, b)`
# 1. `not a` ➠ `operator.not_(a)`
# 1. `a in b` ➠ `operator.__contains__(b, a)`
# 1. `a not in b` ➠ `operator.not_(operator.__contains__(b, a))`
