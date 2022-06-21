import pytest
from sample import Sample, Laser
from zscan import Zscan
from typing import List

@pytest.fixture
def sample() -> Sample:
    sample = Sample(
        name='toluene',
        concentration=0.2,
        refractive_index=1.3
    )

    return sample

@pytest.fixture
def laser() -> Laser:
    laser = Laser(
        name='tridentx',
        pulse_duration=100,
        wavalength=800
    )
    
    return laser

@pytest.fixture
def scan() -> Zscan:
    scan = Zscan.create_from_csv(
        sample = sample,
        energy = 125,
        file_dir='/home/nikos/Documents/photonics/analysis/f10032020/scans/toluene/125/26.csv',
        delimiter=','
        )
    return scan

def test_create_from_csv():

    scan = Zscan.create_from_csv(
        energy = 125,
        file_dir='/home/nikos/Documents/photonics/analysis/f10032020/scans/toluene/125/26.csv',
        delimiter=','
        )


def test_create_from_folder(sample):
    
    scans = Zscan.create_from_folder(
        energy = 125,
        folder_dir='/home/nikos/Documents/photonics/analysis/f10032020/scans/toluene/125/',
        delimiter=','
        )

    assert len(scans) == 2

def test_create_from_folders(sample):

    scans = Zscan.create_from_folders(
        sample=sample,
        folder_dir='/home/nikos/Documents/photonics/analysis/f10032020/scans/toluene/',
        delimiter=','
    )

    assert len(scans) == 8

def test_fit_divided(scan):
    scan.fit_divided()
    assert scan.dtpv == None
    assert scan.plato == None
    assert scan.estia == None
    assert scan.zo == None
    assert scan.df == None
    

    
