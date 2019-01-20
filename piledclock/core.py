from datetime import datetime
import time

import unicornhathd as uhd

from .conf import FADE_INTERVAL, MAX_BRIGHTNESS, QUAD_SIZE
from .chars import NUMBERS
from .colors import Color

# Calculate the values to extract bits from the bit chars
# FYI, the range is reversed because drawing is from left-to-right
bit_steps = tuple([2 ** x for x in reversed(range(0, QUAD_SIZE))])


def split_digits(t):
    return (t // 10, t % 10)


def make_bitmap(char, color_choice, offset=(0, 0)):
    for x_pos, bits in enumerate(char):
        x = x_pos + offset[1]
        for y_pos, step in enumerate(bit_steps):
            y = y_pos + offset[0]
            pixel_on = bits & step != 0
            yield tuple([(x, y), color_choice if pixel_on else Color.BLACK.value])


def print_bitmap(display, bitmap):
    for pixel, color in bitmap:
        display.set_pixel(*pixel, *color)


def to_color_tuple(in_color):
    if isinstance(in_color, Color):
        return in_color.value
    elif isinstance(in_color, tuple) and len(in_color) == 3:
        return in_color
    return None


def run(args):
    color_choices = [
        Color[args.colorname] if args.colorname else None,
        tuple(args.rgb) if args.rgb and len(args.rgb) == 3 else None,
        Color.WHITE,
    ]
    chosen_color = to_color_tuple([x for x in color_choices if x][0])

    if args.verbose > 0:
        print("Use color {}".format(chosen_color))

    uhd.off()
    uhd.rotation(args.rotation)
    uhd.brightness(1.0)

    dt = datetime.now()

    digits = (*split_digits(dt.hour), *split_digits(dt.minute))
    quadrants = ((x % 2 * QUAD_SIZE, x // 2 * QUAD_SIZE) for x in range(4))

    for n, pos in zip(digits, quadrants):
        if args.verbose > 1:
            print(pos, chosen_color)
        bitmap = make_bitmap(NUMBERS[n - 1], chosen_color, offset=pos)
        if args.verbose > 1:
            print(bitmap)
        print_bitmap(uhd, bitmap)

    if args.verbose > 0:
        print("Hour {:02d}".format(dt.hour))
        print("Minute {:02d}".format(dt.minute))

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
