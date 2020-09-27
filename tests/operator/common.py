class LHS:

    """__*__ methods returning their own name."""

    def __add__(self, _):
        return "__add__"

    def __sub__(self, _):
        return "__sub__"

    def __mul__(self, _):
        return "__mul__"

    def __matmul__(self, _):
        return "__matmul__"

    def __truediv__(self, _):
        return "__truediv__"

    def __floordiv__(self, _):
        return "__floordiv__"

    def __mod__(self, _):
        return "__mod__"

    def __pow__(self, _):
        return "__pow__"

    def __lshift__(self, _):
        return "__lshift__"

    def __rshift__(self, _):
        return "__rshift__"

    def __and__(self, _):
        return "__and__"

    def __xor__(self, _):
        return "__xor__"

    def __or__(self, _):
        return "__or__"


class LHSNotImplemented:

    """__*__ methods returning NotImplemented."""

    def __init__(self):
        super().__init__()
        self.called = 0

    def __add__(self, _):
        self.called += 1
        return NotImplemented

    def __sub__(self, _):
        self.called += 1
        return NotImplemented

    def __mul__(self, _):
        self.called += 1
        return NotImplemented

    def __matmul__(self, _):
        self.called += 1
        return NotImplemented

    def __truediv__(self, _):
        self.called += 1
        return NotImplemented

    def __floordiv__(self, _):
        self.called += 1
        return NotImplemented

    def __mod__(self, _):
        self.called += 1
        return NotImplemented

    def __pow__(self, _):
        self.called += 1
        return NotImplemented

    def __lshift__(self, _):
        self.called += 1
        return NotImplemented

    def __rshift__(self, _):
        self.called += 1
        return NotImplemented

    def __and__(self, _):
        self.called += 1
        return NotImplemented

    def __xor__(self, _):
        self.called += 1
        return NotImplemented

    def __or__(self, _):
        self.called += 1
        return NotImplemented


class RHS:

    """__r*__ methods returning their name."""

    def __radd__(self, _):
        return "__radd__"

    def __rsub__(self, _):
        return "__rsub__"

    def __rmul__(self, _):
        return "__rmul__"

    def __rmatmul__(self, _):
        return "__rmatmul__"

    def __rtruediv__(self, _):
        return "__rtruediv__"

    def __rfloordiv__(self, _):
        return "__rfloordiv__"

    def __rmod__(self, _):
        return "__rmod__"

    def __rpow__(self, _):
        return "__rpow__"

    def __rlshift__(self, _):
        return "__rlshift__"

    def __rrshift__(self, _):
        return "__rrshift__"

    def __rand__(self, _):
        return "__rand__"

    def __rxor__(self, _):
        return "__rxor__"

    def __ror__(self, _):
        return "__ror__"


def radd_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def rsub_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def rmul_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def rmatmul_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def rtruediv_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def rfloordiv_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def rmod_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def rpow_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def rlshift_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def rrshift_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def rand_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def rxor_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


def ror_not_implemented(self, _):
    self.rcalled += 1
    return NotImplemented


class RHSNotImplemented:

    """__r*__ methods returning NotImplemented."""

    def __init__(self):
        super().__init__()
        self.rcalled = 0

    __radd__ = radd_not_implemented
    __rsub__ = rsub_not_implemented
    __rmul__ = rmul_not_implemented
    __rmatmul__ = rmatmul_not_implemented
    __rtruediv__ = rtruediv_not_implemented
    __rfloordiv__ = rfloordiv_not_implemented
    __rmod__ = rmod_not_implemented
    __rpow__ = rpow_not_implemented
    __rlshift__ = rlshift_not_implemented
    __rrshift__ = rrshift_not_implemented
    __rand__ = rand_not_implemented
    __rxor__ = rxor_not_implemented
    __ror__ = ror_not_implemented


class DifferentRHSNotImplemented:

    """__r*__ methods returning NotImplemented."""

    def __init__(self):
        super().__init__()
        self.rcalled = 0

    __radd__ = radd_not_implemented
    __rsub__ = rsub_not_implemented
    __rmul__ = rmul_not_implemented
    __rmatmul__ = rmatmul_not_implemented
    __rtruediv__ = rtruediv_not_implemented
    __rfloordiv__ = rfloordiv_not_implemented
    __rmod__ = rmod_not_implemented
    __rpow__ = rpow_not_implemented
    __rlshift__ = rlshift_not_implemented
    __rrshift__ = rrshift_not_implemented
    __rand__ = rand_not_implemented
    __rxor__ = rxor_not_implemented
    __ror__ = ror_not_implemented


class LHSRHS(LHS, RHS):

    """Class that implements both __*__ and __r*__."""


