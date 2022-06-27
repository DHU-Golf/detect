import numpy as np

import data.tool.hit as hit
import data.tool.mat_rotate as mat_rotate
import project_config as cf
from scipy.spatial.distance import euclidean


def scale_data(data_one, data_two):
    # h scale
    # h_rate = data_one[0][10][2] / data_two[0][10][2]
    h_rate = data_one[0][0][2] / data_two[0][0][2]
    # h_rate = euclidean(data_one[0][7],data_one[0][0]) / euclidean(data_two[0][6],data_two[0][0])
    data_two = data_two * h_rate
    # # ---------------------------
    # for hip
    # data_one[:, :, 2] -= data_one[0, 0, 2]
    # data_two[:, :, 2] -= data_two[0, 0, 2]
    # h_rate =(np.max(data_one[0, :, 2]) - np.min(data_one[0, :, 2])) / (np.max(data_two[0, :, 2]) - np.min(data_two[0, :, 2]))
    # h_rate =(data_one[0][10][2] - data_one[0][0][2]) / (data_two[0][10][2] - data_two[0][0][2])
    # h_rate = euclidean(data_one[0][7], data_one[0][0]) / euclidean(data_two[0][7], data_two[0][0])
    # data_two[:, :, 2] = (data_two[:, :, 2] - data_two[0][0][2]) * h_rate + data_two[0][0][2]
    # data_two[:, :, 0] = data_two[:, :, 0] * h_rate
    # data_two[:, :, 1] = data_two[:, :, 1] * h_rate
    # ---------------------------
    # for visual
    # data_one[:, :, 2] -= np.min(data_one[:, :, 2])
    # data_two[:, :, 2] -= np.min(data_two[:, :, 2])
    return data_one, data_two


# decode path
def PATH_ex(s):
    s = s.replace(f"{cf.the_name_of_typeof_3d_pose}", "video_raw")
    s = s.replace(".mp4.npy", ".mp4")
    return s


def PATH_ex_v(s):
    s = s.replace("video_raw", f"{cf.the_name_of_typeof_3d_pose}")
    s = s.replace(".mp4", ".mp4.npy")
    return s


def prepare(point_path_a, point_path_b, hit_method=0, verbose=0):
    """

    Args:
        point_path_a: path for point a
        point_path_b: path for point b
        hit_method: how to find hit events
        verbose: print verbosely

    Returns: normalized sequences

    """

    data_one = np.load(point_path_a)
    data_two = np.load(point_path_b)

    if int(hit_method) == 0:
        one_hit = hit.findhit(data_one)
        two_hit = hit.findhit(data_two)
    elif int(hit_method) == 1:
        # golfdb
        one_hit = hit.findevent(PATH_ex(point_path_a))
        two_hit = hit.findevent(PATH_ex(point_path_b))
    elif int(hit_method) == 2:  # manual
        csv_p = f'{cf.PROJECT_ROOT}data/tag/tag.csv'
        one_hit = hit.find_hit_by_ao(csv_p, point_path_a)[:2]
        two_hit = hit.find_hit_by_ao(csv_p, point_path_b)[:2]

    if verbose:
        print(one_hit, two_hit)
    data_one = data_one[one_hit[0]:one_hit[1]]
    data_two = data_two[two_hit[0]:two_hit[1]]

    data_one, data_two = scale_data(data_one, data_two)

    best_ang = mat_rotate.best_angle(data_one[0], data_two[0]) / 10
    if verbose:
        print("best ang %lf" % best_ang)
    frame_lenth = data_one.shape[0]
    if verbose:
        for i in range(frame_lenth):
            data_one[i] = mat_rotate.rotate_mat(data_one[i], best_ang)
        print("done")
    else:
        for i in range(frame_lenth):
            data_one[i] = mat_rotate.rotate_mat(data_one[i], best_ang)

    return [data_one, data_two]
