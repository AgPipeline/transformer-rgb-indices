# Greenness Indices

This algorithm computes a series of indices from RGB cameras. These can be used to assess crop and plant
growth and health, taking into account variations between lighting and cameras.


## Authors

- Clairessa Brown
- Chris Schnaufer
- Jacob van der Leeuw
- David LeBauer 

## Overview

The Greenness transformer computes several indices from RGB image data in order to get an idea of plant growth and
health. 

Using RGB images from digital cameras can be used to assess plant growth and health digital camera images. One challenge is taking consistent measurements from images that may be taken under different lighting, with different cameras, or with different settings. Most methods below focus on correcting for different light (illumination) conditions.

_Note:_ These are intended for use on images that have had soil removed (see the soil mask transformer).

## Algorithm Description

This transformer provides calculations using the red, green, and blue values for each pixel. 

| Formula                                                      | What It Accounts for                                                                                              | Limitations                        | How to Use it                                                                                   | Misc.                                                                                                    | Citation(s)                                                                          |
|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|-------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Green chromatic coordinate (Gcc)  Gcc = G/(R+G+B)            | Green pigmentation in vegetation                                                                                  | Different color leaves, background like soil       | Take mean of green pixels (digital numbers) for each ROI and then apply Gcc data transformation | Calculate the 90th percentile method* to minimize variation between different illuminations | Woebbecke, D.M et. al, 1995;  Gillespie A., et al, 1987                              |
| Excess greenness index (ExG) ExG = 2G-(R+B)                  | Minimize variation between different illuminations (light quality) and enhance detection of plants                | Can’t compare absolute values of different cameras | Calculate average of digital numbers across ROI and then apply data transformation              |  Named ‘2G_RBi’ in Richardson 2007| Sonnentag, O. et. al, 2012                         |
| Green Leaf Index (GLI) GLI = (2×G-R-B)/ (2×G+R+B)            |                                                                                                                   |                                                    |                                                                                                 |                                                                                                          |                                                                                      |
| CIVE = 0.441R-0.811G+0.385B+18.78745                         | Can measure crop growth status                                                                                    |                                                    |                                                                                                 |                                                                                                          | Kataoka et. al, 2003                                                                 |
| Normalized difference index (NDI)  NDI = 128×((G-R)/(G+R))+1 |                                                                                                                   |                                                    |                                                                                                 |                                                                                                          | Perez et al., 2000 (links to original paper although equation was slightly modified) |
| Excess Red ExR = 1.3R-G                                      | Illumination issues that make it difficult to tease apart redness from crops/leaves from soil or camera artifacts |                                                    |                                                                                                 |                                                                                                          | Meyer et al., 1998 (links to closely related paper)                                  |
| ExGR = ExG-ExR                                               | Minimize variation between different illuminations                                                                |                                                    |                                                                                                 |                                                                                                          | Neto et. al, 2004                                                                    |
| Combined Indices 1 = ExG + CIVE                              |                                                                                                                   |                                                    |                                                                                                 |                                                                                                          | Guijarro et al., 2011                                                                |
| Combined Indices 2 = 0.36ExG + 0.47CIVE + 0.17VEG            |                                                                                                                   |                                                    |                                                                                                 |                                                                                                          | Guerrerro et al., 2012                                                               |
| Normalized Green-Red Difference (NGRDI) NGRDI = g-r/g+r      | Can measure crop growth status                                                                                    |                                                    |                                                                                                 |                                                                                                          | Hunt et. al, 2005                                                                    |
| Vegetative Index (VEG) VEG = g/(r<sup>a</sup>b<sup>1-a</sup>); a = 0.667           | Minimize illumination differences between images                                                                  |                                                    |                                                                                                 |                                                                                                          | Hague et al., 2006                                                                   |
| % Green = G/(R+G+B)                                          |                                                                                                                   |                                                    |                                                                                                 |                                                                                                          | Richardson et al 2007                                                                |
<sup>*</sup>90th percentile method for time series: Take the mean of all values within the 90th percentile of a three-day window and have that value be the middle day's value to reduce illumination variation on different days.

## References

Woebbecke, David M., et al. "Color indices for weed identification under various soil, residue, and lighting conditions." Transactions of the ASAE 38.1 (1995): 259-269. https://doi.org/10.13031/2013.27838

Gillespie, Alan R., Anne B. Kahle, and Richard E. Walker. "Color enhancement of highly correlated images. II. Channel ratio and “chromaticity” transformation techniques." Remote Sensing of Environment 22, no. 3 (1987): 343-365. 
https://doi.org/10.1016/0034-4257(87)90088-5

Sonnentag, Oliver, Koen Hufkens, Cory Teshera-Sterne, Adam M. Young, Mark Friedl, Bobby H. Braswell, Thomas Milliman, John O’Keefe, and Andrew D. Richardson. "Digital repeat photography for phenological research in forest ecosystems." Agricultural and Forest Meteorology 152 (2012): 159-177. https://doi.org/10.1016/j.agrformet.2011.09.009

Kataoka, T., Kaneko, T., Okamoto, H., & Hata, S. (2003, July). Crop growth estimation system using machine vision. In Proceedings 2003 IEEE/ASME International Conference on Advanced Intelligent Mechatronics (AIM 2003) (Vol. 2, pp. b1079-b1083). IEEE. https://doi.org/10.1109/AIM.2003.1225492

Perez, A. J., F. Lopez, J. V. Benlloch, and Svend Christensen. "Colour and shape analysis techniques for weed detection in cereal fields." Computers and electronics in agriculture 25, no. 3 (2000): 197-212. 
https://doi.org/10.1016/S0168-1699(99)00068-X

