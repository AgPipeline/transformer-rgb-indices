#!/usr/bin/env python3
"""
Purpose: Unit testing for algorithm_rgb.py
Author : Chris Schnaufer <schnaufer@arizona.edu>
Notes:
    This file assumes it's in a subfolder off the main folder
"""

import argparse
import os
import re
from subprocess import getstatusoutput
import pytest

TESTING_FILE = 'testing.py'
TESTING_PATH = os.path.abspath(os.path.join('.', TESTING_FILE))

# Test image to use
TEST_IMAGE = os.path.realpath('./test_data/rgb_1_2_E.tif')
TEST_IMAGE_FOLDER = os.path.split(TEST_IMAGE)[0]


def test_exists():
    """Asserts that the source file is available"""
    assert (os.path.isfile(TESTING_PATH) and os.path.isfile(TEST_IMAGE))


# Unit testing
def test_fail_file_or_folder_arg():
    """Tests non-files or folders passed in to file-or-folder testing used by argparse"""
    # pylint: disable=import-outside-toplevel, protected-access
    import testing as tt

    for one_folder in ['/bogus/folder', 'invalid_file.xyz']:
        with pytest.raises(argparse.ArgumentTypeError):
            _ = tt._file_or_folder_arg(one_folder)


def test_file_or_folder_arg():
    """Tests file-or-folder function used by argparse to validate input"""
    # pylint: disable=import-outside-toplevel, protected-access
    import testing as tt

    for one_folder in [os.path.abspath('.'), TEST_IMAGE]:
        res = tt._file_or_folder_arg(one_folder)
        assert res == one_folder


def test_get_variables_header_fields():
    """Tests getting variables header fields"""
    # pylint: disable=import-outside-toplevel, protected-access
    import testing as tt

    headers = tt._get_variables_header_fields()
    assert len(headers) >= 1


def test_check_configuration():
    """Checks that the configuration is setup"""
    # pylint: disable=import-outside-toplevel
    import testing as tt

    setup = tt.check_configuration()
    assert setup is True


# Integration Testing
def test_usage():
    """Program prints a "usage" statement when requested"""
    for flag in ['-h', '--help']:
        ret_val, out = getstatusoutput(f'{TESTING_PATH} {flag}')
        assert re.match('usage', out, re.IGNORECASE)
        assert ret_val == 0


def test_no_args():
    """Verify that the program dies on no arguments"""
    ret_val, out = getstatusoutput(f'{TESTING_PATH}')
    assert ret_val == 2
    assert re.search('the following arguments are required', out)


def test_good_file():
    """Test with good inputs"""
    cmd = f'{TESTING_PATH} {TEST_IMAGE}'
    ret_val, out = getstatusoutput(cmd)
    assert ret_val == 0
    assert out.split("\n")[-1] == f"{TEST_IMAGE},14.0,0.02,16.16,-1.53,"\
                                  "56.53,-42.53,30.16,12.81,1.02,-0.02,0.34"


def test_good_folder():
    """Test with good inputs"""
    cmd = f'{TESTING_PATH} {TEST_IMAGE_FOLDER}'
    ret_val, out = getstatusoutput(cmd)
    assert ret_val == 0
    assert out.split("\n")[-1] == f"{TEST_IMAGE},14.0,0.02,16.16,-1.53,"\
                                  "56.53,-42.53,30.16,12.81,1.02,-0.02,0.34"
