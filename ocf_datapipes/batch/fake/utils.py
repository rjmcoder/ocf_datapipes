""" Utils Functions to for fake data """
from typing import List

import numpy as np
import pandas as pd
import xarray as xr


def make_t0_datetimes_utc(batch_size, temporally_align_examples: bool = False):
    """
    Make list of t0 datetimes

    Args:
        batch_size: the batch size
        temporally_align_examples: option to align examples (within the batch) in time

    Returns: pandas index of t0 datetimes
    """

    all_datetimes = pd.date_range("2023-01-01", "2023-02-01", freq="5T")

    if temporally_align_examples:
        t0_datetimes_utc = list(np.random.choice(all_datetimes, size=1)) * batch_size
    else:
        if len(all_datetimes) >= batch_size:
            replace = False
        else:
            # there are not enought data points,
            # so some examples will have the same datetime
            replace = True

        t0_datetimes_utc = np.random.choice(all_datetimes, batch_size, replace=replace)
    # np.random.choice turns the pd.Timestamp objects into datetime.datetime objects.

    t0_datetimes_utc = pd.to_datetime(t0_datetimes_utc)

    # TODO make test repeatable using numpy generator
    # https://github.com/openclimatefix/nowcasting_dataset/issues/594

    return t0_datetimes_utc
