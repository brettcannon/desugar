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
1. [`a // b`](https://docs.python.org/3.8/reference/expressions.html#binary-arithmetic-operations) ➠ [`operator.__floordiv__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a % b`](https://docs.python.org/3.8/reference/expressions.html#binary-arithmetic-operations) ➠ [`operator.__mod__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a ** b`](https://docs.python.org/3.8/reference/expressions.html#binary-arithmetic-operations) ➠ [`operator.__pow__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a << b`](https://docs.python.org/3.8/reference/expressions.html#shifting-operations) ➠ [`operator.__lshift__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a >> b`](https://docs.python.org/3.8/reference/expressions.html#shifting-operations) ➠ [`operator.__rshift__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a & b`](https://docs.python.org/3.8/reference/expressions.html#binary-bitwise-operations) ➠ [`operator.__and__(a, b)`](https://snarky.ca/unravelling-binary-arithmetic-operations-in-python/)
1. [`a ^ b`](https://docs.python.org/3.8/reference/expressions.html#binary-bitwise-operations) ➠ [`operator.__xor__(a, b)`](https://docs.python.org/3.8/reference/expressions.html#binary-bitwise-operations)
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
1. [`(c for b in a)`](https://docs.python.org/3/reference/expressions.html#generator-expressions) ➠ see below ([post](https://snarky.ca/not-unravelling-generator-expressions/))
1. [`[c for b in a]`](https://snarky.ca/unravelling-comprehensions/) ➠ [`list(c for b in a)`](https://snarky.ca/unravelling-comprehensions/)
1. [`{c for b in a}`](https://snarky.ca/unravelling-comprehensions/) ➠ [`set(c for b in a)`](https://snarky.ca/unravelling-comprehensions/)
1. [`{c: d for b in a}`](https://snarky.ca/unravelling-comprehensions/) ➠ [`dict((c, d) for b in a)`](https://snarky.ca/unravelling-comprehensions/)
1. [`[a, b]`](https://docs.python.org/3.8/reference/expressions.html#list-displays) ➠ [`list((a, b))`](https://snarky.ca/unravelling-data-structure-displays/) (includes iterable unpacking)
1. [`{a, b}`](ttps://docs.python.org/3.8/reference/expressions.html#set-displays) ➠ [`set((a, b))`](https://snarky.ca/unravelling-data-structure-displays/) (includes iterable unpacking)
1. [`(a, b)`](https://docs.python.org/3.8/reference/expressions.html#parenthesized-forms)) ➠ [`(lambda *args: args)(a, b)`](https://snarky.ca/unravelling-data-structure-displays/) (includes iterable unpacking)
1. [`{a: b, c: d}`](https://docs.python.org/3.8/reference/expressions.html#dictionary-displays)) ➠ [`dict(((a, b), (c, d)))`](https://snarky.ca/unravelling-data-structure-displays/) (include dictionary unpacking)
1. [`@decorator`](https://docs.python.org/3.8/reference/compound_stmts.html#function-definitions) ➠ see below ([post](https://snarky.ca/unravelling-decorators/))
1. [`break`](https://docs.python.org/3.8/reference/simple_stmts.html#the-break-statement) ➠ see below ([post](https://snarky.ca/unravelling-break-and-continue/))
1. [`continue`](https://docs.python.org/3.8/reference/simple_stmts.html#the-continue-statement) ➠ see below ([post](https://snarky.ca/unravelling-break-and-continue/))
1. `else` clause on [`while`](https://docs.python.org/3.8/reference/compound_stmts.html#the-while-statement) ➠ see below ([post](https://snarky.ca/unravelling-break-and-continue/))
1. `elif` and `else` clauses on [`if`](https://docs.python.org/3.8/reference/compound_stmts.html#the-if-statement) ➠ see below ([post](https://snarky.ca/unravelling-break-and-continue/))
1. `else` clause on [`try`](https://docs.python.org/3.8/reference/compound_stmts.html#the-try-statement) ➠ see below ([post](https://snarky.ca/unravelling-finally-and-else-from-try/))
1. `finally` clause on [`try`](https://docs.python.org/3.8/reference/compound_stmts.html#the-try-statement) ➠ see below ([post](https://snarky.ca/unravelling-finally-and-else-from-try/))
1. [`raise A from B`](https://docs.python.org/3.8/reference/simple_stmts.html#the-raise-statement) ➠ see below ([post](https://snarky.ca/unravelling-from/))
1. [`x[A, B]`](https://docs.python.org/3.8/reference/expressions.html#subscriptions) ➠ `type(x).__getitem__(x, (A, B))`
1. [`x[A, B] = C`](https://docs.python.org/3.8/reference/expressions.html#subscriptions) ➠ [`type(x).__setitem__(x, (A, B), C)`](https://snarky.ca/unravelling-subscriptions-in-python/)
1. [`del x[A, B]`](https://docs.python.org/3.8/reference/expressions.html#subscriptions) ➠ [`type(x).__delitem__(x, (A, B))`](https://snarky.ca/unravelling-subscriptions-in-python/)
1. [`A:B:C`](https://docs.python.org/3.8/reference/expressions.html#slicings) ➠ [`slice(A, B, C)`](https://snarky.ca/unravelling-subscriptions-in-python/)
1. [`4+3j`](https://docs.python.org/3.8/reference/lexical_analysis.html#imaginary-literals) ➠ [`complex(4, 3)`](https://snarky.ca/unravelling-literals/)
1. [`True`](https://docs.python.org/3.8/reference/lexical_analysis.html#keywords) ➠ [`bool(1)`](https://snarky.ca/unravelling-literals/)
1. [`False`](https://docs.python.org/3.8/reference/lexical_analysis.html#keywords) ➠ [`bool(0)`](https://snarky.ca/unravelling-literals/)
1. [`None`](https://docs.python.org/3.8/reference/lexical_analysis.html#keywords) ➠ see below ([post](https://snarky.ca/unravelling-literals/))
1. [`b"ABC"`](https://docs.python.org/3.8/reference/lexical_analysis.html#string-and-bytes-literals) ➠ [`bytes([65, 66, 67])`](https://snarky.ca/unravelling-literals/)
1. [`"ABC"`](https://docs.python.org/3.8/reference/lexical_analysis.html#string-and-bytes-literals) ➠ [`bytes([65, 66, 67]).decode("utf-8")`](https://snarky.ca/unravelling-literals/)
1. [`...`](https://docs.python.org/3/reference/datamodel.html?highlight=ellipsis#the-standard-type-hierarchy) ➠ [`Ellipsis`](https://snarky.ca/unravelling-ellipsis/)
1. [`class A: ...`](https://docs.python.org/3.8/reference/datamodel.html#metaclasses) ➠ see below ([post](https://snarky.ca/unravelling-pythons-classes/))
`. `;` ➠ newline plus proper indentation
1. [`if ...: ...`](https://docs.python.org/3/reference/compound_stmts.html#the-if-statement) ➠ see below ([post](https://snarky.ca/unravelling-if-statements/))
1. [`a := b`](https://docs.python.org/3/reference/expressions.html#assignment-expressions) see the [post](https://snarky.ca/unravelling-assignment-expressions/)
1. [`lambda a: b`](https://docs.python.org/3.8/reference/expressions.html#lambda) ➠ see below ([post](https://snarky.ca/unraveling-lambda-expressions/))
1. [`global A; A = 42`]() ➠ [`getattr(dict, "__setitem__")(globals(), "A", 42)`](https://snarky.ca/unravelling-global/)

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

### `(c for b in a)`

```Python
(c for b in a)
```

➠

```Python
def _gen_exp(_leftmost_iterable):
    for b in _leftmost_iterable:
        yield c

_gen_exp(a)
```


### `@decorator`

```Python
@decorator
def func():
    ...
```

➠

```Python
def func():
    ...

_temp_func_name = func
del func

func = decorator(_temp_func_name)
```

### `break`
```Python
while x:
    break
```

➠

```Python
class _BreakStatement(Exception):
    pass

try:
    while x:
        raise _BreakStatement
except BreakStatement:
    pass
```

### `continue`
```Python
while x:
    continue
```

➠

```Python
class _ContinueStatement(Exception):
    pass

while x:
    try:
        raise _ContinueStatement
    except ContinueStatement:
        pass
```

### `else` clause on a loop
```Python
while x:
    break
else:
    ...
```

➠

```Python
class _BreakStatement(Exception):
    pass

try:
    while x:
        raise _BreakStatement
except _BreakStatement:
    pass
else:
    ...
```

### `if`
```Python
if A:
    B
```

➠

```Python
class _Done(Exception):
    pass

try:
    while A:
        B
        raise _Done
except _Done:
    pass
```

### `elif`/`else` on an `if` statement
```Python
if A:
    B
elif C:
    D
else:
    E
```

➠

```Python
_B_ran = _D_ran = False
if A:
    _B_ran = True
    B
if not _B_ran and C:
    _D_ran = True
    D
if not (_B_ran or _D_ran):
    E
```

### `try`

#### `else`
```Python
try:
    A
except:
    B
else:
    C
```

➠

```Python
_A_finished = False
try:
    A
    _A_finished = True
except:
    B
if _A_finished:
    C
```

#### `finally`
```Python
try:
    A
except Exception:
    B
finally:
    C
```

➠

```Python
try:
    try:
        A
    except Exception:
        B
except BaseException:
    C
    raise
C
```

### `raise A from B`
```Python
raise A from B
```

➠

```Python
_raise = A
if isinstance(_raise, type) and issubclass(_raise, BaseException):
        _raise = _raise()
elif not isinstance(_raise, BaseException):
    raise TypeError("exceptions must derive from BaseException")

_from = B
if isinstance(_from, type) and issubclass(_from, BaseException):
        _from = _from()
if _from is not None:
    _raise.__cause__ = _from

raise _raise
```

### `None`
```Python
None
```

➠

```Python
def _None():
    pass

_None()
```

### `class`

```Python
class Example(SuperClass):
  """Docstring."""
  a: int = 3
  def c(self): return 42
```

➠

```Python
def _exec_Example(_ns):
    _temp_ns = {}

    _temp_ns["__module__"] = _ns["__module__"] = __name__
    _temp_ns[__"qualname__"] = _ns["__qualname__"] = "Example"
    _temp_ns["__doc__"] = _ns["__doc__"] = """Docstring."""
    _temp_ns["__annotations__"] = _ns["__annotations__"] = {"a": int}

    _temp_ns["a"] = _ns["a"] = 3

    def _method_c(self):
        return 42
    _method_c.__name__ = "c"
    _method_c.__qualname__ = "Example.c"
    temp_ns["c"] = _ns["c"] = _method_c
    del _method_c

def _class_Example():
    # Resolving MRO entries.
    bases = types.resolve_bases((SuperClass, ))
    # Determining the appropriate metaclass **and**
    # preparing the class namespace.
    meta, ns, kwds = types.prepare_class("Example", bases)
    # Executing the class body.
    _exec_Example(ns)
    # Creating the class object.
    cls = meta("Example", bases, ns)
    ## Class decorators, if there were any.
    ## Make the namespace read-only.
    cls.__dict__ = read_only_proxy(ns)

    return cls

 Example = _class_Example()
```

### `lambda`
```Python
lambda A: B
```

➠

```Python
def _lambda(A):
    return B
_lambda.__name__ = "<lambda>"
```

## Syntax that can't be unravelled

[Summary post](https://snarky.ca/mvpy-minimum-viable-python/)

### Keywords

Taken from the [`keyword` module](https://github.com/python/cpython/blob/v3.8.3/Lib/keyword.py).

Nothing; all unravelled!

#### Expressions

1. [`yield`](https://docs.python.org/3.8/reference/simple_stmts.html#the-yield-statement)

#### Statements

1. [`def`](https://docs.python.org/3.8/reference/compound_stmts.html#function-definitions)

1. [`global`](https://docs.python.org/3.8/reference/simple_stmts.html#the-global-statement)
1. [`nonlocal`](https://docs.python.org/3.8/reference/simple_stmts.html#the-nonlocal-statement)

1. [`del`](https://docs.python.org/3.8/reference/simple_stmts.html#the-del-statement)

1. [`return`](https://docs.python.org/3.8/reference/simple_stmts.html#the-return-statement)

1. [`try`](https://docs.python.org/3.8/reference/compound_stmts.html#the-try-statement)/`except`

1. [`if`](https://docs.python.org/3.8/reference/compound_stmts.html#the-if-statement)
1. [`while`](https://docs.python.org/3.8/reference/compound_stmts.html#the-while-statement)

### Tokens

Taken from the [`token` module](https://github.com/python/cpython/blob/v3.8.3/Lib/token.py).

1. [`=`](https://docs.python.org/3.8/reference/simple_stmts.html#assignment-statements)

1. `()` for [calls](https://docs.python.org/3.8/reference/expressions.html#calls)

1. `,`

### Literals

1. [Integers](https://docs.python.org/3.8/reference/lexical_analysis.html#integer-literals)
