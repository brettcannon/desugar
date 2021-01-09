from __future__ import annotations

import textwrap
from typing import Callable, Union

import redbaron
from redbaron import nodes


def _wrap(op: str, method: str, doc: str):
    """Decorator to update an unravelling closure's details."""

    if method.startswith("__") and method.endswith("__"):
        method_name = method[2:-2]
    else:
        method_name = method

    def wrapper(func):
        func.__name__ = func.__qualname__ = f"unravel_{method_name}"
        func.__doc__ = doc.format(op=op, method=method_name)
        return func

    return wrapper


def _create_binary_op(
    op: str, method: str
) -> Callable[[nodes.BinaryOperatorNode], nodes.AtomtrailersNode]:
    @_wrap(op, method, "Convert `a {op} b` to `operator.{method}(a, b)`.")
    def unravel(node: nodes.BinaryOperatorNode) -> nodes.AtomtrailersNode:
        """Convert `a {op} b` to `operator.{method}(a, b)`."""
        left = node.first.dumps()
        right = node.second.dumps()
        top_node = redbaron.RedBaron(f"operator.{method}({left}, {right})")
        return top_node[0]

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
    @_wrap(op, method, "Convert `a {op}= b` to `a = operator.{method}(a, b)`.")
    def unravel(node: nodes.AssignmentNode) -> nodes.AssignmentNode:
        new_node = node.copy()
        new_node.operator = ""
        left = node.target.dumps()
        right = node.value.dumps()
        rhs = redbaron.RedBaron(f"operator.{method}({left}, {right})")[0]
        new_node.value = rhs
        return new_node

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
    @_wrap(op, method, "Convert `{op} a` to `operator.{method}(a)`.")
    def unravel(node: nodes.UnitaryOperatorNode) -> nodes.AtomtrailersNode:
        target = node.target.dumps()
        return redbaron.RedBaron(f"operator.{method}({target})")[0]

    return unravel


unravel_invert = _create_unary_op("~", "__invert__")
unravel_neg = _create_unary_op("-", "__neg__")
unravel_pos = _create_unary_op("+", "__pos__")
unravel_not = _create_unary_op("not", "not_")


def _create_compare_op(
    op: str, method: str
) -> Callable[[nodes.ComparisonNode], nodes.AtomtrailersNode]:
    @_wrap(op, method, "Convert `a {op} b` to `operator.{method}(a, b)`.")
    def unravel(node: nodes.ComparisonNode) -> nodes.AtomtrailersNode:
        lhs = node.first.dumps()
        rhs = node.second.dumps()
        return redbaron.RedBaron(f"operator.{method}({lhs}, {rhs})")[0]

    return unravel


unravel_eq = _create_compare_op("==", "__eq__")
unravel_ne = _create_compare_op("!=", "__ne__")
unravel_lt = _create_compare_op("<", "__lt__")
unravel_le = _create_compare_op("<=", "__le__")
unravel_gt = _create_compare_op(">", "__gt__")
unravel_ge = _create_compare_op(">=", "__ge__")
unravel_is = _create_compare_op("is", "is_")
unravel_is_not = _create_compare_op("is not", "is_not")


def unravel_in(node: nodes.ComparisonNode) -> nodes.AtomtrailersNode:
    """Convert `a in b` to `operator.__contains__(b, a)`."""
    lhs = node.first.dumps()
    rhs = node.second.dumps()
    return redbaron.RedBaron(f"operator.__contains__({rhs}, {lhs})")[0]


def unravel_not_in(node: nodes.ComparisonNode) -> nodes.AtomtrailersNode:
    """Convert `a not in b` to `operator.not_(operator.__contains__(b, a))."""
    contains = unravel_in(node)
    return redbaron.RedBaron(f"operator.not_({contains})")[0]


def unravel_boolean_or(node: nodes.BooleanOperatorNode, temp_var: str):
    """Convert `a or b` to `temp_var if (temp_var := a) else b`."""
    raise NotImplementedError("RedBaron does not support assignment expressions")


def unravel_boolean_and(node: nodes.BooleanOperatorNode, *, temp_var: str):
    """Convert `a and b` to `temp_var if not (temp_var := a) else b`."""
    raise NotImplementedError("RedBaron does not support assignment expressions")


def unravel_import(
    node: Union[nodes.ImportNode, nodes.FromImportNode]
) -> list[nodes.Node]:
    """Convert the various forms of an import statement to calls of `__import__()`."""
    if isinstance(node, nodes.ImportNode):
        if (target := node.value[0].target) :
            # `import a.b.c as d`
            parent, _, child = node.value[0].value.dumps().rpartition(".")
            if not parent:
                stmt = f"{target} = __import__({child!r}, globals(), locals())"
            else:
                stmt = f"{target} = __import__({parent!r}, globals(), locals(), [{child!r}]).{child}"
        else:
            # `import a.b`
            parent = node.value[0][0].dumps()
            full_name = node.value.dumps()
            stmt = f"{parent} = __import__({full_name!r}, globals(), locals())"
        return [redbaron.RedBaron(stmt)[0]]
    else:
        parent = node.value.dumps()
        index = 0
        for char in parent:
            if char == ".":
                index += 1
            else:
                break
        stmts = []
        for from_ in node.targets:
            if not (target := from_.target):
                target = from_.value
            child = from_.value
            stmts.append(
                f"{target} = __import__({parent[index:]!r}, globals(), locals(), [{child!r}], {index}).{child}"
            )
        return [redbaron.RedBaron(stmt)[0] for stmt in stmts]


def unravel_assert(node: nodes.AsAssertNode) -> nodes.IfelseblockNode:
    """Convert `assert a, b` to:

    ```
    if __debug__:
        if a:
            raise AssertionError(b)
    ```
    """
    assertion = node.value.dumps()
    if message := node.message:
        stmt = f"""
            if __debug__:
                if {assertion}:
                    raise AssertionError({message.dumps()})
        """
    else:
        stmt = f"""
            if __debug__:
                if {assertion}:
                    raise AssertionError
        """
    return redbaron.RedBaron(textwrap.dedent(stmt).strip())[0]


# >>> redbaron.RedBaron("assert a")[0].help()
# AssertNode()
#   # identifiers: assert, assert_, assertnode
#   value ->
#     NameNode()
#       # identifiers: name, name_, namenode
#       value='a'
#   message ->
#     None
# >>> redbaron.RedBaron("assert a, b")[0].help()
# AssertNode()
#   # identifiers: assert, assert_, assertnode
#   value ->
#     NameNode()
#       # identifiers: name, name_, namenode
#       value='a'
#   message ->
#     NameNode()
#       # identifiers: name, name_, namenode
#       value='b'
