import builtins

import pytest

import desugar.builtins


class NonDataProp:
    msg = "non-data property"

    def __get__(self, instance, owner=None):
        return self.msg


class NonDataPropSubclass(NonDataProp):
    pass


class SetDataProp(NonDataProp):
    msg = "__set__"

    def __set__(self, instance, value):
        return value


class DeleteDataProp(NonDataProp):
    msg = "__delete__"

    def __delete__(self, instance):
        return "__delete__"


class ObjectBaseExample:
    @property
    def data_prop(self):
        return "should never be reached (superclass non-data property)"

    superclass_attr = "superclass attribute"


class ObjectExample(ObjectBaseExample):
    @property
    def data_prop(self):
        return "data property"

    set_data_prop = SetDataProp()
    delete_data_prop = DeleteDataProp()

    def __init__(self):
        self.ins_attr = "instance attribute"
        self.__dict__["data_prop"] = self.__dict__["set_data_prop"] = self.__dict__[
            "delete_data_prop"
        ] = "Should never be reached (instance attribute)"

    non_data_prop = NonDataProp()
    non_data_prop_subclass = NonDataPropSubclass()

    class_attr = "class attribute"
    ins_attr = "should never be reached (class attribute)"


class GetattrExample(ObjectBaseExample):

    """Override object.__getattribute__()."""

    def __getattribute__(self, attr):
        return 42


class GetattrMissing:
    def __getattribute__(self, attr):
        raise AttributeError("uh-oh")

    def __getattr__(self, attr):
        return 42


@pytest.mark.parametrize("getattr", [builtins.getattr, desugar.builtins.getattr])
class TestGetattr:

    """Tests for getattr()."""

    def test_getattribute(self, getattr):
        """A class defining __getattribute__() has that method called."""
        assert getattr(ObjectExample(), "ins_attr") == "instance attribute"

    def test_getattribute_overriding(self, getattr):
        """A subclass' __getattribute__() gets called over the superclass."""
        assert getattr(GetattrExample(), "superclass_attr") == 42
        assert (
            object.__getattribute__(GetattrExample(), "superclass_attr")
            == "superclass attribute"
        )

    def test_getattribute_from_type(self, getattr):
        """__getattribute__() is not fetched from the instance."""
        ins = ObjectExample()
        ins.__getattribute__ = lambda self, attr: 42
        assert getattr(ins, "ins_attr") == "instance attribute"

    def test_attr_type(self, getattr):
        """Only the str type is acceptable for the attribute name."""
        with pytest.raises(TypeError):
            getattr(GetattrExample(), 42)

    def test_AttributeError(self, getattr):
        with pytest.raises(AttributeError):
            getattr(ObjectExample(), "not_real")

    def test_getattr_method(self, getattr):
        assert getattr(GetattrMissing(), "not_real") == 42

    def test_default(self, getattr):
        assert getattr(ObjectExample(), "not_real", 42) == 42


@pytest.mark.parametrize(
    "__getattribute__",
    [builtins.object.__getattribute__, desugar.builtins.object.__getattribute__],
)
class TestObjectGetattribute:

    """Tests for  object.__getattribute__()."""

    def test_full_data_descriptor(self, __getattribute__):
        """A data descriptor on the class will be found."""
        assert __getattribute__(ObjectExample(), "data_prop") == "data property"

    def test_set_data_descriptor(self, __getattribute__):
        assert __getattribute__(ObjectExample(), "set_data_prop") == "__set__"

    def test_delete_data_descriptor(self, __getattribute__):
        assert __getattribute__(ObjectExample(), "delete_data_prop") == "__delete__"

    def test_instance_attr(self, __getattribute__):
        """An attribute on the instance will be found."""
        assert __getattribute__(ObjectExample(), "ins_attr") == "instance attribute"

    def test_non_data_descriptor(self, __getattribute__):
        """A non-data descriptor on the class will be found."""
        assert __getattribute__(ObjectExample(), "non_data_prop") == "non-data property"

    def test_non_data_descriptor_subclass(self, __getattribute__):
        """A subclass of a non-data descriptor should work."""
        assert (
            __getattribute__(ObjectExample(), "non_data_prop_subclass")
            == "non-data property"
        )

    def test_class_attr(self, __getattribute__):
        """An attribute on the class will be found."""
        assert __getattribute__(ObjectExample(), "class_attr") == "class attribute"

    def test_superclass_attr(self, __getattribute__):
        """An attribute on a superclass will be found."""
        assert (
            __getattribute__(ObjectExample(), "superclass_attr")
            == "superclass attribute"
        )

    def test_missing_attr(self, __getattribute__):
        """AttributeError is raised when an attribute is missing."""
        with pytest.raises(AttributeError):
            __getattribute__(ObjectExample(), "missing_attr")

    def test_bad_attr_name_type(self, __getattribute__):
        """Only strings are acceptable as the attribute name."""
        with pytest.raises(TypeError):
            __getattribute__(ObjectExample(), 42)


@pytest.mark.parametrize(
    "__eq__", [builtins.object.__eq__, desugar.builtins.object.__eq__]
)
class TestEq:
    def test_same(self, __eq__):
        """Same objects result in True."""
        ob = object()
        assert __eq__(ob, ob) is True

    def test_different(self, __eq__):
        """Different objects result in NotImplemented."""
        assert __eq__(object(), object()) is NotImplemented


@pytest.mark.parametrize(
    "__ne__", [builtins.object.__ne__, desugar.builtins.object.__ne__]
)
class TestNe:
    def test_same(self, __ne__):
        """Same objects result in False."""
        ob = object()
        assert __ne__(ob, ob) is False

    def test_different(self, __ne__):
        """Different objects, by default, result in NotImplemented."""
        assert __ne__(object(), object()) is NotImplemented

    def test_defer_to_eq(self, __ne__):
        """__ne__ differs and and negates what __eq__ returns.

        This only applies if the result is not NotImplemented.

        """

        class ImplementEq:
            def __init__(self):
                self.called = False

            def __eq__(self, _):
                self.called = True
                return True

        ob = ImplementEq()

        assert not __ne__(ob, object())
        assert ob.called

    def test_defer_to_eq_not_implemented(self, __ne__):
        """if __eq__ returns NotImplemented, so does __ne__."""

        class EqNotImplemented:
            def __eq__(self, _):
                return NotImplemented

        assert __ne__(EqNotImplemented(), EqNotImplemented()) is NotImplemented

    def test_coercion_false(self, __ne__):
        """If __eq__ does not return NotImplemented and a true value, then
        __ne__ always returns False."""

        class EqTrueNumber:
            def __eq__(self, _):
                return 42

        assert __ne__(EqTrueNumber(), EqTrueNumber()) is False

    def test_coercion_true(self, __ne__):
        """If __eq__ does not return NotImplemented and a false value, then
        __ne__ always returns True."""

        class EqFalseNumber:
            def __eq__(self, _):
                return 0

        assert __ne__(EqFalseNumber(), EqFalseNumber()) is True
