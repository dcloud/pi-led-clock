#!/usr/bin/env python3

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

bit_steps = tuple([2 ** x for x in range(0, 8)])

TEXT_COLOR = (36, 130, 206)
BLACK = (0, 0, 0)


def split_digits(t):
    return (t // 10, t % 10)


def main():
    uhd.off()
    uhd.rotation(0)
    uhd.brightness(1.0)
    hat_width, hat_height = uhd.get_shape()

    dt = datetime.now()
    time_str = dt.strftime("%I:%M %p")
    print(time_str)

    hour_tens, hour_ones = split_digits(dt.hour)

    for y, bits in enumerate(NUMBERS[hour_tens]):
        for x, step in enumerate(bit_steps):
            pixel_on = bits & step != 0
            print("X" if pixel_on else "O", end="")
            color = TEXT_COLOR if pixel_on else (255, 0, 0)
            uhd.set_pixel(x, y, *color)
        print("")

    print("Hour  ", dt.hour)
    print("Minute", dt.minute)

    uhd.show()


if __name__ == "__main__":
    main()
