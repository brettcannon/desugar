# desugar
Unravelling Python source code.


## Unravelled syntax

1. `obj.attr` ➠ `getattr(obj, "attr")` (including `object.__getattribute__()`)
