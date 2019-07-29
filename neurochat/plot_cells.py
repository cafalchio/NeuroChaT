import os
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
sys.path.insert(1, r'C:\Users\maolivei\neuro_sean\NeuroChaT')

import neurochat.nc_plot as nc_plot
from neurochat.nc_datacontainer import NDataContainer
from neurochat.nc_containeranalysis import place_cell_summary

container =NDataContainer(load_on_fly=True)
container.add_axona_files_from_dir(r"D:\Cafalchio\data\LCA3\remapping")
container.setup()
place_cell_summary(container, dpi=100)