Meyer, George E. ["Machine vision identification of plants."](https://pdfs.semanticscholar.org/189a/08841373be95d474394a39f2693a7813b2d7.pdf) In Recent trends for enhancing the diversity and quality of soybean products. IntechOpen, 2011. https://doi.org/10.5772/18690

Neto, Joao Camargo. A combined statistical-soft computing approach for classification and mapping weed species in minimum-tillage systems. The University of Nebraska-Lincoln, 2004.https://digitalcommons.unl.edu/dissertations/AAI3147135

Guijarro, Marıa, Gonzalo Pajares, Isabel Riomoros, P. J. Herrera, X. P. Burgos-Artizzu, and Angela Ribeiro. "Automatic segmentation of relevant textures in agricultural images." Computers and Electronics in Agriculture 75, no. 1 (2011): 75-83. https://doi.org/10.1016/j.compag.2010.09.013

Hunt, E. Raymond, Michel Cavigelli, Craig ST Daughtry, James E. Mcmurtrey, and Charles L. Walthall. "Evaluation of digital photography from model aircraft for remote sensing of crop biomass and nitrogen status." Precision Agriculture 6, no. 4 (2005): 359-378. https://doi.org/10.1007/s11119-005-2324-5

Hague, T., N. D. Tillett, and H. Wheeler. "Automated crop and weed monitoring in widely spaced cereals." Precision Agriculture 7, no. 1 (2006): 21-32. https://doi.org/10.1007/s11119-005-6787-1

Richardson, Andrew D., Julian P. Jenkins, Bobby H. Braswell, David Y. Hollinger, Scott V. Ollinger, and Marie-Louise Smith. "Use of digital webcam images to track spring green-up in a deciduous broadleaf forest." Oecologia 152, no. 2 (2007): 323-334. https://doi.org/10.1007/s00442-006-0657-z

### Sample Docker Command line

Below is a sample command line that shows how the soil mask Docker image could be run.
An explanation of the command line options used follows.
Be sure to read up on the [docker run](https://docs.docker.com/engine/reference/run/) command line for more information.

```docker run --rm --mount "src=${PWD}/test_data,target=/mnt,type=bind" agdrone/transformer-greenness:1.0 --working_space "/mnt" --metadata "/mnt/experiment.yaml" "/mnt/rgb_1_2_E.tif" ```

This example command line assumes the source files are located in the `test_data` folder off the current folder.
The name of the image to run is `agdrone/transformer-greenness:1.0`.

We are using the same folder for the source files and the output files.
By using multiple `--mount` options, the source and output files can be separated.

**Docker commands** \
Everything between 'docker' and the name of the image are docker commands.

- `run` indicates we want to run an image
- `--rm` automatically delete the image instance after it's run
- `--mount "src=${PWD}/test_data,target=/mnt,type=bind"` mounts the `${PWD}/test_data` folder to the `/mnt` folder of the running image

We mount the `${PWD}/test_data` folder to the running image to make files available to the software in the image.

**Image's commands** \
The command line parameters after the image name are passed to the software inside the image.
Note that the paths provided are relative to the running image (see the --mount option specified above).

- `--working_space "/mnt"` specifies the folder to use as a workspace
- `--metadata "/mnt/experiment.yaml"` is the name of the source metadata
- `"/mnt/rgb_1_2_E.tif"` is the name of the image to calculate greenness on

## Acceptance Testing

There are automated test suites that are run via [GitHub Actions](https://docs.github.com/en/actions).
In this section we provide details on these tests so that they can be run locally as well.

These tests are run when a [Pull Request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests) or [push](https://docs.github.com/en/github/using-git/pushing-commits-to-a-remote-repository) occurs on the `develop` or `master` branches.
There may be other instances when these tests are automatically run, but these are considered the mandatory events and branches.

### PyLint and PyTest

These tests are run against any Python scripts that are in the repository.

[PyLint](https://www.pylint.org/) is used to both check that Python code conforms to the recommended coding style, and checks for syntax errors.
The default behavior of PyLint is modified by the `pylint.rc` file in the [Organization-info](https://github.com/AgPipeline/Organization-info) repository.
Please also refer to our [Coding Standards](https://github.com/AgPipeline/Organization-info#python) for information on how we use [pylint](https://www.pylint.org/).

The following command can be used to fetch the `pylint.rc` file:
```bash
wget https://raw.githubusercontent.com/AgPipeline/Organization-info/master/pylint.rc
```

Assuming the `pylint.rc` file is in the current folder, the following command can be used against the `algorithm_rgb.py` file:
```bash
# Assumes Python3.7+ is default Python version
python -m pylint --rcfile ./pylint.rc algorithm_rgb.py
``` 

In the `tests` folder there are testing scripts; their supporting files are in the `test_data` folder.
The tests are designed to be run with [Pytest](https://docs.pytest.org/en/stable/).
When running the tests, the root of the repository is expected to be the starting directory.

The command line for running the tests is as follows:
```bash
# Assumes Python3.7+ is default Python version
python -m pytest -rpP
```

If [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) is installed, it can be used to generate a code coverage report as part of running PyTest.
The code coverage report shows how much of the code has been tested; it doesn't indicate **how well** that code has been tested.
The modified PyTest command line including coverage is:
```bash
# Assumes Python3.7+ is default Python version
python -m pytest --cov=. -rpP 
```

### Docker Testing

The Docker testing Workflow replicate the examples in this document to ensure they continue to work.
