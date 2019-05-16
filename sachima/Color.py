import random
import colorsys
import matplotlib as mpl

# must befor seaborn import for ImportError: libGL.so.1: cannot open shared object file: No such file or directory
#
mpl.use("Agg")
import seaborn as sns


def get_random_color(pastel_factor=0.5):
    return [
        (x + pastel_factor) / (1.0 + pastel_factor)
        for x in [random.uniform(0, 1.0) for i in [1, 2, 3]]
    ]


def color_distance(c1, c2):
    return sum([abs(x[0] - x[1]) for x in zip(c1, c2)])


def generate_new_color(existing_colors, pastel_factor=0.5):
    max_distance = None
    best_color = None
    for i in range(0, 100):
        color = get_random_color(pastel_factor=pastel_factor)
        if not existing_colors:
            return color
        best_distance = min(
            [color_distance(color, c) for c in existing_colors]
        )
        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color
    return best_color


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def gen_hex_colors(colorcode, N):
    # (210, 90, 60)"#"
    # colors = sns.light_palette((254, 67, 101), input="husl",n_colors=N)
    # https://seaborn.pydata.org/generated/seaborn.light_palette.html
    colors = sns.light_palette(colorcode, n_colors=N)
    hex_colors = []

    # for i in range(0,N):
    #     colors.append(generate_new_color(colors,pastel_factor=0.0000001) )

    for c in colors:
        hex_colors.append(
            rgb2hex(int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))
        )

    return hex_colors


# Example:
# if __name__ == "__main__":
#     pass
# print(gen_hex_colors(100))
# print(sns.color_palette("Blues"))
# print(colnum_string(98))
