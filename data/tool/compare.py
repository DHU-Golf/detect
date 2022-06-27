# Load_DATA -> prepare_data 

import argparse

import numpy as np
import tqdm

import data.tool.hit as hit
import data.tool.mat_rotate as mat_rotate
from data.golfdb.events import events
from data.tool.prepare_data import PATH_ex, scale_data


def Load_DATA(point_path_a, point_path_b, verbose=0, if_hit=1, hit_method=0):
    data_one = np.load(point_path_a)
    data_two = np.load(point_path_b)

    if if_hit == 1:
        one_hit = hit.findhit(data_one)
        two_hit = hit.findhit(data_two)

        if verbose:
            print(one_hit, two_hit)
        data_one = data_one[one_hit[0]:one_hit[1]]
        data_two = data_two[two_hit[0]:two_hit[1]]

    data_one, data_two = scale_data(data_one, data_two)

    best_ang = mat_rotate.best_angle(data_one[0], data_two[0]) / 10
    if verbose:
        print("best_ang %lf" % best_ang)
    frame_lenth = data_one.shape[0]
    if verbose:
        for i in tqdm.tqdm(range(frame_lenth)):
            data_one[i] = mat_rotate.rotate_mat(data_one[i], best_ang)
        print("done")
    else:
        for i in range(frame_lenth):
            data_one[i] = mat_rotate.rotate_mat(data_one[i], best_ang)

    return [data_one, data_two]


def justdistance(data_one, data_two):
    dist = 0
    num = min(len(data_one), len(data_two))
    for i in range(0, num):
        oned = int(len(data_one) / num * i)
        twod = int(len(data_two) / num * i)
        dist += mat_rotate.calculate_dis(data_one[oned], data_two[twod])
    dist = dist / num
    return dist


def Compare_DIS(point_path_a, point_path_b):
    data_one, data_two = Load_DATA(point_path_a, point_path_b)
    ans = justdistance(data_one, data_two)
    return ans


def Compare_GOLFDB(point_path_a, point_path_b):
    data_one, data_two = Load_DATA(point_path_a, point_path_b, if_hit=0)
    # data_one is std
    key_frame = [1, 1, 1, 1, 1, 1, 1, 1]
    tf = events(PATH_ex(point_path_a))
    sf = events(PATH_ex(point_path_b))
    dist = 0
    for i in range(0, len(tf)):
        dist += mat_rotate.calculate_dis(data_one[tf[i]], data_two[sf[i]])
    return dist / len(tf)


if __name__ == "__main__":
    parse = argparse.ArgumentParser("compare")
    parse.add_argument('point_path_a', help='path a')
    parse.add_argument('point_path_b', help='path b')
    args = parse.parse_args()
    # import project_config as cf
    #
    # ppath = f'{cf.PROJECT_ROOT}data/3d_point_vis/'
    # for i in range(1, 191):
    #     ans = Compare_GOLFDB(ppath + "PE4.mp4.npy", ppath + f"{i}.mp4.npy")
    #     print(str(i) + "," + str(ans))
