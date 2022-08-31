from torchdata.datapipes.iter import IterDataPipe
from torchdata.datapipes import functional_datapipe
from ocf_datapipes.utils.consts import BatchKey, NumpyBatch
import numpy as np
import xarray as xr

@functional_datapipe("ensure_n_nwp_variables")
class EnsureNNWPVariables(IterDataPipe):
    def __init__(self, source_datapipe: IterDataPipe, num_variables: int):
        self.source_datapipe = source_datapipe
        self.num_variables = num_variables

    def __iter__(self):
        for np_batch in self.source_datapipe:
            num_tiles = int(np.ceil(self.num_variables / np_batch[BatchKey.nwp_channel_names]))
            channel_names = np.tile(np_batch[BatchKey.nwp_channel_names], num_tiles)[:self.num_variables]
            data = np.tile(np_batch[BatchKey.nwp], (1,1,num_tiles,1,1))[:,:,:self.num_variables,:,:]
            np_batch[BatchKey.nwp] = data
            np_batch[BatchKey.nwp_channel_names] = channel_names
            yield np_batch
