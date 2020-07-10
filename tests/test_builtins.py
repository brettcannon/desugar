import builtins

import pytest

import desugar.builtins


class NonDataProp:
    def __get__(self, instance, owner=None):
        return "non-data property"


class ObjectBaseExample:
    @property
    def data_prop(self):
        return "should never be reached (superclass non-data property)"

    superclass_attr = "superclass attribute"


class ObjectExample(ObjectBaseExample):
    @property
    def data_prop(self):
        return "data property"

    def __init__(self):
        self.ins_attr = "instance attribute"
        self.__dict__["data_prop"] = "Should never be reached (instance attribute)"

    non_data_prop = NonDataProp()

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

    def test_data_descriptor(self, __getattribute__):
        """A data descriptor on the class will be found."""
        assert __getattribute__(ObjectExample(), "data_prop") == "data property"

    def test_instance_attr(self, __getattribute__):
        """An attribute on the instance will be found."""
        assert __getattribute__(ObjectExample(), "ins_attr") == "instance attribute"

    def test_non_data_descriptor(self, __getattribute__):
        """A non-data descriptor on the class will be found."""
        assert __getattribute__(ObjectExample(), "non_data_prop") == "non-data property"

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
