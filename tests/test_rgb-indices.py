#!/usr/bin/env python3
"""
Purpose: Unit testing for algorithm_rgb.py
Author : Chris Schnaufer <schnaufer@arizona.edu
Notes:
    This file assumes it's in a subfolder off the main folder
"""

import os
import re
import pytest
from subprocess import getstatusoutput

SOURCE_FILE = 'testing.py'
IMAGES = 'images'
SOURCE_PATH = os.path.abspath(os.path.join(os.path.join('.', SOURCE_FILE)), IMAGES)


def test_exists():
    """Asserts that the source file is available"""
    assert os.path.isfile(SOURCE_PATH)


def test_usage():
    """
    Program prints a "usage" statement when requested
    """
    for flag in ['-h', '--help']:
        ret_val, out = getstatusoutput(f'{SOURCE_PATH} {flag}')
        assert ret_val == 0
        assert re.match('usage', out, re.IGNORECASE)