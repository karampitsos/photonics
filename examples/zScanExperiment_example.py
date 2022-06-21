from zscan import Zscan
from sample import Sample
from experiments import ZscanExperiment
from typing import List


toluene = Sample(name='toluene', concentration=0.2, refractive_index=1.4)
scans: List[Zscan] = Zscan.create_from_folders(
                            sample=toluene,
                            folder_dir='/home/nikos/Documents/photonics/analysis/f10032020/scans/toluene/'
                            )

for scan in scans:
    scan.fit_divided()
    scan.fit_open()

experiment = ZscanExperiment(scans, toluene)

experiment.fit_dtpv()
experiment.plot_dtpvs()