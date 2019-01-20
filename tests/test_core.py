# from unittest.mock import patch

from piledclock.core import split_digits


def test_split_digits():
    assert split_digits(12) == (1, 2)
    assert split_digits(6) == (0, 6)
