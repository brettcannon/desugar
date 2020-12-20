# desugar
Unravelling Python's syntactic sugar source code.

There are [accompanying blog posts](https://snarky.ca/tag/syntactic-sugar/) to
go with all of the code in this repository.

## Unravelled syntax

1. `obj.attr` ➠ `builtins.getattr(obj, "attr")` (including `object.__getattribute__()`)
1. `a + b` ➠ `operator.__add__(a, b)`
1. `a - b` ➠ `operator.__sub__(a, b)`
1. `a * b` ➠ `operator.__mul__(a, b)`
1. `a @ b` ➠ `operator.__matmul__(a, b)`
1. `a / b` ➠ `operator.__truediv__(a, b)`
1. `a // b` ➠ `operator.__floordiv__(a, b)`
1. `a % b` ➠ `operator.__mod__(a, b)`
1. `a ** b` ➠ `operator.__pow__(a, b)`
1. `a << b` ➠ `operator.__lshift__(a, b)`
1. `a >> b` ➠ `operator.__rshift__(a, b)`
1. `a & b` ➠ `operator.__and__(a, b)`
1. `a ^ b` ➠ `operator.__xor__(a, b)`
1. `a | b` ➠ `operator.__or__(a, b)`
1. `a += b` ➠ `a = operator.__iadd__(a, b)`
1. `a -= b` ➠ `a = operator.__isub__(a, b)`
1. `a *= b` ➠ `a = operator.__imul__(a, b)`
1. `a @= b` ➠ `a = operator.__imatmul__(a, b)`
1. `a /= b` ➠ `a = operator.__itruediv__(a, b)`
1. `a //= b` ➠ `a = operator.__ifloordiv__(a, b)`
1. `a %= b` ➠ `a = operator.__imod__(a, b)`
1. `a **= b` ➠ `a = operator.__ipow__(a, b)`
1. `a <<= b` ➠ `a = operator.__ilshift__(a, b)`
1. `a >>= b` ➠ `a = operator.__irshift__(a, b)`
1. `a &= b` ➠ `a = operator.__iand__(a, b)`
1. `a ^= b` ➠ `a = operator.__ixor__(a, b)`
1. `a |= b` ➠ `a = operator.__ior__(a, b)`
1. `~ a` ➠ `operator.__invert__(a)`
1. `- a` ➠ `operator.__neg__(a)`
1. `+ a` ➠ `operator.__pos__(a)`
1. `a == b` ➠ `operator.__eq__(a, b)`  (including `object.__eq__()`)
1. `a != b` ➠ `operator.__ne__(a, b)`  (including `object.__ne__()`)
1. `a < b` ➠ `operator.__lt__(a, b)`
1. `a <= b` ➠ `operator.__le__(a, b)`
1. `a > b` ➠ `operator.__gt__(a, b)`
1. `a >= b` ➠ `operator.__ge__(a, b)`
1. `a is b` ➠ `operator.is_(a, b)`
1. `a is not b` ➠ `operator.is_not(a, b)`
1. `not a` ➠ `operator.not_(a)`
1. `a in b` ➠ `operator.__contains__(b, a)`
1. `a not in b` ➠ `operator.not_(operator.__contains__(b, a))`

## Syntax to (potentially) unravel

### Keywords
Taken from the [`keyword` module](https://github.com/python/cpython/blob/v3.8.3/Lib/keyword.py).

#### Expressions
1. [`and`](https://docs.python.org/3/reference/expressions.html#boolean-operations) *
1. [`or`](https://docs.python.org/3/reference/expressions.html#boolean-operations) *

1. [`yield`](https://docs.python.org/3.8/reference/simple_stmts.html#the-yield-statement)
1. [`await`](https://docs.python.org/3.8/reference/expressions.html#await) ~

1. [`lambda`](https://docs.python.org/3.8/reference/expressions.html#lambda)

#### Statements
1. [`assert`](https://docs.python.org/3.8/reference/simple_stmts.html#the-assert-statement) *

1. [`import`/`from`/`as`](https://docs.python.org/3.8/reference/simple_stmts.html#the-import-statement) *

1. [`pass`](https://docs.python.org/3.8/reference/simple_stmts.html#the-pass-statement) *
1. [`break`](https://docs.python.org/3.8/reference/simple_stmts.html#the-break-statement)
1. [`continue`](https://docs.python.org/3.8/reference/simple_stmts.html#the-continue-statement)

1. [`if`/`elif`/`else`](https://docs.python.org/3.8/reference/compound_stmts.html#the-if-statement)
1. [`while`/`else`](https://docs.python.org/3.8/reference/compound_stmts.html#the-while-statement)
1. [`for`/`else`](https://docs.python.org/3.8/reference/compound_stmts.html#the-for-statement) *
1. [`async for`/`else`](https://docs.python.org/3.8/reference/compound_stmts.html#async-for) *

1. [`with`](https://docs.python.org/3.8/reference/compound_stmts.html#the-with-statement) *
1. [`async with`](https://docs.python.org/3.8/reference/compound_stmts.html#async-with) *

1. [`def`](https://docs.python.org/3.8/reference/compound_stmts.html#function-definitions)
1. [`async def`](https://docs.python.org/3.8/reference/compound_stmts.html#coroutine-function-definition) ~
1. [`class`](https://docs.python.org/3.8/reference/compound_stmts.html#class-definitions) ~

1. [`try`/`except`/`else`/`finally`](https://docs.python.org/3.8/reference/compound_stmts.html#the-try-statement)

1. [`global`](https://docs.python.org/3.8/reference/simple_stmts.html#the-global-statement)
1. [`nonlocal`](https://docs.python.org/3.8/reference/simple_stmts.html#the-nonlocal-statement)

1. [`del`](https://docs.python.org/3.8/reference/simple_stmts.html#the-del-statement)

1. [`raise`/`from`](https://docs.python.org/3.8/reference/simple_stmts.html#the-raise-statement)
1. [`return`](https://docs.python.org/3.8/reference/simple_stmts.html#the-return-statement)

### Tokens
Taken from the [`token` module](https://github.com/python/cpython/blob/v3.8.3/Lib/token.py).

1. [`=`](https://docs.python.org/3.8/reference/simple_stmts.html#assignment-statements)
1. [`:=`](https://docs.python.org/3.8/reference/expressions.html#assignment-expressions)

1. `[]` for [list display](https://docs.python.org/3.8/reference/expressions.html#list-displays) *
1. `[]` for list [comprehensions](https://docs.python.org/3.8/reference/expressions.html#displays-for-lists-sets-and-dictionaries) *
1. `[]` for [subscriptions](https://docs.python.org/3.8/reference/expressions.html#subscriptions) (get, set, del), `:` for [slicing](https://docs.python.org/3.8/reference/expressions.html#slicings) *

1. `{}` for [set display](https://docs.python.org/3.8/reference/expressions.html#set-displays) *
1. `{}` for set [comprehensions](https://docs.python.org/3.8/reference/expressions.html#displays-for-lists-sets-and-dictionaries) *

1. `{}` for [dictionary display](https://docs.python.org/3.8/reference/expressions.html#dictionary-displays) *
1. `{}` for dictionary [comprehensions](https://docs.python.org/3.8/reference/expressions.html#displays-for-lists-sets-and-dictionaries) *

1. `()` for [tuple display](https://docs.python.org/3.8/reference/expressions.html#parenthesized-forms)

1. `()` for [calls](https://docs.python.org/3.8/reference/expressions.html#calls)

1. `@` for [decorators](https://docs.python.org/3.8/reference/compound_stmts.html#function-definitions) *

1. `,`
1. `;` *

1. `...` *

### [Literals](https://docs.python.org/3.8/reference/lexical_analysis.html#literals)

The list below ignores literals which are represented via syntax above.
For instance, lists are ignored as they are represented by `[]` tokens.

1. `None`
1. `False`
1. `True`
1. Bytes (`b`, `r`)
1. Strings (`u`, `f`, `r`; single line, multi-line)
1. Integers (base-10, `b`, `o`, `x`)
1. Floats (point, `e`)
1. Complex/imaginary numbers
