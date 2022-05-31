from typing import List
from sample import Sample, Laser
from zscan import Zscan


scans: List[Zscan] = Zscan.create_from_folders(
                            folder_dir='/home/nikos/Documents/photonics/analysis/f10032020/scans/toluene/'
                            )

for scan in scans:
    scan.plot_scan()