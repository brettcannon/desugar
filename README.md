# desugar
Unravelling Python source code.


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

## Syntax to (potentially) unravel

### Keywords
Taken from the [`keyword` module](https://github.com/python/cpython/blob/v3.8.3/Lib/keyword.py).

1. `False`
1. `True`
1. `None`

1. `and`
1. `or`

1. `assert`
1. `await`

1. `break`
1. `continue`
1. `pass`

1. `class`
1. `def`
1. `async`
1. `lambda`

1. `if`
1. `elif`
1. `else`
1. `for`
1. `while`
1. `with`

1. `try`
1. `except`
1. `finally`

1. `global`
1. `nonlocal`

1. `import`
1. `from`
1. `as`

1. `del`
1. `in`
1. `is`
1. `not`

1. `raise`
1. `return`
1. `yield`

### Tokens
Taken from the [`token` module](https://github.com/python/cpython/blob/v3.8.3/Lib/token.py).

1. `=`
1. `:=`

1. `[]`
1. `{}`

1. `()`
1. `,`
1. `:`
1. `;`

1. `->`

1. `...`

### [Literals](https://docs.python.org/3.8/reference/lexical_analysis.html#literals)

The list below ignores literals which are represented via syntax above.
For instance, lists are ignored as they are represented by `[]` tokens.

1. Bytes (`b`, `r`)
1. Strings (`u`, `f`, `r`; single line, multi-line)
1. Integers (base-10, `b`, `o`, `x`)
1. Floats (point, `e`)
1. Complex/imaginary numbers
