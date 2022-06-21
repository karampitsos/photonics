# nonlinear-optics

Nonlinear-optics is a user-friendly Python library for dealing with the analysis of nonlinear optics experimental results. Currently supports only Zscan measurements.
In order to analyze the experimental results of a nonlinear optics experiment you have to repeat yourself or use a proprietary software. This library aims to help
scientist to automate the analysis and save time to concentrate to their science.

## Instalation
Use the package manager pip to install nonlinear-optics.

```bash

pip install nonlinear-optics

```

## Basic Usage
In order to read a Zscan from a csv file you can use this factory.

```python

from nonlinear_optics import Zscan
from nonlinear_optics import Sample
from typing import List

scan = Zscan.create_from_csv(energy=100, file_dir='file.csv', delimiter=',')

```

In order to read multiple Zscans from a folder which contain csv files you can use the from_folder factory. You have to pass a sample instance to point the zscans.

```python

sample = Sample(name='toluene', concentration=0.2, refractive_index=1.3)
scans: List[scans] = Zscan.create_from_folder(sample = sample, 'folder_dir')

```