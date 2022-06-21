from typing import List
from nonlinear_optics.sample import Sample, Laser
from nonlinear_optics.zscan import Zscan


scans: List[Zscan] = Zscan.create_from_folders(
                            folder_dir='/home/nikos/Documents/photonics/analysis/f10032020/scans/toluene/'
                            )

for scan in scans:
    scan.plot_scan()