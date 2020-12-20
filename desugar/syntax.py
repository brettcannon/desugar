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
        rhs = redbaron.RedBaron(f"operator.{method}({left}, {right})")[0]
        new_node.value = rhs
        return new_node

    unravel.__name__ = unravel.__qualname__ = f"unravel_{method[2:-2]}"
    unravel.__doc__ = f"Convert `a {op}= b` to `a = operator.{method}(a, b)`."
    return unravel


unravel_iadd = _create_aug_assign("+", "__iadd__")
unravel_isub = _create_aug_assign("-", "__isub__")
unravel_imul = _create_aug_assign("*", "__imul__")
unravel_imatmul = _create_aug_assign("@", "__imatmul__")
unravel_itruediv = _create_aug_assign("/", "__itruediv__")
unravel_ifloordiv = _create_aug_assign("//", "__ifloordiv__")
unravel_imod = _create_aug_assign("%", "__imod__")
unravel_ipow = _create_aug_assign("**", "__ipow__")
unravel_ilshift = _create_aug_assign("<<", "__ilshift__")
unravel_irshift = _create_aug_assign(">>", "__irshift__")
unravel_iand = _create_aug_assign("&", "__iand__")
unravel_ixor = _create_aug_assign("^", "__ixor__")
unravel_ior = _create_aug_assign("|", "__ior__")


def _create_unary_op(
    op: str, method: str
) -> Callable[[nodes.UnitaryOperatorNode], nodes.AtomtrailersNode]:
    def unravel(node: nodes.UnitaryOperatorNode) -> nodes.AtomtrailersNode:
        target = node.target.dumps()
        return redbaron.RedBaron(f"operator.{method}({target})")[0]

    unravel.__name__ = unravel.__qualname__ = f"unravel_{method[2:-2]}"
    unravel.__doc__ = f"Convert `{op} a` to `operator.{method}(a)`."
    return unravel


unravel_invert = _create_unary_op("~", "__invert__")
unravel_neg = _create_unary_op("-", "__neg__")
unravel_pos = _create_unary_op("+", "__pos__")

# 1. `a == b` ➠ `operator.__eq__(a, b)`  (including `object.__eq__()`)
# 1. `a != b` ➠ `operator.__ne__(a, b)`  (including `object.__ne__()`)
# 1. `a < b` ➠ `operator.__lt__(a, b)`
# 1. `a <= b` ➠ `operator.__le__(a, b)`
# 1. `a > b` ➠ `operator.__gt__(a, b)`
# 1. `a >= b` ➠ `operator.__ge__(a, b)`
# >>> given = redbaron.RedBaron("a < b"); given[0].help()
# ComparisonNode()
#   # identifiers: comparison, comparison_, comparisonnode
#   first ->
#     NameNode()
#       # identifiers: name, name_, namenode
#       value='a'
#   value ->
#     ComparisonOperatorNode()
#       # identifiers: comparison_operator, comparison_operator_, comparisonoperator, comparisonoperatornode
#       first='<'
#       second=''
#   second ->
#     NameNode()
#       # identifiers: name, name_, namenode
#       value='b'

# 1. `a is b` ➠ `operator.is_(a, b)`
# 1. `a is not b` ➠ `operator.is_not(a, b)`
# >>> given = redbaron.RedBaron("a is not b"); given[0].help()
# ComparisonNode()
#   # identifiers: comparison, comparison_, comparisonnode
#   first ->
#     NameNode()
#       # identifiers: name, name_, namenode
#       value='a'
#   value ->
#     ComparisonOperatorNode()
#       # identifiers: comparison_operator, comparison_operator_, comparisonoperator, comparisonoperatornode
#       first='is'
#       second='not'
#   second ->
#     NameNode()
#       # identifiers: name, name_, namenode
#       value='b'

# 1. `not a` ➠ `operator.not_(a)`
# >>> given = redbaron.RedBaron("not a"); given[0].help()
# UnitaryOperatorNode()
#   # identifiers: unitary_operator, unitary_operator_, unitaryoperator, unitaryoperatornode
#   value='not'
#   target ->
#     NameNode()
#       # identifiers: name, name_, namenode
#       value='a'

# 1. `a in b` ➠ `operator.__contains__(b, a)`
# 1. `a not in b` ➠ `operator.not_(operator.__contains__(b, a))`
# >>> given = redbaron.RedBaron("a not in b"); given[0].help()
# ComparisonNode()
#   # identifiers: comparison, comparison_, comparisonnode
#   first ->
#     NameNode()
#       # identifiers: name, name_, namenode
#       value='a'
#   value ->
#     ComparisonOperatorNode()
#       # identifiers: comparison_operator, comparison_operator_, comparisonoperator, comparisonoperatornode
#       first='not'
#       second='in'
#   second ->
#     NameNode()
#       # identifiers: name, name_, namenode
#       value='b'
