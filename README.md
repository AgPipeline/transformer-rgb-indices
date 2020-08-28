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
