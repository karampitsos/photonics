import pytest
from nonlinear_optics import Zscan
from nonlinear_optics import Sample
from typing import List
from dataclasses import dataclass
import csv


@dataclass
class Scan:
    z: List[float]
    close: List[float]
    opened: List[float]
    divided: List[float]

@pytest.fixture
def apertures() -> Scan:
    z = []
    close = []
    opened = []
    divided = []

    with open('./input/f10032020/scans/toluene/125/26.csv', 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            z.append(round(float(row[0]), 3))
            close.append(round(float(row[1]), 3))
            opened.append(round(float(row[2]), 3))
            divided.append(round(float(row[3]), 3))
    
    return Scan(z, close, opened, divided)


@pytest.fixture
def scan() -> Zscan:
    scan = Zscan.create_from_csv(
        energy = 125,
        file_dir='input/f10032020/scans/toluene/125/26.csv',
        delimiter=','
        )
    return scan


def test_create_from_csv(apertures: Scan):

    scan = Zscan.create_from_csv(
        energy = 125,
        file_dir='input/f10032020/scans/toluene/125/26.csv',
        delimiter=','
        )

    assert scan.dtpv == 0.126
    assert scan.plato == 0.954 
    assert scan.estia == -2.518
    assert scan.zo == 0.97
    assert scan.q == 0.032
    assert scan.open_aperture == apertures.opened
    assert scan.closed_aperture == apertures.close
    assert scan.z == apertures.z
    assert scan.divided_aperture == apertures.divided


def test_create_from_folder():
    
    scans = Zscan.create_from_folder(
        energy = 125,
        folder_dir='./input/f10032020/scans/toluene/125/',
        delimiter=','
        )

    assert len(scans) == 2

def test_create_from_folders():

    scans: List[Zscan] = Zscan.create_from_folders(
        folder_dir='./input/f10032020/scans/toluene/',
        delimiter=','
    )

    assert len(scans) == 8
    assert [scan.energy for scan in scans] == [330.0, 330.0, 240.0, 125.0, 125.0, 200.0, 200.0, 200.0]