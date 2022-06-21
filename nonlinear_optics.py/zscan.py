from __future__ import annotations
import os
from typing import List, Optional
import numpy as np
import scipy.optimize
import csv
from fittings import open_fitting_function, divided_fitting_function
import matplotlib.pyplot as plt


class Zscan:
    """
    This class represent a scan of a zcan experiment
    energy: the energy of laser pulse in nJ
    z, closed_aperture, open_aperture, divided_aperture:
    are lists contains the experimental data.
    
    If the divided aperture doesn't it's calculated from 
    the open and close apertures.
    The fitting value is necessary if you want the paramateres
    of the expirement be calculated.

    """
    def __init__(self, 
                energy: float,
                closed_aperture: List[float],
                open_aperture: List[float],
                z: List[float],
                divided_aperture: Optional[List[float]] = None,
                fitting: bool = True
                ):
        
        self.energy = energy
        self.closed_aperture = closed_aperture
        self.open_aperture = open_aperture
        
        if divided_aperture:
            self.divided_aperture = divided_aperture
        else:
            self.divided_aperture = self.divided()
        
        self.z = z  
        self.dtpv: Optional[float] = None
        self.plato: Optional[float] = None
        self.estia: Optional[float] = None
        self.zo: Optional[float] = None
        self.df: Optional[float] = None

        self.q: Optional[float] = None
        self.open_estia: Optional[float] = None
        self.open_zo: Optional[float] = None
        self.open_plato: Optional[float] = None

        if fitting:
            self.fit_divided()
            self.fit_open()

    def divided(self):
        divided: List[float] = []
        for i, closed in enumerate(self.closed_aperture):
            point = closed/self.open_aperture[i]
            divided.append(point)
        return divided
    
    def plot_divided_row(self):
        pass

    def plot_divided(self, show=True, file: str = None):
        plt.plot(self.z-self.estia,self.divided_aperture/self.plato, "bo", label='divided')
        plt.plot(
            self.z-self.estia,
            divided_fitting_function(self.z, self.plato, self.df, self.estia, self.zo)/self.plato
            )
        plt.xlabel('z(mm)')
        plt.ylabel('Normalized Transmittance')
        plt.xlim(-4, 4)
        plt.ylim(0.75, 1.35)
        if show:
            plt.show()
        if file:
            plt.savefig(file,dpi=600)

    def plot_open_row(self):
        pass

    def plot_open(self, show: bool=True, file: Optional[str] = None):
        plt.plot(self.z-self.open_estia,self.open_aperture/self.open_plato, "r+", label='open')
        plt.plot(self.z-self.open_estia,
                 open_fitting_function(self.z,self.q, self.open_estia, self.open_zo, self.open_plato)/self.open_plato,
                 color='red')#,label='fit')
        plt.xlabel('z(mm)')
        plt.ylabel('Normalized Transmittance')
        plt.legend(loc="upper left")
        if show: 
            plt.show()
        if file:
            plt.savefig(file, dpi=600)
    
    def plot_scan(self, show: bool = True, file: Optional[str] = None):
        
        self.plot_open(show=False)
        self.plot_divided(show=False)
        if show: 
            plt.show()
        if file:
            plt.savefig(file, dpi=600)

    def fit_divided(self):
        
        popt, pcov1 = scipy.optimize.curve_fit(
            divided_fitting_function,
            self.z,
            self.divided_aperture,
            bounds=([0.3,-1,np.mean(self.z)-4,0.7],[1.5,1,np.mean(self.z)+4,1.5]),
            maxfev=1000000
            )
        
        self.plato = popt[0]
        self.df = popt[1]
        self.dtpv = 0.406*self.df/self.plato
        self.estia = popt[2]
        self.zo = popt[3]
        
        return popt, pcov1
    
    def fit_open(self):
        popt, pcov1 = scipy.optimize.curve_fit(
            open_fitting_function,
            self.z,
            self.open_aperture,
            bounds=([0,np.mean(self.z)-8,0.7,0.4],[1,np.mean(self.z)+8,1.5,1.5]),
            maxfev=1000000
            )
        
        self.q = popt[0]
        self.open_estia = popt[1]
        self.open_zo = popt[2]
        self.open_plato = popt[3]
        
        return popt, pcov1

    @classmethod
    def create_from_csv(cls, energy: float,  file_dir: str, delimiter: str = ',') -> Zscan:
        
        z = []
        closed_aperture = []
        open_aperture = []
        divided_aperture = []

        with open(file_dir) as file:
            csv_reader = csv.reader(file, delimiter=delimiter)
            for row in csv_reader:
                z.append(float(row[0]))
                closed_aperture.append(float(row[1]))
                open_aperture.append(float(row[2]))
                divided_aperture.append(float(row[3]))

        scan = cls(
            energy=energy,
            closed_aperture= closed_aperture,
            open_aperture=open_aperture,
            z=z
            )
        
        return scan

    @classmethod
    def create_from_folder(cls, energy: float, folder_dir: str, delimiter: str = ',') -> List[Zscan]:
        scans: List[Zscan] = []
        files = os.listdir(folder_dir)
        for file_dir in files:
            scan = cls.create_from_csv(energy, os.path.join(folder_dir, file_dir), delimiter=delimiter)
            scans.append(scan)
        
        return scans
    
    @classmethod
    def create_from_folders(cls, folder_dir: str, delimiter: str = ',') -> List[Zscan]:
        scans: List[Zscan] = []
        folders = os.listdir(folder_dir)
        for folder in folders:
            scans_to_add = cls.create_from_folder(
                energy = float(folder),
                folder_dir=os.path.join(folder_dir, folder),
                delimiter=delimiter
                )
            scans.extend(scans_to_add)
        
        return scans