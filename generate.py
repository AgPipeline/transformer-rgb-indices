#!/usr/bin/env python3

"""Generates files used to create Docker images
"""
import datetime

import algorithm_rgb

# Names of empty files to create
EMPTY_FILE_NAMES = ['requirements.txt', 'packages.txt']

# The name of the Docker build file
DOCKERFILE_NAME = 'Dockerfile'

# Template contents of the Docker build file
DOCKERFILE_CONTENTS = [
    'FROM agpipeline/rgb-plot-base-image:latest',
    'LABEL maintainer="Someone <someone@example.com>"',
    '',
    'COPY requirements.txt packages.txt /home/extractor/',
    '',
    'USER root',
    '',
    'RUN [ -s /home/extractor/packages.txt ] && \\',
    '    (echo "Installing packages" && \\',
    '        apt-get update && \\',
    '       cat /home/extractor/packages.txt | xargs apt-get install -y --no-install-recommends && \\',
    '        rm /home/extractor/packages.txt && \\',
    '        apt-get autoremove -y && \\',
    '        apt-get clean && \\',
    '        rm -rf /var/lib/apt/lists/*) || \\',
    '    (echo "No packages to install" && \\',
    '        rm /home/extractor/packages.txt)',
    '',
    'RUN [ -s /home/extractor/requirements.txt ] && \\',
    '    (echo "Install python modules" && \\',
    '    python -m pip install -U --no-cache-dir pip && \\',
    '    python -m pip install --no-cache-dir setuptools && \\',
    '     python -m pip install --no-cache-dir -r /home/extractor/requirements.txt && \\',
    '     rm /home/extractor/requirements.txt) || \\',
    '    (echo "No python modules to install" && \\',
    '     rm /home/extractor/requirements.txt)',
    '',
    'USER extractor'
    '',
    'COPY algorithm_rgb.py /home/extractor/'
]

# Required variables in algorithm_rgb
REQUIRED_VARIABLES = [
    'ALGORITHM_AUTHOR',
    'ALGORITHM_AUTHOR_EMAIL',
    'ALGORITHM_NAME',
    'ALGORITHM_DESCRIPTION',
    'VARIABLE_NAMES'
]

# Variables in algorithm_rgb that are required to not be empty
REQUIRED_NOT_EMPTY_VARIABLES = [
    'VARIABLE_NAMES'
]

# Variables in algorithm_rgb that should be filled in, but aren't required to be
PREFERRED_NOT_EMPTY_VARIABLES = [
    'ALGORITHM_AUTHOR',
    'ALGORITHM_AUTHOR_EMAIL',
    'ALGORITHM_NAME',
    'ALGORITHM_DESCRIPTION',
    'CITATION_AUTHOR',
    'CITATION_TITLE',
    'CITATION_YEAR'
]


def check_environment() -> bool:
    """Checks that we have the information we need to generate the files
    Returns:
        Returns True if everything appears to be OK and False if there's a problem detected
    """
    # Check for missing definitions
    bad_values = []
    for one_attr in REQUIRED_VARIABLES:
        if not hasattr(algorithm_rgb, one_attr):
            bad_values.append(one_attr)
    if bad_values:
        print("The following variables are not globally defined in algorithm_rgb.py: %s" % ', '.join(bad_values))
        print("Please add the variables and try again")
        return False

    # Check for empty values
    for one_attr in REQUIRED_NOT_EMPTY_VARIABLES:
        if not getattr(algorithm_rgb, one_attr, None):
            bad_values.append(one_attr)
    if bad_values:
        print("The following variables are empty in algorithm_rgb.py: %s" % ', '.join(bad_values))
        print("Please assign values to the variables and try again")
        return False

    # Warnings
    for one_attr in PREFERRED_NOT_EMPTY_VARIABLES:
        if not hasattr(algorithm_rgb, one_attr) or not getattr(algorithm_rgb, one_attr, None):
            bad_values.append(one_attr)
    if bad_values:
        print("The following variables are missing or empty when it would be better to have them defined and filled in: %s" % \
              ','.join(bad_values))
        print("Continuing to generate files ...")

    return True


def generate_files() -> int:
    """Generated files needed to create a Docker image
    Return:
        Returns an integer representing success; zero indicates success and any other value represents failure.
    """
    try:
        for one_name in EMPTY_FILE_NAMES:
            open(one_name, 'a').close()
    except Exception as ex:
        print("Exception caught while attempting to create files: %s" % str(ex))
        print("Stopping file generation")
        return -1

    # Create the Dockerfile
    try:
        with open(DOCKERFILE_NAME, "w") as out_file:
            out_file.write('# automatically generated: %s\n' % datetime.datetime.now().isoformat())
            for line in DOCKERFILE_CONTENTS:
                if line.startswith('LABEL maintainer='):
                    out_file.write("LABEL maintainer=\"{0} <{1}>\"\n".format(algorithm_rgb.ALGORITHM_AUTHOR,
                                                                             algorithm_rgb.ALGORITHM_AUTHOR_EMAIL))
                else:
                    out_file.write("{0}\n".format(line))
    except Exception as ex:
        print("Exception caught while attempting to create Docker build file: %s" % str(ex))
        print("Stopping build file generation")
        return -2

    return 0


# Make the call to generate the files
if __name__ == "__main__":
    print('Confirming the environment')
    if check_environment():
        print('Configuring files')
        generate_files()
