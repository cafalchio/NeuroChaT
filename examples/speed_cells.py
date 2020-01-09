#Script to analyse before and after stimulation
import os

import numpy as np
import matplotlib.pyplot as plt

from neurochat.nc_data import NData
from neurochat.nc_datacontainer import NDataContainer
from neurochat.nc_utils import log_exception, make_dir_if_not_exists
from neurochat import nc_plot

def main(dir):
    container = NDataContainer(load_on_fly=True)
    container.add_axona_files_from_dir(dir, recursive=True)
    container.setup()
    print(container.string_repr(True))

    for i in range(len(container)):
        try:
            data = container[i]        
            graph_data = data.speed(range = [4, 100], binsize= 1, update=True)
            fig = nc_plot.speed(graph_data)
            plt.savefig('/home/cafalchio/Desktop/MS/LS7'+ str(i) + '.png', dpi=100)
            plt.close(fig)

        except Exception as e:
            log_exception(
                e, "During stimulation batch at {}".format(i))

   
if __name__ == "__main__":
    dir = r"/home/cafalchio/Desktop/MS/LS7/data"
    # speeds = [4, 100]
    main(dir)

