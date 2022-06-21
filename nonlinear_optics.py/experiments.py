from typing import List, Optional
from fittings import linear_fitting
from zscan import Zscan
import scipy.optimize
#from sample import Sample
import matplotlib.pyplot as plt 
import numpy as np
import csv


class ZscanExperiment:

    def __init__(self, zscans: List[Zscan], sample, fitting: bool = True):
        
        self.sample = sample
        self.sample.add_experiment(self)
        self.zscans = zscans
        self.energies = [scan.energy for scan in self.zscans]
        self.dtpvs = [scan.dtpv for scan in self.zscans]
        self.qs = [scan.q for scan in self.zscans]
        self.realXi: Optional[float] = None
        self.ImaginaryXi: Optional[float] = None
        self.beta: Optional[float] = None
        self.slop: Optional[float] = None
        self.gamma: Optional[float] = None

        if fitting:
            self.fit_qs()
            self.fit_dtpv()

    def fit_qs(self):
        
        popt, pcov1 = scipy.optimize.curve_fit(
            linear_fitting,
            self.energies,
            self.qs,
            maxfev=1000000
            )
        
        self.beta = 100000*popt[0]/4.38 # 10-15 m/W
        self.imaginaryXi = 0.04*self.beta*self.sample.refractive_index**2

    def fit_dtpv(self):

        popt, pcov1 = scipy.optimize.curve_fit(
            linear_fitting,
            self.energies,
            self.dtpvs, 
            maxfev=1000000
            )
        
        self.slop = popt[0]
        self.gamma = 10000*popt[0] #10-21 m2/W
        self.realXi = 0.634*(self.sample.refractive_index**2)*self.gamma #10-16 esu

    def plot_dtpvs(self, show: bool = True, file: Optional[str] = None, dot: str = 'bo'):
        
        plt.plot(self.energies, self.dtpvs, dot, label=self.sample.name)
        plt.plot(np.linspace(0, np.max(self.energies)+100, num=200), self.slop*np.linspace(0, np.max(self.energies)+100, num=200), dot[0])
        plt.xlabel('Energy(nJ)')
        plt.ylabel('ΔΤp-v')
        plt.xlim(0, np.max(self.energies)+100)
        plt.ylim(0, np.max(self.dtpvs)+0.1)
        plt.legend(loc="upper left")
        if show:
            plt.show()
        if file:
            plt.savefig(file, dpi=600)

    @property
    def xi(self):
        return (self.realXi**2+self.imaginaryXi**2)**0.5
    
    def export_dtpvs_to_file(self, file: str):
        header = ['energy', 'dtpv']
        with open(file, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for i, energy in enumerate(self.energies):
                writer.writerow(energy, self.dtpvs[i])


class ZscanExperimentWithSolvent:
    pass