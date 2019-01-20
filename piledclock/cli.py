from datetime import datetime
import argparse
import time
import logging
import sys

import unicornhathd as uhd

from .core import split_digits, make_bitmap, print_bitmap
from .chars import NUMBERS
from .conf import DISPLAY_ROTATION, DISPLAY_DURATION, QUAD_SIZE


def run(args):
    uhd.off()
    uhd.rotation(args.rotation)
    uhd.brightness(1.0)
    hat_width, hat_height = uhd.get_shape()

    dt = datetime.now()

    digits = (*split_digits(dt.hour), *split_digits(dt.minute))
    quadrants = ((x // 2 * QUAD_SIZE, x % 2 * QUAD_SIZE) for x in range(4))

    for n, pos in zip(digits, quadrants):
        bitmap = make_bitmap(NUMBERS[n - 1], offset=pos)
        if logging.verbose > 1:
            logging.info(bitmap)
        print_bitmap(uhd, bitmap)

    if args.verbose > 0:
        logging.info("Hour  ", dt.hour)
        logging.info("Minute", dt.minute)

    if args.fade:
        uhd.brightness(0)
    uhd.show()
    if args.fade:
        for x in range(1 / 100):
            uhd.brightness(x)

    time.sleep(args.duration)

    uhd.clear()
    uhd.off()


def main():
    parser = argparse.ArgumentParser(description="Display time on LED clock")
    parser.add_argument("--verbose", "-v", action="count")
    parser.add_argument("--rotation", type=int, default=DISPLAY_ROTATION)
    parser.add_argument("--color", choices=["RED", "GREEN", "BLUE"])
    parser.add_argument("--no-fade", action="store_false", dest="fade")
    parser.add_argument(
        "--duration",
        type=float,
        default=DISPLAY_DURATION,
        help="Number of seconds to display the time",
    )
    args = parser.parse_args(sys.argv)
    run(args)


if __name__ == "__main__":
    main()
