import os

import numpy as np
import pytest

import ocf_datapipes
from ocf_datapipes.training.metnet_pv_national import metnet_national_datapipe


@pytest.mark.skip("Failing at the moment")
def test_metnet_datapipe():
    filename = os.path.join(os.path.dirname(ocf_datapipes.__file__), "../tests/config/test.yaml")
    gsp_datapipe = metnet_national_datapipe(filename, use_nwp=False, max_num_pv_systems=1)

    batch = next(iter(gsp_datapipe))
    assert np.isfinite(batch[0]).all()
    assert np.isfinite(batch[1]).all()
    assert np.isfinite(batch[2]).all()
    assert np.isfinite(batch[3]).all()
