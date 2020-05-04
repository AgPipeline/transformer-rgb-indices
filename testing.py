#!/usr/bin/env python3

"""Test script for algorithm_rgb code
"""

import os
import sys
import numpy as np
import gdal

import algorithm_rgb


def _get_variables_header_fields() -> str:
    """Returns a string representing the variable header fields
    Return:
        Returns a string representing the variables' header fields
    """
    variables = algorithm_rgb.VARIABLE_NAMES.split(',')
    labels = algorithm_rgb.VARIABLE_LABELS.split(',')
    labels_len = len(labels)
    units = algorithm_rgb.VARIABLE_UNITS.split(',')
    units_len = len(units)

    if labels_len != len(variables):
        sys.stderr.write("The number of defined labels doesn't match the number of defined variables")
        sys.stderr.write("  continuing processing")
    if units_len != len(variables):
        sys.stderr.write("The number of defined units doesn't match the number of defined variables")
        sys.stderr.write("  continuing processing")

    headers = ''
    for idx, variable_name in enumerate(variables):
        variable_header = variable_name
        if idx < labels_len:
            variable_header += ' - %s' % labels[idx]
        if idx < units_len:
            variable_header += ' (%s)' % units[idx]
        headers += variable_header + ','

    return headers


def print_usage():
    """Displays information on how to use this script
    """
    argc = len(sys.argv)
    if argc:
        our_name = os.path.basename(sys.argv[0])
    else:
        our_name = os.path.basename(__file__)
    print(our_name + " <folder>|<filename> ...")
    print("    folder:   path to folder containing images to process")
    print("    filename: path to an image file to process")
    print("")
    print("  One or more folders and/or filenames can be used")
    print("  Only files at the top level of a folder are processed")


def check_arguments():
    """Checks that we have script argument parameters that appear valid
    """
    argc = len(sys.argv)
    if argc < 2:
        sys.stderr.write("One or more paths to images need to be specified on the command line\n")
        print_usage()
        return False

    # Check that the paths exist.
    have_errors = False
    for idx in range(1, argc):
        if not os.path.exists(sys.argv[idx]):
            print("The following path doesn't exist: " + sys.argv[idx])
            have_errors = True

    if have_errors:
        sys.stderr.write("Please correct any problems and try again\n")

    return not have_errors


def check_configuration():
    """Checks if the configuration is setup properly for testing
    """
    if not hasattr(algorithm_rgb, 'VARIABLE_NAMES') or not algorithm_rgb.VARIABLE_NAMES:
        sys.stderr.write("Variable names configuration variable is not defined yet. Please define and try again")
        sys.stderr.write("    Update configuration.py and set VALUE_NAMES variable with your variable names")
        return False

    return True


def run_test(filename):
    """Runs the extractor code using pixels from the file
    Args:
        filename(str): Path to image file
    Return:
        The result of calling the extractor's calculate() method
    Notes:
        Assumes the path passed in is valid. An error is reported if
        the file is not an image file.
    """
    try:
        open_file = gdal.Open(filename)
        if open_file:
            # Get the pixels and call the calculation
            pix = np.array(open_file.ReadAsArray())
            calc_val = algorithm_rgb.calculate(np.rollaxis(pix, 0, 3))

            # Check for unsupported types
            if isinstance(calc_val, set):
                raise RuntimeError("A 'set' type of data was returned and isn't supported.  Please use a list or a tuple instead")

            # Perform any type conversions to a printable string
            if isinstance(calc_val, str):
                print_val = calc_val
            else:
                # Check if the return is iterable and comma separate the values if it is
                try:
                    _ = iter(calc_val)
                    print_val = ",".join(map(str, calc_val))
                except Exception:
                    print_val = str(calc_val)

            print(filename + "," + print_val)
    except Exception as ex:
        sys.stderr.write("Exception caught: " + str(ex) + "\n")
        sys.stderr.write("    File: " + filename + "\n")


def process_files():
    """Processes the command line file/folder arguments
    """
    argc = len(sys.argv)
    if argc:
        print("Filename," + _get_variables_header_fields())
        for idx in range(1, argc):
            cur_path = sys.argv[idx]
            if not os.path.isdir(cur_path):
                run_test(cur_path)
            else:
                allfiles = [os.path.join(cur_path, fn) for fn in os.listdir(cur_path)  if os.path.isfile(os.path.join(cur_path, fn))]
                for one_file in allfiles:
                    run_test(one_file)


if __name__ == "__main__":
    if check_arguments() and check_configuration():
        process_files()
