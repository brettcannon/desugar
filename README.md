# desugar

Unravelling Python's syntactic sugar source code.

There are [accompanying blog posts](https://snarky.ca/tag/syntactic-sugar/) to
go with all of the code in this repository.

## Unravelled syntax

1. [`obj.attr`](https://snarky.ca/unravelling-attribute-access-in-python/) ➠ [`builtins.getattr(obj, "attr")`](https://docs.python.org/3.8/reference/expressions.html#attribute-references) (including `object.__getattribute__()`)
1. [`a + b`](https://docs.python.org/3.8/reference/expressions.html#binary-arithmetic-operations) ➠ [`operator.__add__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a - b`](https://docs.python.org/3.8/reference/expressions.html#binary-arithmetic-operations) ➠ [`operator.__sub__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a * b`](https://docs.python.org/3.8/reference/expressions.html#binary-arithmetic-operations) ➠ [`operator.__mul__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a @ b`](https://docs.python.org/3.8/reference/expressions.html#binary-arithmetic-operations) ➠ [`operator.__matmul__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a / b`](https://docs.python.org/3.8/reference/expressions.html#binary-arithmetic-operations) ➠ [`operator.__truediv__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a // b`](https://docs.python.org/3.8/reference/expressions.html#binary-arithmetic-operations) ➠ `operator.__floordiv__(a, b)`
1. [`a % b`](https://docs.python.org/3.8/reference/expressions.html#binary-arithmetic-operations) ➠ [`operator.__mod__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a ** b`](https://docs.python.org/3.8/reference/expressions.html#binary-arithmetic-operations) ➠ [`operator.__pow__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a << b`](https://docs.python.org/3.8/reference/expressions.html#shifting-operations) ➠ [`operator.__lshift__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a >> b`](https://docs.python.org/3.8/reference/expressions.html#shifting-operations) ➠ [`operator.__rshift__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a & b`](https://docs.python.org/3.8/reference/expressions.html#binary-bitwise-operations) ➠ [`operator.__and__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a ^ b`](https://docs.python.org/3.8/reference/expressions.html#binary-bitwise-operations) ➠ `operator.__xor__(a, b)`
1. [`a | b`](https://docs.python.org/3.8/reference/expressions.html#binary-bitwise-operations) ➠ [`operator.__or__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a += b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__iadd__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a -= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__isub__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a *= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__imul__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a @= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__imatmul__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a /= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__itruediv__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a //= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__ifloordiv__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a %= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__imod__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a **= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__ipow__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a <<= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__ilshift__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a >>= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__irshift__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a &= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__iand__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a ^= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__ixor__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`a |= b`](https://docs.python.org/3/reference/simple_stmts.html#augmented-assignment-statements) ➠ [`a = operator.__ior__(a, b)`](https://snarky.ca/unravelling-augmented-arithmetic-assignment/)
1. [`~ a`](https://docs.python.org/3.8/reference/expressions.html#unary-arithmetic-and-bitwise-operations) ➠ [`operator.__invert__(a)`](https://snarky.ca/unravelling-unary-arithmetic-operators/)
1. [`- a`](https://docs.python.org/3.8/reference/expressions.html#unary-arithmetic-and-bitwise-operations) ➠ [`operator.__neg__(a)`](https://snarky.ca/unravelling-unary-arithmetic-operators/)
1. [`+ a`](https://docs.python.org/3.8/reference/expressions.html#unary-arithmetic-and-bitwise-operations) ➠ [`operator.__pos__(a)`](https://snarky.ca/unravelling-unary-arithmetic-operators/)
1. [`a == b`](https://docs.python.org/3.8/reference/expressions.html#value-comparisons) ➠ [`operator.__eq__(a, b)`](https://snarky.ca/unravelling-rich-comparison-operators/) (including `object.__eq__()`)
1. [`a != b`](https://docs.python.org/3.8/reference/expressions.html#value-comparisons) ➠ [`operator.__ne__(a, b)`](https://snarky.ca/unravelling-rich-comparison-operators/) (including `object.__ne__()`)
1. [`a < b`](https://docs.python.org/3.8/reference/expressions.html#value-comparisons) ➠ [`operator.__lt__(a, b)`](https://snarky.ca/unravelling-rich-comparison-operators/)
1. [`a <= b`](https://docs.python.org/3.8/reference/expressions.html#value-comparisons) ➠ [`operator.__le__(a, b)`](https://snarky.ca/unravelling-rich-comparison-operators/)
1. [`a > b`](https://docs.python.org/3.8/reference/expressions.html#value-comparisons) ➠ [`operator.__gt__(a, b)`](https://snarky.ca/unravelling-rich-comparison-operators/)
1. [`a >= b`](https://docs.python.org/3.8/reference/expressions.html#value-comparisons) ➠ [`operator.__ge__(a, b)`](https://snarky.ca/unravelling-rich-comparison-operators/)
1. [`a is b`](https://docs.python.org/3.8/reference/expressions.html#is-not) ➠ [`operator.is_(a, b)`](https://snarky.ca/unravelling-is-and-is-not/)
1. [`a is not b`](https://docs.python.org/3.8/reference/expressions.html#is-not) ➠ [`operator.is_not(a, b)`](https://snarky.ca/unravelling-is-and-is-not/)
1. [`not a`](https://docs.python.org/3.8/reference/expressions.html#boolean-operations) ➠ [`operator.not_(a)`](https://snarky.ca/unravelling-not-in-python/)
1. [`a in b`](https://docs.python.org/3.8/reference/expressions.html#membership-test-operations) ➠ [`operator.__contains__(b, a)`](https://snarky.ca/unravelling-membership-testing/)
1. [`a not in b`](https://docs.python.org/3.8/reference/expressions.html#membership-test-operations) ➠ [`operator.not_(operator.__contains__(b, a))`](https://snarky.ca/unravelling-membership-testing/)
1. [`a or b`](https://docs.python.org/3.8/reference/expressions.html#boolean-operations) ➠ [`_temp if (_temp := a) else b`](https://snarky.ca/unravelling-boolean-operations/)
1. [`a and b`](https://docs.python.org/3.8/reference/expressions.html#boolean-operations) ➠ [`_temp if not (_temp := a) else b`](https://snarky.ca/unravelling-boolean-operations/)
1. [`import a.b`](https://docs.python.org/3.8/reference/simple_stmts.html#the-import-statement) ➠ [`a = __import__('a.b', globals(), locals())`](https://snarky.ca/unravelling-the-import-statement/)
1. [`import a.b as c`](https://docs.python.org/3.8/reference/simple_stmts.html#the-import-statement) ➠ [`c = __import__('a', globals(), locals(), ['b'], 0).b`](https://snarky.ca/unravelling-the-import-statement/)
1. [`from .a import b`](https://docs.python.org/3.8/reference/simple_stmts.html#the-import-statement) ➠ [`b = __import__('a', globals(), locals(), ['b'], 1).b`](https://snarky.ca/unravelling-the-import-statement/)
1. [`from .a import b as c`](https://docs.python.org/3.8/reference/simple_stmts.html#the-import-statement) ➠ [`c = __import__('a', globals(), locals(), ['b'], 1).b`](https://snarky.ca/unravelling-the-import-statement/)
1. [`assert ...`](https://docs.python.org/3.8/reference/simple_stmts.html#the-assert-statement) ➠ see below ([post](https://snarky.ca/unravelling-assertions/))
1. [`for ...`](https://docs.python.org/3.8/reference/compound_stmts.html#the-for-statement) ➠ see below ([including `builtins.iter()` and `builtins.next()`](https://snarky.ca/unravelling-for-statements/))
1. `pass` ➠ `"pass"`
1. [`with ...`](https://docs.python.org/3.8/reference/compound_stmts.html#the-with-statement) ➠ see below ([post](https://snarky.ca/unravelling-the-with-statement/))
1. [`async def ...`](https://docs.python.org/3.8/reference/compound_stmts.html#coroutine-function-definition) ➠ see below ([post](https://snarky.ca/unravelling-async-and-await/))
1. [`await ...`](https://docs.python.org/3.8/reference/expressions.html#await-expression) ➠ [`desugar.builtins._await(...)`](https://snarky.ca/unravelling-async-and-await/)
1. [`async for`](https://docs.python.org/3.8/reference/compound_stmts.html#async-for) ➠ see below ([including `builtins.aiter()` and `builtins.anext()`](https://snarky.ca/unravelling-async-for-loops/))
1. [`async with`](https://docs.python.org/3.8/reference/compound_stmts.html#async-with) ➠ see below ([post](https://snarky.ca/unravelling-the-async-with-statement/))

### `assert ...`

#### With message

```Python
assert a, b
```

➠

```Python
if __debug__:
    if not a:
        raise AssertionError(b)
```

#### Without a message

```Python
assert a
```

➠

```Python
if __debug__:
    if not a:
        raise AssertionError
```

### `for ...`

#### Without `else`

```Python
for a in b:
    c
```

➠

```Python
_iter = iter(b)
while True:
    try:
        a = next(_iter)
    except StopIteration:
        break
    else:
        c
del _iter
```

#### With `else`

```Python
for a in b:
    c
else:
    d
```

➠

```Python
_iter = iter(b)
_looping = True
while _looping:
    try:
        a = next(_iter)
    except StopIteration:
        _looping = False
        continue
    else:
        c
else:
    d
del _iter, _looping
```

### `with ...`

```Python
with a as b:
    c
```

➠

```Python
_enter = type(a).__enter__
_exit = type(a).__exit__
b = _enter(a)

try:
    c
except:
    if not _exit(a, *sys.exc_info()):
        raise
else:
    _exit(a, None, None, None)
```

### `async def ...`
```Python
async def spam():
    ...
```

➠

```Python
@types.coroutine
def spam():
    ...
```

### `async for ...`

#### Without `else`

```Python
async for a in b:
    c
```

➠

```Python
_iter = aiter(b)
while True:
    try:
        a = await anext(_iter)
    except StopAsyncIteration:
        break
    else:
        c
del _iter
```

#### With `else`

```Python
async for a in b:
    c
else:
    d
```

➠

```Python
_iter = aiter(b)
_looping = True
while _looping:
    try:
        a = await anext(_iter)
    except StopAsyncIteration:
        _looping = False
        continue
    else:
        c
else:
    d
del _iter, _looping
```

### `async with ...`

```Python
async with a as b:
    c
```

➠

```Python
_enter = type(a).__aenter__
_exit = type(a).__aexit__
b = await _enter(a)

try:
    c
except:
    if not await _exit(a, *sys.exc_info()):
        raise
else:
    await _exit(a, None, None, None)
```

## Syntax to (potentially) unravel

### Keywords

Taken from the [`keyword` module](https://github.com/python/cpython/blob/v3.8.3/Lib/keyword.py).

#### Expressions

1. [`yield`](https://docs.python.org/3.8/reference/simple_stmts.html#the-yield-statement)
1. [`lambda`](https://docs.python.org/3.8/reference/expressions.html#lambda)

#### Statements

1. [`break`](https://docs.python.org/3.8/reference/simple_stmts.html#the-break-statement)
1. [`continue`](https://docs.python.org/3.8/reference/simple_stmts.html#the-continue-statement)

1. [`if`/`elif`/`else`](https://docs.python.org/3.8/reference/compound_stmts.html#the-if-statement)
1. [`while`/`else`](https://docs.python.org/3.8/reference/compound_stmts.html#the-while-statement)

1. [`def`](https://docs.python.org/3.8/reference/compound_stmts.html#function-definitions)

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

1. `[]` for [list display](https://docs.python.org/3.8/reference/expressions.html#list-displays) \*
1. `[]` for list [comprehensions](https://docs.python.org/3.8/reference/expressions.html#displays-for-lists-sets-and-dictionaries) \*
1. `[]` for [subscriptions](https://docs.python.org/3.8/reference/expressions.html#subscriptions) (get, set, del), `:` for [slicing](https://docs.python.org/3.8/reference/expressions.html#slicings) \*

1. `{}` for [set display](https://docs.python.org/3.8/reference/expressions.html#set-displays) \*
1. `{}` for set [comprehensions](https://docs.python.org/3.8/reference/expressions.html#displays-for-lists-sets-and-dictionaries) \*

1. `{}` for [dictionary display](https://docs.python.org/3.8/reference/expressions.html#dictionary-displays) \*
1. `{}` for dictionary [comprehensions](https://docs.python.org/3.8/reference/expressions.html#displays-for-lists-sets-and-dictionaries) \*

1. `()` for [tuple display](https://docs.python.org/3.8/reference/expressions.html#parenthesized-forms) \*

1. `()` for [generator expressions](https://docs.python.org/3.8/reference/expressions.html#generator-expressions) (and [why they can't be unravelled](https://snarky.ca/not-unravelling-generator-expressions/))

1. `()` for [calls](https://docs.python.org/3.8/reference/expressions.html#calls)

1. `@` for [decorators](https://docs.python.org/3.8/reference/compound_stmts.html#function-definitions) \*

1. `,`
1. `;` \*

1. `...` \*

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
