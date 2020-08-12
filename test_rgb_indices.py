#!/usr/bin/env python3
"""
Purpose: Unit testing for algorithm_rgb.py
Author : Chris Schnaufer <schnaufer@arizona.edu
Notes:
    This file assumes it's in a subfolder off the main folder
"""

import os
import re
from subprocess import getstatusoutput

SOURCE_FILE = './testing.py'
TEST_IMAGE = './images/rgb_1_2_E.tif'
# PARTIAL_PATH = os.path.abspath(os.path.join('.', SOURCE_FILE))
# SOURCE_PATH = os.path.abspath(os.path.join('.', IMAGES))


# --------------------------------------------------
def test_exists():
    """Asserts that the source file is available"""
    assert (os.path.isfile(SOURCE_FILE) and os.path.isfile(TEST_IMAGE))


# --------------------------------------------------
def test_usage():
    """
    Program prints a "usage" statement when requested
    """
    for flag in ['-h', '--help']:
        ret_val, out = getstatusoutput(f'{SOURCE_FILE} {flag}')
        print(str(ret_val))
        assert ret_val == 0
        #assert re.match('usage', out, re.IGNORECASE)


# --------------------------------------------------
def test_no_args():
    """
    Verify that the program dies on no arguments
    """
    ret_val, out = getstatusoutput(SOURCE_FILE)
    print("HELLO")
    print("HELLO")
    print("HELLO")
    print("HELLO")
    print("HELLO")
    print("HELLO")

    print(str(ret_val))
    assert ret_val == 0
    assert re.search("One or more paths to images need to be specified on the command line", out)


# --------------------------------------------------
def test_good_input():
    """
    Test with good inputs
    """
    cmd = f'{SOURCE_FILE} {TEST_IMAGE}'
    ret_val, output = getstatusoutput(cmd)
    print("output = " + str(output.split("\n")))
    assert ret_val == 0
    assert output.split("\n")[-1] == "./images/rgb_1_2_E.tif,14.0,0.02,16.16,-1.53," \
                                     "56.53,-42.53,30.16,12.81,1.02,-0.02,0.34"
