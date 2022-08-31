import logging
from typing import Optional, Union

import numpy as np
import xarray as xr
from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

logger = logging.getLogger(__name__)


@functional_datapipe("check_greater_than_or_equal_to")
class CheckGreaterThanOrEqualToIterDataPipe(IterDataPipe):
    def __init__(
        self, source_datapipe: IterDataPipe, min_value: int, dataset_name: Optional[str] = None
    ):
        self.source_datapipe = source_datapipe
        self.min_value = min_value
        self.dataset_name = dataset_name

    def __iter__(self):
        for xr_data in self.source_datapipe:
            if self.dataset_name is not None:
                check_dataset_greater_than_or_equal_to(
                    xr_data[self.dataset_name], min_value=self.min_value
                )
            else:
                check_dataset_greater_than_or_equal_to(xr_data, min_value=self.min_value)
            yield xr_data


@functional_datapipe("check_less_than_or_equal_to")
class CheckLessThanOrEqualToIterDataPipe(IterDataPipe):
    def __init__(
        self, source_datapipe: IterDataPipe, max_value: int, dataset_name: Optional[str] = None
    ):
        self.source_datapipe = source_datapipe
        self.max_value = max_value
        self.dataset_name = dataset_name

    def __iter__(self):
        for xr_data in self.source_datapipe:
            if self.dataset_name is not None:
                check_dataset_less_than_or_equal_to(
                    xr_data[self.dataset_name], max_value=self.max_value
                )
            else:
                check_dataset_less_than_or_equal_to(xr_data, max_value=self.max_value)
            yield xr_data


@functional_datapipe("check_not_equal_to")
class CheckNotEqualToIterDataPipe(IterDataPipe):
    def __init__(
        self,
        source_datapipe: IterDataPipe,
        value: int,
        dataset_name: Optional[str] = None,
        raise_error: bool = true,
    ):
        self.source_datapipe = source_datapipe
        self.value = value
        self.dataset_name = dataset_name
        self.raise_error = raise_error

    def __iter__(self):
        for xr_data in self.source_datapipe:
            if self.dataset_name is not None:
                check_dataset_not_equal(
                    xr_data[self.dataset_name], value=self.value, raise_error=self.raise_error
                )
            else:
                check_dataset_not_equal(xr_data, value=self.value, raise_error=self.raise_error)
            yield xr_data


def check_dataset_greater_than_or_equal_to(data: xr.Dataset, min_value: int):
    """Check data is greater than a certain value"""
    if (data < min_value).any():
        message = f"Some data values are less than {min_value}. "
        message += f"The minimum value is {data.min()}. "
        raise Exception(message)


def check_dataset_less_than_or_equal_to(data: xr.Dataset, max_value: int):
    """Check data is less than a certain value"""
    if (data > max_value).any():
        message = f"Some data values are more than {max_value}"
        message += f"The maximum value  is {data.max()}. "
        raise Exception(message)


def check_dataset_not_equal(data: xr.Dataset, value: int, raise_error: bool = True):
    """Check data is not equal than a certain value"""
    if np.isclose(data, value).any():
        message = f"Some data values are equal to {value}"
        if raise_error:
            logger.error(message)
            raise Exception(message)
        else:
            logger.warning(message)
