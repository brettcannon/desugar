import operator

import pytest

import desugar.operator


@pytest.mark.parametrize("getitem", [operator.getitem, desugar.operator.__getitem__])
class TestGetitem:

    def test_get(self, getitem):
        container = range(3)
        for x in container:
            assert getitem(container, x) == x

    def test_no_getitem(self, getitem):
        with pytest.raises(TypeError):
            getitem(object, 0)


@pytest.mark.parametrize("setitem", [operator.setitem, desugar.operator.__setitem__])
class TestSetitem:

    def test_set(self, setitem):
        container = [0]
        setitem(container, 0, 42)
        assert container[0] == 42

    def test_no_setitem(self, setitem):
        with pytest.raises(TypeError):
            setitem(object, 0, 0)


@pytest.mark.parametrize("delitem", [operator.delitem, desugar.operator.__delitem__])
class TestDelitem:

    def test_set(self, delitem):
        container = [0]
        delitem(container, 0)
        assert not len(container)

    def test_no_delitem(self, delitem):
        with pytest.raises(TypeError):
            delitem(object, 0)
