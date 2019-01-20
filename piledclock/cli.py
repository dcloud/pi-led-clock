from datetime import datetime
import argparse
import time
import unicornhathd as uhd

from .core import split_digits, make_bitmap, print_bitmap
from .colors import Color
from .chars import NUMBERS
from .conf import (
    DISPLAY_ROTATION,
    DISPLAY_DURATION,
    FADE_INTERVAL,
    MAX_BRIGHTNESS,
    QUAD_SIZE,
)

color_choices = tuple([c.name for c in Color])


def run(args):

    user_color = None
    if args.color:
        user_color = args.color
    elif args.rgb:
        user_color = tuple(args.rgb)
    if args.verbose > 0:
        print("Use color {}".format(user_color))
    uhd.off()
    uhd.rotation(args.rotation)
    uhd.brightness(1.0)

    dt = datetime.now()

    digits = (*split_digits(dt.hour), *split_digits(dt.minute))
    quadrants = ((x % 2 * QUAD_SIZE, x // 2 * QUAD_SIZE) for x in range(4))

    for n, pos in zip(digits, quadrants):
        if args.verbose > 1:
            print(pos, user_color)
        bitmap = make_bitmap(NUMBERS[n - 1], offset=pos, color_choice=user_color)
        if args.verbose > 1:
            print(bitmap)
        print_bitmap(uhd, bitmap)

    if args.verbose > 0:
        print("Hour {:02d}".format(dt.hour))
        print("Minute {:02d}", dt.minute)

    if args.fade:
        if args.verbose > 1:
            print("Fade LEDs")
            print("Set brightness to 0")
        uhd.brightness(0)

    fade_in_range = list(range(1, int(MAX_BRIGHTNESS * FADE_INTERVAL) + 1))
    fade_out_range = list(reversed([0] + fade_in_range))

    uhd.show()

    if args.fade:
        for x in fade_in_range:
            fade_amt = x / FADE_INTERVAL
            if args.verbose > 1:
                print("Fade to {:.3f}".format(fade_amt))
            uhd.brightness(fade_amt)
            uhd.show()
            time.sleep(1 / FADE_INTERVAL)
        uhd.brightness(MAX_BRIGHTNESS)

    if args.verbose > 1:
        print("Sleeping for %s", args.duration)
    time.sleep(args.duration)

    if args.fade:
        for x in fade_out_range:
            fade_amt = x / FADE_INTERVAL
            if args.verbose > 1:
                print("Fade to {:.3f}".format(fade_amt))
            uhd.brightness(fade_amt)
            uhd.show()
            time.sleep(1 / FADE_INTERVAL)
        uhd.brightness(0)

    uhd.clear()
    uhd.off()


def main():
    parser = argparse.ArgumentParser(description="Display time on LED clock")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument("--rotation", type=int, default=DISPLAY_ROTATION)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--color", choices=color_choices, default=Color.WHITE.name)
    group.add_argument("--rgb", nargs=3, type=int)
    parser.add_argument("--no-fade", action="store_false", dest="fade")
    parser.add_argument(
        "--duration",
        type=float,
        default=DISPLAY_DURATION,
        help="Number of seconds to display the time",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
