from typing import List
from sample import Sample
from sample import ZscanExperiment
from sample import Spectrum
from zscan import Zscan
from reports import Report
from docx import Document as Document_constructor


toluene = Sample(name='toluene', concentration=0.2, refractive_index=1.4)
toluene_scans: List[Zscan] = Zscan.create_from_folders(folder_dir='./input/f10032020/scans/toluene/')
experiment_toluene = ZscanExperiment(toluene_scans, toluene)

sample = Sample(name='4', concentration=0.5, refractive_index=1.4)
sample_scans: List[Zscan] = Zscan.create_from_folders(folder_dir='./input/f10032020/scans/z4_0_5_mM/')
experiment_sample = ZscanExperiment(sample_scans, sample)

sample_two = Sample(name='10', concentration=0.1, refractive_index=1.4)
sample_two_scans: List[Zscan] = Zscan.create_from_folders(folder_dir='/home/nikos/Documents/photonics/analysis/app/input/f10032020/scans/z10_0_1_mM/')
experiment_sample_two = ZscanExperiment(sample_two_scans, sample_two)

sample_three = Sample(name='10', concentration=0.21, refractive_index=1.4)
sample_three_scans: List[Zscan] = Zscan.create_from_folders(folder_dir='/home/nikos/Documents/photonics/analysis/app/input/f10032020/scans/z10_0_21_mM/')
experiment_sample_three = ZscanExperiment(sample_three_scans, sample_three)

spectrum = Spectrum.create_from_csv(
    sample=sample,
    file_dir='/home/nikos/Documents/photonics/analysis/app/input/f10032020/spectra/4_0_25_mM/060320(03).csv',
    delimiter='\t'
    )

spectrum_two = Spectrum.create_from_csv(
    sample=sample_two,
    file_dir='/home/nikos/Documents/photonics/analysis/app/input/f10032020/spectra/10_0_1_mM/040320(02).csv',
    delimiter='\t'
    )

spectrum_three = Spectrum.create_from_csv(
    sample=sample_three,
    file_dir='/home/nikos/Documents/photonics/analysis/app/input/f10032020/spectra/10_0_21_mM/060320(04).csv',
    delimiter='\t'
    )

document = Document_constructor()
report = Report([toluene, sample, sample_two, sample_three], doc=document)
report.add_scans()
report.plot_spectra(documented=True)
report.plot_dtpvs(documented=True)
report.create_table()

document.save('./output/files/test.docx')