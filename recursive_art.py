"""
@author: Sungwoo Park

Computational art program

This python program generates an image based on randomly composed mathematical functions.
"""

import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    one_arg_functions = ['cos_pi','sin_pi','square']
    two_arg_functions = ['prod','avg','neg_prod']
    if min_depth == 0:
        if random.random() < 0.5: #~50% chance each for x or y
            return ['x']
        else:
            return ['y']
    random_index = random.randrange(3)
    if random.random() < 0.5: #~50% chance each for one or two args
        return [one_arg_functions[random_index],build_random_function(min_depth-1,max_depth-1)]
    else:
        return [two_arg_functions[random_index],build_random_function(min_depth-1,max_depth-1),build_random_function(min_depth-1,max_depth-1)]

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        I can't really test square function because python float is decimal approximation of exact decimal. Therefore, I cannot predict exact result.
        
        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(["prod",["x"],["y"]],0.2,0.3)
        0.06
        >>> evaluate_random_function(["prod",["avg",["x"],["y"]],["prod",["x"],["y"]]],0.3,0.5)
        0.06
        >>> evaluate_random_function(["neg_prod",["x"],["y"]],0.5,0.4)
        -0.2

    """
    if f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 'prod':
        return evaluate_random_function(f[1],x,y) * evaluate_random_function(f[2],x,y)
    elif f[0] == 'avg':
        return 0.5 * (evaluate_random_function(f[1],x,y) + evaluate_random_function(f[2],x,y))
    elif f[0] == 'cos_pi':
        return math.cos(math.pi*evaluate_random_function(f[1],x,y))
    elif f[0] == 'sin_pi':
        return math.sin(math.pi*evaluate_random_function(f[1],x,y))
    elif f[0] == 'neg_prod': #negative product
        return -(evaluate_random_function(f[1],x,y) * evaluate_random_function(f[2],x,y))
    elif f[0] == 'square': #square first argument
        return evaluate_random_function(f[1],x,y) ** 2 


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    input_distance_from_start = float(val - input_interval_start)
    input_interval_range = float(input_interval_end - input_interval_start)
    input_raw_value = input_distance_from_start / input_interval_range
    
    output_interval_range = float(output_interval_end - output_interval_start)
    return output_interval_start + (input_raw_value * output_interval_range)

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9)
    green_function = build_random_function(7,9)
    blue_function = build_random_function(7,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    #doctest.testmod(verbose=True)

    generate_art("example1.png")
    generate_art("example2.png")

    # Test that PIL is installed correctly
    #test_image("noise.png")
