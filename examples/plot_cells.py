"""Plot all spatial cells in an Axona directory."""
from neurochat.nc_datacontainer import NDataContainer
import neurochat.nc_containeranalysis as nca


def main(dir):
    container = NDataContainer(load_on_fly=True)
    container.add_axona_files_from_dir(dir, recursive=True)
    container.setup()
    print(container.string_repr(True))
    nca.place_cell_summary(
        container, dpi=200, out_dirname="nc_spat_plots", 
        filter_place_cells=True, filter_low_freq=True,
        num_shuffles=300)


if __name__ == "__main__":
    dir = r'/media/cafalchio/ATN_CA1_backup/ATNx_CA1_1'
    main(dir)

if __name__ == "__main__":
    dir = r'/media/cafalchio/ATN_CA1_backup/ATNx_CA1_2'
    main(dir)

if __name__ == "__main__":
    dir = r'/media/cafalchio/ATN_CA1_backup/ATNx_CA1_3'
    main(dir)