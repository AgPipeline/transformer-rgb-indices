"""My nifty plot-level RGB algorithm
"""

# Importing modules. Please add any additional import statements below
import numpy as np

# Definitions
# Please replace these definitions' values with the correct ones
VERSION = '1.0'

# Information on the creator of this algorithm
ALGORITHM_AUTHOR = 'Unknown'
ALGORITHM_AUTHOR_EMAIL = ''
ALGORITHM_CONTRIBUTORS = [""]

ALGORITHM_NAME = 'my nifty one'
ALGORITHM_DESCRIPTION = 'This algorithm calculates the niftyness of RGB plot-level images'

# Citation information for publication (more information in HOW_TO.md)
CITATION_AUTHOR = 'unknown'
CITATION_TITLE = ''
CITATION_YEAR = ''

# The name of one or more variables returned by the algorithm, separated by commas (more information in HOW_TO.md)
# If only one name is specified, no comma's are used.
# Note that variable names cannot have comma's in them: use a different separator instead. Also,
# all white space is kept intact; don't add any extra whitespace since it may cause name comparisons
# to fail.
# !! Replace the content of this string with your variable names
VARIABLE_NAMES = 'size of image channels'

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
def calculate(pxarray: np.ndarray):
    """Calculates one or more values from plot-level RGB data
    Arguments:
        pxarray: Array of RGB data for a single plot
    Return:
        Returns one or more calculated values
    """
    # ALGORITHM: replace the following lines with your algorithm
    channel_size = pxarray[:, :, 1].size

    # RETURN: replace the following return with your calculated values. Be sure to order them as defined in VARIABLE_NAMES above
    return channel_size
