from __future__ import annotations
import os
from typing import List
import matplotlib.pyplot as plt
from typing import Optional
import csv


class Spectrum:

    def __init__(self, wavelengths: List[float], absorptions: List[float], sample):
        
        self.sample = sample
        self.sample.add_spectra(self)
        self.wavelengths = wavelengths
        self.absorptions = absorptions
        self.molar: List[float] = [abs/self.sample.concentration for abs in self.absorptions]
    
    def plot(self, show: bool=True, file: Optional[str] = None, dot: str = 'bo'):
        plt.plot(self.wavelengths, self.absorptions, dot[0], label=f'{self.sample.name} c={self.sample.concentration} mM')
        plt.xlim(300, 900)
        plt.ylim(0, 3)
        plt.xlabel('λ(nm)')
        plt.ylabel('absorbance')
        plt.legend(loc="upper left")
        if show:
            plt.show()
        if file:
            plt.savefig(file, dpi=600)

    def plot_molar(self, show: bool = True, file: Optional[str] = None):
        plt.plot(self.wavelengths, self.molar,label="{} c ={} mM".format(self.sample.name, self.sample.concentration))
        plt.xlim(300, 900)
        plt.ylim(0, 15)
        plt.xlabel('λ(nm)')
        plt.ylabel('& ε \times \mathregular{10^{-4}} (\mathregular{M^{-1}} \mathregular{cm^{-1}})$')
        if show:
            plt.show()
        if file:
            plt.savefig(file, dpi=600)

    @property
    def oscillator_strength(self):
        pass

    @classmethod
    def create_from_csv(cls, sample, file_dir: str, delimiter: str = '\t') -> Spectrum:
        wavelengths: List[float] = []
        absorptions: List[float] = []
        with open(file_dir, 'r') as file:
            csv_reader = csv.reader(file, delimiter=delimiter)
            for row in csv_reader:
                wavelengths.append(float(row[0]))
                absorptions.append(float(row[1]))

        spectrum = cls(
            sample=sample,
            wavelengths=wavelengths,
            absorptions=absorptions
            )
        
        return spectrum
            
    @classmethod
    def create_from_folder(cls, sample, folder_dir: str, delimiter: str = '\t') -> List[Spectrum]:
        spectrums: List[Spectrum] = []
        files = os.listdir(folder_dir)
        for file_dir in files:
            spectra = cls.create_from_csv(
                sample=sample,
                file_dir = os.path.join(folder_dir, file_dir),
                delimiter = delimiter)
            spectrums.append(spectra)
        
        return spectrums