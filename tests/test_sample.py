import pytest
from nonlinear_optics import Sample

@pytest.fixture
def sample() -> Sample:
    sample = Sample(
        name='toluene',
        concentration=0.2,
        refractive_index=1.3
    )

    return sample

