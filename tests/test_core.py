import sys
from unittest.mock import Mock, call

sys.modules["unicornhathd"] = Mock()
mock_display = Mock()


def test_print_bitmap():
    from piledclock.core import print_bitmap

    bitmap = [((0, 0), (255, 255, 255)), ((0, 1), (255, 255, 0))]
    print_bitmap(mock_display, bitmap)

    mock_display.set_pixel.assert_has_calls(
        [call(0, 0, 255, 255, 255), call(0, 1, 255, 255, 0)]
    )


def test_split_digits():
    from piledclock.core import split_digits

    assert split_digits(12) == (1, 2)
    assert split_digits(6) == (0, 6)
