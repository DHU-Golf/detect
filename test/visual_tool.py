import matplotlib.pyplot as plt
import numpy as np

import project_config as cf

from data.tool.anime import DrawOneFrame
from data.tool.prepare_data import PATH_ex_v
from test.npzcompress import read_coco_2d_17, read_human_2d_17, get_video

"""
human 36m and coco 17 joints visual tool
created by ao
"""


# For 2D visual
def vis_2d_coco_17(filename, frame, fix=True):
    if fix:
        coco_17_skeleton = [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 7], [6, 8], [7, 9], [8, 10],
                            [9, 11], [2, 3], [1, 2], [1, 3], [2, 4], [3, 5]]
    else:
        coco_17_skeleton = [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13], [6, 7], [6, 8], [7, 9],
                            [8, 10],
                            [9, 11], [2, 3], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]]

    
    info = get_video(filename)
    fig, ax = plt.subplots()
    plt.xlim(0, info['w'])
    plt.ylim(0, info['h'])
    plt.autoscale(False)
    ax.set_aspect(1)

    data_2d_coco_17_data = read_coco_2d_17(filename, frame)
    for i in data_2d_coco_17_data:
        i[1] = abs(i[1] - info['h'])

    for i in coco_17_skeleton:
        x_p = [data_2d_coco_17_data[i[0] - 1][0], data_2d_coco_17_data[i[1] - 1][0]]
        y_p = [data_2d_coco_17_data[i[0] - 1][1], data_2d_coco_17_data[i[1] - 1][1]]
        plt.plot(x_p, y_p)

    if fix:
        top_m = (data_2d_coco_17_data[5] + data_2d_coco_17_data[6]) / 2
        plt.plot([data_2d_coco_17_data[0][0], top_m[0]], [data_2d_coco_17_data[0][1], top_m[1]])
        under_m = (data_2d_coco_17_data[12] + data_2d_coco_17_data[11]) / 2
        plt.plot([under_m[0], top_m[0]], [under_m[1], top_m[1]])
    plt.show()

    return read_coco_2d_17(filename, frame)


def vis_2d_human36m_17(filename, frame):
    human36m_17_skeleton = [[10, 9], [9, 8], [8, 7], [7, 0], [0, 1], [1, 2], [2, 3], [0, 4], [4, 5], [5, 6], [8, 14],
                            [14, 15], [15, 16], [8, 11], [11, 12], [12, 13]]

    # junk code
    # for i in range(0, len(human36m_17_skeleton)):
    #     human36m_17_skeleton[i][0] += 1
    #     human36m_17_skeleton[i][1] += 1

    info = get_video(filename)
    fig, ax = plt.subplots()
    plt.xlim(0, info['w'])
    plt.ylim(0, info['h'])
    plt.autoscale(False)
    ax.set_aspect(1)

    data_2d_human_17_data = read_human_2d_17(filename, frame)
    for i in data_2d_human_17_data:
        i[1] = abs(i[1] - info['h'])

    for i in human36m_17_skeleton:
        x_p = [data_2d_human_17_data[i[0]][0], data_2d_human_17_data[i[1]][0]]
        y_p = [data_2d_human_17_data[i[0]][1], data_2d_human_17_data[i[1]][1]]
        plt.plot(x_p, y_p)

    # if fix:
    #     top_m = (data_2d_human_17_data[5] + data_2d_human_17_data[6]) / 2
    #     plt.plot([data_2d_human_17_data[0][0], top_m[0]], [data_2d_human_17_data[0][1], top_m[1]])
    #     under_m = (data_2d_human_17_data[12] + data_2d_human_17_data[11]) / 2
    #     plt.plot([under_m[0], top_m[0]], [under_m[1], top_m[1]])
    plt.show()

    return read_human_2d_17(filename, frame)


# For 3d visual
def vis_3d_human36_17(filename, frame, elev=0, azim=90):
    v_p = cf.PROJECT_ROOT + f"data/video_raw/" + filename
    data = np.load(PATH_ex_v(v_p))
    DrawOneFrame(data[frame], elev=elev, azim=azim)


if __name__ == "__main__":
    vis_2d_coco_17('1.mp4', 0)
    # vis_3d_human36_17("183.mp4", 0, elev=45, azim=45)