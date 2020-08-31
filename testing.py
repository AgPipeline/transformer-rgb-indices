#!/usr/bin/env python3

"""Test script for algorithm_rgb code
"""

import argparse
import os
import sys
import numpy as np

from osgeo import gdal

import algorithm_rgb


def _file_or_folder_arg(param: str) -> str:
    """Used by argparse to check if an argument is a file or a folder
    Arguments:
        param: the parameter to check
    Returns:
        Returns the param string if it's a valid file or folder that exists. This does not mean that
        the application has the necessary permissions to the file or folder.
    Exception:
        Raises an argparse.ArgumentTypeError exception if the param path doesn't exist
    """
    if os.path.exists(param):
        return param
    raise argparse.ArgumentTypeError('"%s" is not a file or a folder' % param)


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
        sys.stderr.write("\n")
    if units_len != len(variables):
        sys.stderr.write("The number of defined units doesn't match the number of defined variables")
        sys.stderr.write("  continuing processing")
        sys.stderr.write("\n")

    headers = ''
    for idx, variable_name in enumerate(variables):
        variable_header = variable_name
        if idx < labels_len:
            variable_header += ' - %s' % labels[idx]
        if idx < units_len:
            variable_header += ' (%s)' % units[idx]
        headers += variable_header + ','

    return headers


def get_arguments() -> argparse.Namespace:
    """Sets up and parses command line arguments"""
    argparse_description = 'Testing RGB algorithm'
    if hasattr(algorithm_rgb, 'ALGORITHM_NAME') and algorithm_rgb.ALGORITHM_NAME:
        argparse_description += ' for "' + algorithm_rgb.ALGORITHM_NAME + '"'
    parser = argparse.ArgumentParser(argparse_description)

    parser.add_argument('file_folder', action='append', type=_file_or_folder_arg,
                        help='Image files and/or folders containing images')

    return parser.parse_args()


def check_configuration():
    """Checks if the configuration is setup properly for testing
    """
    if not hasattr(algorithm_rgb, 'VARIABLE_NAMES') or not algorithm_rgb.VARIABLE_NAMES:
        sys.stderr.write("Variable names configuration variable is not defined yet. Please define and try again")
        sys.stderr.write("    Update configuration.py and set VARIABLE_NAMES variable with your variable names")
        return False

    return True


def run_test(filename: str):
    """Runs the extractor code using pixels from the file and prints the result
    Args:
        filename: Path to image file
    Return:
        The result of calling the extractor's calculate() method
    Exceptions:
        Raises RuntimeError if there's a problem with the returned values
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
                raise RuntimeError("A 'set' type of data was returned and isn't supported. "
                                   "Please use a list or a tuple instead")

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


def process_files(user_args: argparse.Namespace):
    """Processes the command line file/folder arguments
    Parameters:
        user_args: the result of parsing the command line using argparse
    """
    if user_args:
        print("Filename," + _get_variables_header_fields())
        for one_path in user_args.file_folder:
            if not os.path.isdir(one_path):
                run_test(one_path)
            else:
                allfiles = [os.path.join(one_path, fn) for fn in os.listdir(one_path)
                            if os.path.isfile(os.path.join(one_path, fn))]
                for one_file in allfiles:
                    run_test(one_file)


if __name__ == "__main__":
    args = get_arguments()
    if args and check_configuration():
        process_files(args)
    sys.exit(0)
