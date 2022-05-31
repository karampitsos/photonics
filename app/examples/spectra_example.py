from typing import List
from sample import Sample, Laser
from spectrum import Spectrum
from zscan import Zscan


toluene = Sample(name='toluene', concentration=0.2, refractive_index=1.4)
spectrum = Spectrum.create_from_csv(
    sample=toluene,
    file_dir='/home/nikos/Documents/photonics/analysis/f10032020/spectra/4_0_25_mM/060320(03).csv',
    delimiter='\t'
    )

spectrum.plot()