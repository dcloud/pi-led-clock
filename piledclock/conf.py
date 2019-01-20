# We can hardcode the display size
DISPLAY_SIZE = 16
# Attached to pi zero, 180 is proper rotation
DISPLAY_ROTATION = 180

DISPLAY_DURATION = 8

# We split a 16x16 display into 4 quadrants to fit 4 8px characters
QUAD_SIZE = 8
QUAD_DIV = DISPLAY_SIZE // QUAD_SIZE
