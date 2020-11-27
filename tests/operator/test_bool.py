import operator

import pytest

import desugar.operator


@pytest.mark.parametrize("truth", [operator.truth, desugar.operator.truth])
class TestTruth:

    """Tests for operator.truth()."""

    def test_true(self, truth):
        """True results in True."""
        assert truth(True) is True

    def test_false(self, truth):
        """False results in False."""
        assert truth(False) is False

    def test_none(self, truth):
        """None results in None."""
        assert truth(None) is False

    @pytest.mark.parametrize("expected", [True, False])
    def test___bool__(self, truth, expected):
        """__bool__() returning True or False results in that being returned."""

        class Spam:
            def __bool__(self):
                return expected

        assert truth(Spam()) is expected

    def test___bool__not_bool(self, truth):
        """__bool__() returning a non-boolean is a TypeError."""

        class Spam:
            def __bool__(self):
                return 42  # Something that is true on its own.

        with pytest.raises(TypeError):
            truth(Spam())

    @pytest.mark.parametrize("length,expected", [(0, False), (1, True), (42, True)])
    def test_len(self, truth, length, expected):
        """len() is called if __bool__() is not defined."""

        class Spam:
            def __len__(self):
                return length

        assert truth(Spam()) is expected

    def test_true_default(self, truth):
        """If an object defines neither __bool__() nor len(), then it's True."""

        class Spam:
            """No definition of __bool__ or __len__."""

        assert truth(Spam()) is True


@pytest.mark.parametrize("not_", [operator.not_, desugar.operator.not_])
class TestNot:

    """Tests for operator.not_()."""

    def test_true(self, not_):
        """True leads to False."""
        assert not_(True) is False

    def test_false(self, not_):
        """False leads to True."""
        assert not (False) is True

    @pytest.mark.parametrize("given,expected", [([1], False), ([], True)])
    def test_conversion(self, not_, given, expected):
        """The inverted truth value of an object is returned."""
        assert not_(given) is expected
