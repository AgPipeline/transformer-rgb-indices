"""Greenness Transformer
"""

# Importing modules.
import numpy as np

# Definitions
VERSION = '1.0'

# Information on the creator of this algorithm
ALGORITHM_AUTHOR = 'Chris Schnaufer, Clairessa Brown, David Lebauer'
ALGORITHM_AUTHOR_EMAIL = 'schnaufer@arizona.edu, clairessabrown@email.arizona.edu, dlebauer@email.arizona.edu'
ALGORITHM_CONTRIBUTORS = ["Jacob van der Leeuw"]

ALGORITHM_NAME = 'Greenness Transformer'
ALGORITHM_DESCRIPTION = 'This algorithm performs a variety of calculations using RGB pixels from images in order' \
                        'to assess plant and crop health and growth'

# Citation information for publication
CITATION_AUTHOR = 'Clairessa Brown'
CITATION_TITLE = 'Woebbecke, D.M. et al'
CITATION_YEAR = '2020'

# The name of one or more variables returned by the algorithm, separated by commas

VARIABLE_NAMES = 'excess greenness index, green leaf index, cive, normalized difference index, excess red, ' \
                 'exgr, combined indices 1, combined indices 2, vegetative index, normalized green-red difference,' \
                 ' percent green'

# Variable units matching the order of VARIABLE_NAMES, also comma-separated.
VARIABLE_UNITS = '[-510:510], [-1:1], [-255:255], [-127:129], [-255:255], [-255:332], ' \
                 '[-1000:1000], [-1000:1000], [-255:255], [-255:255], [0:100]'

# Variable labels matching the order of VARIABLE_NAMES, also comma-separated.
VARIABLE_LABELS = 'excess_greenness_index, green_leaf_index, cive, normalized_difference_index(pxarray), ' \
                'excess_red, exgr, combined_indices_1, combined_indices_2, vegetative_index, ngrdi, percent_green'

# Optional override for the generation of a BETYdb compatible csv file
WRITE_BETYDB_CSV = True

# Optional override for the generation of a TERRA REF Geostreams compatible csv file
WRITE_GEOSTREAMS_CSV = True


# Entry point for plot-level RBG algorithm


def excess_greenness_index(pxarray: np.ndarray) -> float:
    """
    Minimizes variation between different illuminations and enhances detection
    of plants
    """
    red, green, blue = get_red_green_blue_averages(pxarray)

    return round(2 * green - (red + blue), 2)


def green_leaf_index(pxarray: np.ndarray) -> float:
    """
    Calculates the green leaf index of an image
    """
    red, green, blue = get_red_green_blue_averages(pxarray)

    return round((2 * green - red - blue) / (2 * green + red + blue), 2)


def cive(pxarray: np.ndarray) -> float:
    """
    Can measure crop growth status
    """
    red, green, blue = get_red_green_blue_averages(pxarray)

    return round(0.441 * red - 0.811 * green + 0.385 * blue + 18.78745, 2)


def normalized_difference_index(pxarray: np.ndarray) -> float:
    """
    Calculates the normalized difference index of an image
    """
    red, green, _ = get_red_green_blue_averages(pxarray)

    return round(128 * ((green - red) / (green + red)) + 1, 2)


def excess_red(pxarray: np.ndarray) -> float:
    """
    Finds potential illumination issues that make it difficult to
    tease apart redness from crops/leaves from soil or camera
    artifacts
    """
    red, green, _ = get_red_green_blue_averages(pxarray)

    return round(1.3 * red - green, 2)


def exgr(pxarray: np.ndarray) -> float:
    """
    Minimizes the variation between different illuminations
    """

    return round(excess_greenness_index(pxarray) - excess_red(pxarray), 2)


def combined_indices_1(pxarray: np.ndarray) -> float:
    """
    Combined indices calculation 1
    """

    return round(excess_greenness_index(pxarray) + cive(pxarray), 2)


def combined_indices_2(pxarray: np.ndarray) -> float:
    """
    Combined indices calculation 2
    """

    return round(0.36 * excess_greenness_index(pxarray) + 0.47 * cive(pxarray) + 0.17 * vegetative_index(pxarray), 2)


def vegetative_index(pxarray: np.ndarray) -> float:
    """
    Minimize illumination differences between images
    """
    red, green, blue = get_red_green_blue_averages(pxarray)

    return round(green / ((red ** 0.667) * (blue ** .333)), 2)


def ngrdi(pxarray: np.ndarray) -> float:
    """
    Can measure crop growth status
    """
    red, green, _ = get_red_green_blue_averages(pxarray)

    return round((green - red) / (green + red), 2)


def percent_green(pxarray: np.ndarray) -> float:
    """
    Returns the percentage of an image that is green, which can be used
    to identify plant cover
    """
    if pxarray.shape[2] < 4:
        # Get redness, greenness, and blueness values
        red = np.sum(pxarray[:, :, 0])
        green = np.sum(pxarray[:, :, 1])
        blue = np.sum(pxarray[:, :, 2])
    else:
        # Handle Alpha channel masking
        # Get redness, greenness, and blueness values
        alpha_mask = np.where(pxarray[:, :, 3] == 0, 1, 0)  # Convert alpha channel to numpy.ma format
        channel_masked = np.ma.array(pxarray[:, :, 0], mask=alpha_mask)
        red = np.ma.sum(channel_masked)
        channel_masked = np.ma.array(pxarray[:, :, 1], mask=alpha_mask)
        green = np.ma.sum(channel_masked)
        channel_masked = np.ma.array(pxarray[:, :, 2], mask=alpha_mask)
        blue = np.ma.sum(channel_masked)
        del channel_masked

    return round(green / (red + green + blue), 2)


def get_red_green_blue_averages(pxarray: np.ndarray) -> tuple:
    """
    Returns the average red, green, and blue values in a pxarray object
    """
    if pxarray.shape[2] < 4:
        # Get redness, greenness, and blueness values
        red = np.average(pxarray[:, :, 0])
        green = np.average(pxarray[:, :, 1])
        blue = np.average(pxarray[:, :, 2])
    else:
        # Handle Alpha channel masking
        # Get redness, greenness, and blueness values
        alpha_mask = np.where(pxarray[:, :, 3] == 0, 1, 0)  # Convert alpha channel to numpy.ma format
        channel_masked = np.ma.array(pxarray[:, :, 0], mask=alpha_mask)
        red = np.ma.average(channel_masked)
        channel_masked = np.ma.array(pxarray[:, :, 1], mask=alpha_mask)
        green = np.ma.average(channel_masked)
        channel_masked = np.ma.array(pxarray[:, :, 2], mask=alpha_mask)
        blue = np.ma.average(channel_masked)
        del channel_masked

    return red, green, blue


def calculate(pxarray: np.ndarray) -> list:
    """Calculates one or more values from plot-level RGB data
    Arguments:
        pxarray: Array of RGB data for a single plot
    Return:
        Returns a list of the calculated values from the
    """
    return_list = [excess_greenness_index(pxarray), green_leaf_index(pxarray), cive(pxarray),
                   normalized_difference_index(pxarray), excess_red(pxarray), exgr(pxarray),
                   combined_indices_1(pxarray), combined_indices_2(pxarray), vegetative_index(pxarray),
                   ngrdi(pxarray), percent_green(pxarray)]

    return return_list
