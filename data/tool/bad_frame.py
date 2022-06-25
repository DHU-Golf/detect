from scipy.spatial.distance import euclidean
import data.tool.prepare_data as prepare_data
import data.tool.mydtw as myDTW
import argparse
import dtw
from data.tool.mat_rotate import calculate_dis
from matplotlib import pyplot as plt
from project_config import compress_for_gui 


def badframe(point_path_a, point_path_b, hit_method=0):
    [data_one, data_two] = prepare_data.prepare(point_path_a, point_path_b, int(hit_method))
    data_one_std = myDTW.mat_reshape(data_one)
    data_two_std = myDTW.mat_reshape(data_two)
    final = dtw.dtw(data_one_std, data_two_std)
    distance_list = []

    for i in range(len(final.index1)):
        if compress_for_gui:
            data = {
                'index_id': i,
                'index1_id': final.index1[i],
                'index2_id': final.index2[i],
                'distance':  euclidean(data_one_std[final.index1[i]], data_two_std[final.index2[i]])
            }
        else:
            data = {
                'index_id': i,
                'index1_id': final.index1[i],
                'index2_id': final.index2[i],
                'distance': calculate_dis(data_one[final.index1[i]],
                                        data_two[final.index2[i]])
            }
        distance_list.append(data)

    y = [i['distance'] for i in distance_list]
    x = [i for i in range(len(distance_list))]
    aver = sum(y) / len(distance_list)

    plt.plot(x, y)
    plt.plot(x, [aver for i in range(len(distance_list))])
    distance_list_sorted = sorted(distance_list, key=lambda index: index['distance'], reverse=True)
    return [plt, distance_list_sorted, [final, data_one, data_two]]


if __name__ == "__main__":
    parse = argparse.ArgumentParser("find bad frame(distance) in sequence")
    parse.add_argument('point_path_a', help='path_a')
    parse.add_argument('point_path_b', help='path_b')
    parse.add_argument('hit_method', help='how to find the hit events')
    arg = parse.parse_args()
    ans = badframe(arg.point_path_a, arg.point_path_b)
    plt.show()
    print(ans[1][0]['index_id'])

