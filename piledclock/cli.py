import argparse

from .core import run
from .colors import Color
from .conf import DISPLAY_ROTATION, DISPLAY_DURATION

color_choices = tuple([c.name for c in Color])


def main():
    parser = argparse.ArgumentParser(description="Display time on LED clock")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument("--rotation", type=int, default=DISPLAY_ROTATION)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--color", dest="colorname", choices=color_choices)
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
