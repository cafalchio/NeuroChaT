#Script to analyse before and after stimulation
import os
from copy import copy
from collections import OrderedDict
import csv

import numpy as np
import matplotlib.pyplot as plt

from neurochat.nc_event import NEvent
from neurochat.nc_data import NData
from neurochat.nc_datacontainer import NDataContainer
from neurochat.nc_utils import log_exception, make_dir_if_not_exists


def main(dir, bin_size, bin_bound):
    container = NDataContainer(load_on_fly=True)
    container.add_axona_files_from_dir(dir, recursive=True)
    container.setup()
    print(container.string_repr(True))
    event = NEvent()
    last_stm_name = None
    dict_list = []

    for i in range(len(container)):
        try:
            result_dict = OrderedDict()
            data_index, _ = container._index_to_data_pos(i)
            stm_name = container.get_file_dict("STM")[data_index][0]
            data = container[i]
            
            # Add extra keys
            spike_file = data.spike.get_filename()
            spike_dir = os.path.dirname(spike_file)
            spike_name = os.path.basename(spike_file)
            spike_name_only, spike_ext = os.path.splitext(
                spike_name)
            spike_ext = spike_ext[1:]
            result_dict["Dir"] = spike_dir
            result_dict["Name"] = spike_name_only
            result_dict["Tet"] = int(spike_ext)
            result_dict["Unit"] = data.spike.get_unit_no()

            # Do analysis  
            if last_stm_name != stm_name:
                event.load(stm_name, 'Axona')
                last_stm_name = stm_name
            graph_data = data.psth(
                event.get_timestamp(), bins=bin_size, bound=bin_bound)
            spike_count = data.get_unit_spikes_count()
            result_dict["Num_Spikes"] = spike_count

            # Bin renaming
            for (b, v) in zip(graph_data["all_bins"][:-1], graph_data["psth"]):
                result_dict[str(b)] = v
            dict_list.append(result_dict)
            
            # Do plotting
            name = (
                spike_name_only + "_" + spike_ext + 
                "_" + str(result_dict["Unit"]) + ".png")
            plot_name = os.path.join(dir, "psth_results", name)
            make_dir_if_not_exists(plot_name)
            plot_psth(graph_data, plot_name)
            print("Saved psth to {}".format(plot_name))

        except Exception as e:
            log_exception(
                e, "During stimulation batch at {}".format(i))
            dict_list.append(result_dict)

    fname = os.path.join(dir, "psth_results", "psth.csv")
    save_results_to_csv(fname, dict_list)
    print("Saved results to {}".format(fname))

def plot_psth(graph_data, name, dpi=75):
    line_width = 0
    width = np.mean(np.diff(graph_data["all_bins"]))
    plt.bar(
        graph_data["bins"], graph_data["psth"],
        align="edge", width=width, linewidth=line_width, color='black',
        edgecolor='black', rasterized=True)
    plt.xlabel('Time relative to stimulus (ms)')
    plt.ylabel('Spike counts')
    plt.savefig(name, dpi=dpi)
    plt.close()


def save_results_to_csv(filename, in_dicts):
    """Save a dictionary to a csv"""
    # find the dict with the most keys
    max_key = []
    for in_dict in in_dicts:
        names = in_dicts[0].keys()
        if len(names) > len(max_key):
            max_key = names

    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=names)
            writer.writeheader()
            for in_dict in in_dicts:
                writer.writerow(in_dict)

    except Exception as e:
        log_exception(e, "When {} saving to csv".format(filename))   


if __name__ == "__main__":
    dir = r"/home/cafalchio/Desktop/6s_data_and_results/Data"
    bin_size = 8
    bin_bound = [-300, 150]
    main(dir, bin_size, bin_bound)

