from datetime import datetime
import time

import unicornhathd as uhd

from .core import (
    split_digits,
    DISPLAY_ROTATION,
    NUMBERS,
    QUAD_SIZE,
    make_bitmap,
    print_bitmap,
)


def main():
    uhd.off()
    uhd.rotation(DISPLAY_ROTATION)
    uhd.brightness(1.0)
    hat_width, hat_height = uhd.get_shape()

    dt = datetime.now()
    time_str = dt.strftime("%I:%M %p")
    print(time_str)

    digits = (*split_digits(dt.hour), *split_digits(dt.minute))
    quadrants = ((x // 2 * QUAD_SIZE, x % 2 * QUAD_SIZE) for x in range(4))

    for n, pos in zip(digits, quadrants):
        bitmap = make_bitmap(NUMBERS[n - 1], offset=pos)
        print_bitmap(uhd, bitmap)

    print("Hour  ", dt.hour)
    print("Minute", dt.minute)

    uhd.show()

    time.sleep(8)

    uhd.clear()
    uhd.off()


if __name__ == "__main__":
    main()
