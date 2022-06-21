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
### Zscan
In order to parse a Zscan measurement from a csv file you can use the from_csv factory. The csv file must have the column of position z in milimeters and the columns of open and closed apertures with this order. If there are a fourth column that column must correspond to divided otherwise the divided is calculates from the division of open and close apertures.

```python
from nolinear_optics import Zscan

scan = Zscan.create_from_csv(file='file.csv', energy=100)
```

You can retrieve the raw data and use it as you wish.

```python
z: List[float] = scan.z
open: List[float] = scan.open_aperture
closed: List[float] = scan.closed_aperture
divided: List[float] = scan.divided_aperture
```

On the scan instance initialazation the raw data are fitted and the fitting parameteres can be retrieved as class attributes.
```python
# the focus position.
focus = scan.focus
# the z0 coefficient.
z0 = scan.zo
# the ΔΦ of the divided.
df = scan.df
# the q of the open.
q = scan.q
```
In order to plot the normalized and fitted scan use the plot functions of the class. The default value of the show attribute is true and the default value of the file is None. In order to save the image you have to overwrite the file value. If you don't want the matoplotlib pyplot to show the plot you can deactivate it by overwriting the show value to false. 
```python
scan.plot_open(show=True)
scan.plot_divided(show=True)

scan.plot_open(show=False, file='output.png')
scan.plot_divided(show=False, file='output2.png')
```

### Experiment
In order to read multiple Zscans from a folder which contain csv files you can use the from_folders factory.

```python
from nolinear_optics import Zscan

scans: List[scans] = Zscan.create_from_folders('folder_dir')

```

The sample

```python
from nonlinear_optics import Sample

sample = Sample(name='example', concetration=0.3, refractive_index=1.4)

```

The experiment

```python
from nonlinear_optics import ZscanExperiment, Zscan, Sample

scans: List[scans] = Zscan.create_from_folder('folder_dir')
sample = Sample(name='example', concetration=0.3, refractive_index=1.4)
experiment = ZscanExperiment(scans, sample)
```

The report

```python
from nonlinear_optics import Report
from docx import Document as Document_constructor

report = Report([sample, sample_two, sample_three], doc=document)
report.add_scans()
report.plot_spectra(documented=True)
report.plot_dtpvs(documented=True)
report.create_table()
document.save('file.docx')
```
