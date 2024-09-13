# -*- coding: utf-8 -*-
# @Author: eerstone
# @Date:   2023-12-07 10:30:35
# @Last Modified by:   eerstone
# @Last Modified time: 2024-09-13 21:46:30
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def load_montage(montage_filepath=None, readfunc=None):
    from data_load import read_dat, read_montagemat
    montage = None
    if readfunc == None:
        readfunc = "read_dat"
    # exec can't load readfunc due to it has no func return
    # while eval do
    # exec("montage = %s(montage_filepath)" % (readfunc))
    montage = eval("%s(montage_filepath)" % (readfunc))
    return montage


def plot_montage_text(ax, ch_names, pos, show_names):
    '''
    基于给定的通道，显示对应名称
    '''
    if isinstance(show_names, (list, np.ndarray)):  # only given channels
        indices = [list(ch_names).index(name) for name in show_names]
    else:  # all channels
        indices = range(len(pos))
    for idx in indices:
        this_pos = pos[idx]
        x_offset = 0
        y_offset = 0.7
        # if kind == '3d':
        #     ax.text(this_pos[0], this_pos[1], this_pos[2], ch_names[idx])
        # else:
        ## 针对SynAmps2 Quik-Cap64模板的微调
        if ch_names[idx] in ['AF3', 'FT7']:
            x_offset -= 0.9
            y_offset -= 0.7
        elif ch_names[idx] in ['AF4', 'FT8']:
            x_offset += 0.9
            y_offset -= 0.7
        elif ch_names[idx] in ['PO7', 'PO8']:
            # x_offset += 0.7
            y_offset -= 1.4
        ax.text(this_pos[0] + x_offset,
                this_pos[1] + y_offset,
                ch_names[idx],
                fontsize=13,
                fontstyle='normal',
                fontweight='semibold',
                ha='center',
                va='center')
            

def plot_2dmontage(channel_data,  title=None, cmap_name='Blues', 
                   montage_path=None, montage_type=None):
    '''
    给定channel data 输出其数据对应的电极图
    '''
    montage = load_montage(montage_filepath=montage_path,
                           readfunc=montage_type)
    # show_names If an array, only the channel names in the array are shown
    fig = montage.plot(scale_factor=100,
                       kind='topomap',
                       show_names=False,
                       show=False,
                       sphere=(0.5, 0, 0, 9))
    ax = fig.axes[0]
    # get collection of dots in the original montage plot
    collection = ax.collections[0]
    
    map_vir = plt.cm.get_cmap(cmap_name)
    channel_data_min = channel_data.min()
    # Two slope
    if cmap_name == "RdBu_r":
        if channel_data_min >= 0:
            channel_data_min = -0.000000001
        norm = mpl.colors.TwoSlopeNorm(vmin=channel_data_min, vcenter=0, vmax=channel_data.max())
    else:
        if channel_data.min() < 0:
            norm = plt.Normalize(channel_data_min, channel_data.max())
        else:
            norm = plt.Normalize(0, channel_data.max())
    if False: # Sometimes maybe needs boundary Norm
        norm = mpl.colors.BoundaryNorm([-0.5,0.5,1.5,2.5,3.5,4.5,5.5], map_vir.N)  # Permutation Test
    
    color = map_vir(norm(channel_data))
    collection.set_color(color)
    
    sm = plt.cm.ScalarMappable(cmap=map_vir, norm=norm)
    cbar = fig.colorbar(mappable=sm,
                 ax=ax,
                 orientation='vertical',
                 fraction=0.04,
                 pad=0,
                 spacing='uniform',)

    # plot montage text based on the condition, heare plot over the half of absolute value
    pos = collection.get_offsets()
    ch_names = montage.ch_names
    nd_ch_names = np.array(ch_names)
    mask_names = np.abs(channel_data) > np.abs(np.mean(channel_data))
    show_names = nd_ch_names[mask_names]
    plot_montage_text(ax=ax, ch_names=ch_names, pos=pos, show_names=show_names)
    
    if title == None:
        fig.suptitle("")
    else:
        fig.suptitle(title, fontsize=25)
    return fig, ax


def main():
    # Example data
    channel_data = np.random.randn((32))
    # Example cmaps "viridis", "Reds", "Blues", "RdBu","RdBu_r"
    fig, ax = plot_2dmontage(channel_data,"Example", cmap_name="Reds",
                             montage_path="electrode_location_file\\dataset_deap.DAT")
    # fig.savefig("fig.eps",format="pdf", bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    main()
