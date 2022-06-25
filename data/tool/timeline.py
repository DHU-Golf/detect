"""
for process map
"""

import numpy as np
from matplotlib import pyplot as plt

from matplotlib.ticker import MultipleLocator


def time_line(list):
    time_len = list[len(list) - 1] - list[0]
    list_p = [i - list[0] for i in list]
    ans = [i / time_len for i in list_p]
    return ans

def PlotaLine(ax, id, marker, list, label, key=4):
    y = np.ones(len(list)) * id
    x = time_line(list)
    ax.plot(x[:key], y[:key], marker=marker, label=label, color='blue')
    ax.plot(x[key - 1:], y[key - 1:], marker=marker, color='red')
    # ax.text(label,0,0)
    # ax.plot(x[key:],y[key:],marker=marker,label=label,color='blue')

def Pic(figsize=(10, 3)):
    fig = plt.figure(figsize=figsize)
    plt.yticks([])
    ax = plt.gca()
    loc = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    x_major_locator = MultipleLocator(0.1)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    return [fig, plt]


if __name__ == "__main__":

    DATA = [
        [73, 86, 93, 103, 110, 114, 117, 135], 
        [104, 124, 131, 140, 147, 153, 157, 170],  
        [31, 43, 55, 70, 77, 81, 84, 101], 
        [18, 29, 35, 45, 59, 66, 69, 80],  # 18
        [6, 27, 39, 55, 66, 70, 73, 87],  # 155
        [81, 104, 112, 124, 130, 136, 139, 154]  # 162 
    ]

    # use mpv to tag 
    # mpv.conf
    # osd-status-msgosd-status-msg=${playback-timefull}  ${duration} (${percent-pos}%)nframe ${estimated-frame-number}  ${estimated-frame-count}

    v_name = ['PE4', '3', '1', '18', '155', '162']

    shape = ['o', '+', '*', 'x', 's', 'd', 'p', 'h']

    [fig, ax] = Pic()
    for i in range(len(DATA)):
        PlotaLine(ax, -i, shape[i], DATA[i], v_name[i])
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize="small", frameon=False)
    leg = ax.gca().get_legend()
    for i in leg.legendHandles:
        i.set_color('black')
    plt.show()
