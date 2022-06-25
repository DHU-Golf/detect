import sys

import numpy as np
from scipy.spatial.distance import euclidean


def calculate_dis(one, two, weight=None):
    if weight is None:
        weight = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    coco_point = 17
    sum = 0.0
    for i in range(coco_point):
        sum += weight[i] * euclidean(one[i], two[i])
    return sum


def rotate_mat(data, angle):
    mat = data[:, 0:2]
    s = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    mat = np.dot(mat, s)
    data[:, 0:2] = mat
    return data


def best_angle(one, two):
    d_array = []
    for i in range(-600, 600, 1):
        tem_one = one.copy()
        rotate_mat(tem_one, i / 10)
        tem = calculate_dis(tem_one, two)
        d_array.append([i, tem])
    d_array = sorted(d_array, key=lambda data: data[1])
    return d_array[0][0]


if __name__ == '__main__':
    data_one = np.load(sys.argv[1])[0]  
    data_two = np.load(sys.argv[2])[0] 
    print(best_angle(data_one, data_two) / 10)
