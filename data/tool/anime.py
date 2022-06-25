import argparse
import os

import dtw
import matplotlib.pyplot as plt
import tqdm

import data.tool.mydtw as myDTW
import data.tool.prepare_data as prepare_data



# data struct [0 ~ sum][17 coco][x,y,z]

def Draw_Single(ax, data, color='red'):
    x_points = data[:, 0]
    y_points = data[:, 1]
    z_points = data[:, 2]

    ax.scatter3D(x_points, y_points, z_points)
    ax.plot(data[0:4, 0], data[0:4, 1], data[0:4, 2], color=color)
    ax.plot(data[4:7, 0], data[4:7, 1], data[4:7, 2], color=color)
    ax.plot(data[8:11, 0], data[8:11, 1], data[8:11, 2], color=color)
    ax.plot(data[11:14, 0], data[11:14, 1], data[11:14, 2], color=color) # l-h + l-l
    ax.plot(data[14:17, 0], data[14:17, 1], data[14:17, 2], color=color) # r-h + r-l
    ax.plot((data[0, 0], data[7, 0]), (data[0, 1], data[7, 1]), (data[0, 2], data[7, 2]), color=color)
    ax.plot((data[8, 0], data[7, 0]), (data[8, 1], data[7, 1]), (data[8, 2], data[7, 2]), color=color)
    ax.plot((data[8, 0], data[11, 0]), (data[8, 1], data[11, 1]), (data[8, 2], data[11, 2]), color=color)
    ax.plot((data[8, 0], data[14, 0]), (data[8, 1], data[14, 1]), (data[8, 2], data[14, 2]), color=color)
    ax.plot((data[0, 0], data[4, 0]), (data[0, 1], data[4, 1]), (data[0, 2], data[4, 2]), color=color)


def DrawOneFrame(data_one, data_two=None, color_one='red', color_two='blue', save_path=None, id=0, elev=0, azim=90,
                 dpi=100):
    fig = plt.figure(figsize=plt.figaspect(1))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.view_init(elev, azim)
    radius = 1.6
    ax.set_xlim3d([-radius / 2, radius / 2])
    ax.set_zlim3d([0, radius])
    ax.set_ylim3d([-radius / 2, radius / 2])
    Draw_Single(ax, data_one, color=color_one)
    if data_two is not None:
        Draw_Single(ax, data_two, color=color_two)
    if save_path is not None:
        plt.savefig(save_path + str(id) + '.png', dpi=dpi)
    else:
        plt.show()
    plt.close()


if __name__ == '__main__':

    """
    1. python anime.py data1 data2 video_save_path
    2. need ffmpeg in path
    """

    parse = argparse.ArgumentParser("anime generator")
    parse.add_argument('point_path_a', help='path a')
    parse.add_argument('point_path_b', help='path b')
    parse.add_argument('save', help='save_path')
    parse.add_argument('name', help='save_name')

    arg = parse.parse_args()

    save_path = arg.save
    [data_one, data_two] = prepare_data.prepare(arg.point_path_a, arg.point_path_b, 0)

    data_one_std = myDTW.mat_reshape(data_one)
    data_two_std = myDTW.mat_reshape(data_two)

    print("calculate DTW")
    # final = dtw.dtw(data_one_std, data_two_std, dist_method=mydistance.mydistance)
    final = dtw.dtw(data_one_std, data_two_std)
    print("DTW ans:", final.distance)
    # ans
    # plt.plot(final.index1, final.index2)
    # plt.show()

    fin_frame = len(final.index1)
    
    for i in tqdm.tqdm(range(0, fin_frame)):
        DrawOneFrame(data_one[final.index1[i]], data_two[final.index2[i]], save_path=save_path, id=i)

    output = save_path + arg.name + ".mp4"
    command = "ffmpeg -f image2 -i " + save_path + "%d.png" + " " + output
    os.system(command)

    c_clear = "cd " + save_path + " & " + "rm *.png"
    os.system(c_clear)

# -------------------------------------
#   for i in tqdm.tqdm(range(0, max_frame)):
#     if i < min_frame:
#         DrawOneFrame(data_one[i], data_two[i], save_path=save_path, id=i)
#     else:
#         DrawOneFrame_Single(data_one[i], save_path=save_path, id=i)

# def DrawOneFrame_Single(data_one, color_one='red', save_path=None, id=0):
#     fig = plt.figure(figsize=plt.figaspect(1))
#     ax = fig.add_subplot(1, 1, 1, projection='3d')
#     ax.view_init(elev=0, azim=90)
#     radius = 1.6
#     ax.set_xlim3d([-radius / 2, radius / 2])
#     ax.set_zlim3d([0, radius])
#     ax.set_ylim3d([-radius / 2, radius / 2])
#     Draw_Single(ax, data_one, color=color_one)
#     plt.savefig(save_path + str(id) + '.png')
#     plt.close()