class LHSRHSSubclass(LHSRHS):

    """A subclass implementing both __*__ and __r*__ which does not differ from its superclass."""


class LHSRHSNotImplemented(LHSNotImplemented, LHS, RHSNotImplemented):

    """A subclass which always returns NotImplemented."""


class LHSRHSNotImplementedSubclass(LHSRHSNotImplemented):

    """A subclass which always returns NotImplemented that is a different type
    of the superclass."""


class Lvalue:

    """Implement __i*__ methods."""

    def __iadd__(self, _):
        return "__iadd__"

    def __isub__(self, _):
        return "__isub__"

    def __imul__(self, _):
        return "__imul__"

    def __imatmul__(self, _):
        return "__imatmul__"

    def __itruediv__(self, _):
        return "__itruediv__"

    def __ifloordiv__(self, _):
        return "__ifloordiv__"

    def __imod__(self, _):
        return "__imod__"

    def __ipow__(self, _):
        return "__ipow__"

    def __ilshift__(self, _):
        return "__ilshift__"

    def __irshift__(self, _):
        return "__irshift__"

    def __iand__(self, _):
        return "__iand__"

    def __ixor__(self, _):
        return "__ixor__"

    def __ior__(self, _):
        return "__ior__"


class LvalueNotImplemented:

    """__i*__ methods which return NotImplemented."""

    def __init__(self):
        super().__init__()
        self.icalled = 0

    def __iadd__(self, _):
        self.icalled += 1
        return NotImplemented

    def __isub__(self, _):
        self.icalled += 1
        return NotImplemented

    def __imul__(self, _):
        self.icalled += 1
        return NotImplemented

    def __imatmul__(self, _):
        self.icalled += 1
        return NotImplemented

    def __itruediv__(self, _):
        self.icalled += 1
        return NotImplemented

    def __ifloordiv__(self, _):
        self.icalled += 1
        return NotImplemented

    def __imod__(self, _):
        self.icalled += 1
        return NotImplemented

    def __ipow__(self, _):
        self.icalled += 1
        return NotImplemented

    def __ilshift__(self, _):
        self.icalled += 1
        return NotImplemented

    def __irshift__(self, _):
        self.icalled += 1
        return NotImplemented

    def __iand__(self, _):
        self.icalled += 1
        return NotImplemented

    def __ixor__(self, _):
        self.icalled += 1
        return NotImplemented

    def __ior__(self, _):
        self.icalled += 1
        return NotImplemented


class LvalueNotImplementedLHS(LvalueNotImplemented, LHS):

    """__i*__ returns NotImplemented, __*__ implemented."""


class LvalueLHSRHSNotImplemented(
    LvalueNotImplemented, LHSNotImplemented, RHSNotImplemented
):

    """__*__, __r*__, and __i*__ all return NotImplemented."""


class LHSRHSNotImplementedLvalue(LHSRHSNotImplemented, Lvalue):

    """__i*__ implemented, __*__, __r*__ return NotImplemented."""


class GtEqGeComparisons:
    def __gt__(self, _):
        return "__gt__"

    def __eq__(self, _):
        return "__eq__"

    def __ge__(self, _):
        return "__ge__"


class LtNeLeComparisons:
    def __lt__(self, _):
        return "__lt__"

    def __ne__(self, _):
        return "__ne__"

    def __le__(self, _):
        return "__le__"


class ComparisonsNotImplemented:
    def __init__(self, collection):
        self.called = collection

    def __gt__(self, _):
        self.called.append((self, "__gt__"))
        return NotImplemented

    def __eq__(self, _):
        self.called.append((self, "__eq__"))
        return NotImplemented

    def __ge__(self, _):
        self.called.append((self, "__ge__"))
        return NotImplemented

    def __lt__(self, _):
        self.called.append((self, "__lt__"))
        return NotImplemented

    def __ne__(self, _):
        self.called.append((self, "__ne__"))
        return NotImplemented

    def __le__(self, _):
        self.called.append((self, "__le__"))
        return NotImplemented


class ComparisonsNotImplementedSubclass(ComparisonsNotImplemented):
    pass


class DifferentComparisonsNotImplemented:
    def __init__(self, collection):
        self.called = collection

    def __gt__(self, _):
        self.called.append((self, "__gt__"))
        return NotImplemented

    def __eq__(self, _):
        self.called.append((self, "__eq__"))
        return NotImplemented

    def __ge__(self, _):
        self.called.append((self, "__ge__"))
        return NotImplemented

    def __lt__(self, _):
        self.called.append((self, "__lt__"))
        return NotImplemented

    def __ne__(self, _):
        self.called.append((self, "__ne__"))
        return NotImplemented

    def __le__(self, _):
        self.called.append((self, "__le__"))
        return NotImplemented
