#!/usr/bin/env python3

# unicornhathd at 90 degrees is:
# x left to right
# y top to bottom

from datetime import datetime
import time

import unicornhathd as uhd

NUMBERS = (
    (
        0b00010000,
        0b00110000,
        0b00010000,
        0b00010000,
        0b00010000,
        0b00010000,
        0b00010000,
        0b00111000,
    ),
    (
        0b00111000,
        0b01000100,
        0b00000100,
        0b00000100,
        0b00001000,
        0b00010000,
        0b00100000,
        0b01111100,
    ),
    (
        0b00111000,
        0b01000100,
        0b00000100,
        0b00011000,
        0b00000100,
        0b00000100,
        0b01000100,
        0b00111000,
    ),
    (
        0b00000100,
        0b00001100,
        0b00010100,
        0b00100100,
        0b01000100,
        0b01111100,
        0b00000100,
        0b00000100,
    ),
    (
        0b01111100,
        0b01000000,
        0b01000000,
        0b01111000,
        0b00000100,
        0b00000100,
        0b01000100,
        0b00111000,
    ),
    (
        0b00111000,
        0b01000100,
        0b01000000,
        0b01111000,
        0b01000100,
        0b01000100,
        0b01000100,
        0b00111000,
    ),
    (
        0b01111100,
        0b00000100,
        0b00000100,
        0b00001000,
        0b00010000,
        0b00100000,
        0b00100000,
        0b00100000,
    ),
    (
        0b00111000,
        0b01000100,
        0b01000100,
        0b00111000,
        0b01000100,
        0b01000100,
        0b01000100,
        0b00111000,
    ),
    (
        0b00111000,
        0b01000100,
        0b01000100,
        0b01000100,
        0b00111100,
        0b00000100,
        0b01000100,
        0b00111000,
    ),
    (
        0b00111000,
        0b01000100,
        0b01000100,
        0b01000100,
        0b01000100,
        0b01000100,
        0b01000100,
        0b00111000,
    ),
)

# We can hardcode the display size
DISPLAY_SIZE = 16
# Attached to pi zero, 180 is proper rotation
DISPLAY_ROTATION = 180

# We split a 16x16 display into 4 quadrants to fit 4 8px characters
QUAD_SIZE = 8
QUAD_DIV = DISPLAY_SIZE // QUAD_SIZE

TEXT_COLOR = (36, 130, 206)
BLACK = (0, 0, 0)

# Calculate the values to extract bits from the bit chars
# FYI, the range is reversed because drawing is from left-to-right
bit_steps = tuple([2 ** x for x in reversed(range(0, QUAD_SIZE))])


def split_digits(t):
    return (t // 10, t % 10)


def make_bitmap(char, offset=(0, 0), color=TEXT_COLOR):
    for x_pos, bits in enumerate(char):
        x = x_pos + offset[1]
        for y_pos, step in enumerate(bit_steps):
            y = y_pos + offset[0]
            pixel_on = bits & step != 0
            yield (x, y), color if pixel_on else BLACK


def print_bitmap(display, bitmap):
    for pixel, color in bitmap:
        display.set_pixel(*pixel, *color)
        print(pixel, color)


def main():
    uhd.off()
    uhd.rotation(DISPLAY_ROTATION)
    uhd.brightness(1.0)
    hat_width, hat_height = uhd.get_shape()

    dt = datetime.now()
    time_str = dt.strftime("%I:%M %p")
    print(time_str)

    hour_tens, hour_ones = split_digits(dt.hour)
    min_tens, min_ones = split_digits(dt.minute)

    digits = (
        (hour_tens, (0, 0)),
        (hour_ones, (8, 0)),
        (min_tens, (0, 8)),
        (min_ones, (8, 8)),
    )

    for n, pos in digits:
        bitmap = make_bitmap(NUMBERS[n - 1], offset=pos)
        print_bitmap(uhd, bitmap)

    print("Hour  ", dt.hour)
    print("Minute", dt.minute)

    uhd.show()

    time.sleep(3)

    uhd.clear()
    uhd.off()


if __name__ == "__main__":
    main()
