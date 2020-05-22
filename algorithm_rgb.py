"""Greenness Transformer
"""

# Importing modules. Please add any additional import statements below
import numpy as np

# Definitions
# Please replace these definitions' values with the correct ones
VERSION = '1.0'

# Information on the creator of this algorithm
ALGORITHM_AUTHOR = 'Chris Schnaufer, Jacob van der Leeuw'
ALGORITHM_AUTHOR_EMAIL = 'schnaufer@arizona.edu, jvanderleeuw@email.arizona.edu'
ALGORITHM_CONTRIBUTORS = ["David Lebauer"]

ALGORITHM_NAME = 'my nifty one'
ALGORITHM_DESCRIPTION = 'This algorithm calculates the niftyness of RGB plot-level images'

# Citation information for publication (more information in HOW_TO.md)
CITATION_AUTHOR = 'unknown'
CITATION_TITLE = 'Woebbecke, D.M. et al'
CITATION_YEAR = '2020'

# The name of one or more variables returned by the algorithm, separated by commas (more information in HOW_TO.md)
# If only one name is specified, no comma's are used.
# Note that variable names cannot have comma's in them: use a different separator instead. Also,
# all white space is kept intact; don't add any extra whitespace since it may cause name comparisons
# to fail.

VARIABLE_NAMES = 'excess greenness index, green leaf index, cive, normalized difference index, excess red, ' \
                 'exgr, combined indices 1, combined indices 2, vegetative index, normalized green-red difference,' \
                 ' percent green'

# Variable units matching the order of VARIABLE_NAMES, also comma-separated.
# For each variable name in VARIABLE_NAMES add the unit of measurement the value represents.
# !! Replace the content of this string with your variables' unit
VARIABLE_UNITS = 'pixels'

# Variable labels matching the order of VARIABLE_NAMES, also comma-separated.
# This is an optional definition and can be left empty.
VARIABLE_LABELS = ''

# Optional override for the generation of a BETYdb compatible csv file
# Set to False to suppress the creation of a compatible file
WRITE_BETYDB_CSV = True

# Optional override for the generation of a TERRA REF Geostreams compatible csv file
# Set to False to suppress the creation of a compatible file
WRITE_GEOSTREAMS_CSV = True


# Entry point for plot-level RBG algorithm


def excess_greenness_index(pxarray: np.ndarray) -> float:
    """
    Minimizes variation between different illuminations and enhances detection
    of plants
    """
    red, green, blue = get_red_green_blue_averages(pxarray)

    return 2 * green - (red + blue)


def green_leaf_index(pxarray: np.ndarray) -> float:
    """
    Calculates the green leaf index of an image
    """
    red, green, blue = get_red_green_blue_averages(pxarray)

    return (2 * green - red - blue) / (2 * green + red + blue)


def cive(pxarray: np.ndarray) -> float:
    """
    Can measure crop growth status
    """
    red, green, blue = get_red_green_blue_averages(pxarray)

    return 0.441 * red - 0.811 * green + 0.385 * blue + 18.78745


def normalized_difference_index(pxarray: np.ndarray) -> float:
    """
    Calculates the normalized difference index of an image
    """
    red, green, blue = get_red_green_blue_averages(pxarray)

    return 128 * ((green - red) / (green + red)) + 1


def excess_red(pxarray: np.ndarray) -> float:
    """
    Finds potential illumination issues that make it difficult to
    tease apart redness from crops/leaves from soil or camera
    artifacts
    """
    red, green, blue = get_red_green_blue_averages(pxarray)

    return 1.3 * red - green


def exgr(pxarray: np.ndarray) -> float:
    """
    Minimizes the variation between different illuminations
    """

    return excess_greenness_index(pxarray) - excess_red(pxarray)


def combined_indices_1(pxarray: np.ndarray) -> float:
    """
    Combined indices calculation 1
    """

    return excess_greenness_index(pxarray) + cive(pxarray)


def combined_indices_2(pxarray: np.ndarray) -> float:
    """
    Combined indices calculation 2
    """

    return 0.36 * excess_greenness_index(pxarray) + 0.47 * cive(pxarray) + 0.17 * vegetative_index(pxarray)


def vegetative_index(pxarray: np.ndarray) -> float:
    """
    Minimize illumination differences between images
    """
    red, green, blue = get_red_green_blue_averages(pxarray)

    return green / ((red ** 0.667) * (blue ** .333))


def ngrdi(pxarray: np.ndarray) -> float:
    """
    Can measure crop growth status
    """
    red, green, blue = get_red_green_blue_averages(pxarray)

    return (green - red) / (green + red)


def percent_green(pxarray: np.ndarray) -> float:
    """
    Returns the percentage of an image that is green, which can be used
    to identify plant cover
    """
    # redness value
    red = np.sum(pxarray[:, :, 0])

    # greenness value
    green = np.sum(pxarray[:, :, 1])

    # blueness value
    blue = np.sum(pxarray[:, :, 2])

    return green / (red + green + blue)


def get_red_green_blue_averages(pxarray: np.ndarray) -> tuple:
    """
    Returns the average red, green, and blue values in a pxarray object
    """
    # redness value
    red = np.average(pxarray[:, :, 0])

    # greenness value
    green = np.average(pxarray[:, :, 1])

    # blueness value
    blue = np.average(pxarray[:, :, 2])

    return (red, green, blue)


def calculate(pxarray: np.ndarray) -> list:
    """Calculates one or more values from plot-level RGB data
    Arguments:
        pxarray: Array of RGB data for a single plot
    Return:
        Returns one or more calculated values
    """

    return_list = [excess_greenness_index(pxarray), green_leaf_index(pxarray), cive(pxarray),
                   normalized_difference_index(pxarray), excess_red(pxarray), exgr(pxarray),
                   combined_indices_1(pxarray), combined_indices_2(pxarray), vegetative_index(pxarray),
                   ngrdi(pxarray), percent_green(pxarray)]

    return return_list
