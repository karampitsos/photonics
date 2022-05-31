from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from experiments import ZscanExperiment
from spectrum import Spectrum


class Sample:
    def __init__(self, name: str, refractive_index: float,
                 concentration: Optional[float] = None, solvent: Optional[Sample] = None,
                 width: Optional[float] = 1):

        self.name = name
        self.refractive_index = refractive_index
        self.concentration = concentration
        self.solvent = solvent
        self.width = width
        self.experiment: Optional[ZscanExperiment] = None
        self.spectra: Optional[Spectrum] = None
    
    def add_experiment(self, experiment: ZscanExperiment):
        self.experiment = experiment
    
    def add_spectra(self, spectra: Spectrum):
        self.spectra = spectra
    
    def calculate_absorption_from_spectra(self, wavelength):
        pass 
    
    def create_report(self):
        pass


@dataclass
class Laser:
    name: str
    pulse_duration: float
    wavalength: float