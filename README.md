# Greenness Transformer
Provides a variety of calculations using RGB indices in order to monitor crop/plant
growth and health, taking into account variations between lighting and cameras

## Authors
Chris Schnaufer, University of Arizona, Tucson, AZ
Jacob van der Leeuw: University of Arizona, Tucson, AZ

## Overview
The Greenness Transformer is meant to provide several calculations on image rgb data in order to get an idea of plant growth and
health. A more in-depth explanation can be found at [this link](https://docs.google.com/document/d/1cAm5w1Bs6dB1SHgf-HVmwwbebLhbZMUvTkXLtas_-xI/edit)

## Algorithm Description
This transformer provides calculations using the red, green, and blue values for pixels in an image ranging from calculating the
percentage of an image which is green to normalized difference calculations and more

## References

### excess_greenness_index: 
Sonnentag, O. et. al, 2012

Named ‘2G_RBi’ in Richardson 2007

### green_leaf_index:

### cive: 
Kataoka et. al, 2003

### normalized_difference_index: 
Perez et al., 2000 (links to original paper although equation was slightly modified)

### excess_red
Meyer et al., 1998 (links to closely related paper)

### exgr: 
Neto et. al, 2004

### combined_indices_1:
Guijarro et al., 2011

### combined_indices_2: 
Guerrerro et al., 2012

### vegetative_index: 
Hague et al., 2006

### ngrdi:
Hunt et. al, 2005

### percent_green:
Richardson et al 2007