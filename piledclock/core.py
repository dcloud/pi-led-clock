# unicornhathd at 90 degrees is:
# x left to right
# y top to bottom

from .conf import QUAD_SIZE
from .colors import Color

# Calculate the values to extract bits from the bit chars
# FYI, the range is reversed because drawing is from left-to-right
bit_steps = tuple([2 ** x for x in reversed(range(0, QUAD_SIZE))])


def split_digits(t):
    return (t // 10, t % 10)


def make_bitmap(char, offset=(0, 0), color=Color.WHITE):
    color_value = color.value if isinstance(color, Color) else color
    for x_pos, bits in enumerate(char):
        x = x_pos + offset[1]
        for y_pos, step in enumerate(bit_steps):
            y = y_pos + offset[0]
            pixel_on = bits & step != 0
            yield ((x, y), color_value if pixel_on else Color.BLACK.value)


def print_bitmap(display, bitmap):
    for pixel, color in bitmap:
        display.set_pixel(*pixel, *color)
