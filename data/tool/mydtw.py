import argparse

import dtw
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean

import data.tool.prepare_data as prepare_data
from data.tool.mydistance import mydistance


def mat_reshape(data):
    tem = data.shape[0]
    return data.reshape(tem, 51)


def drawforDTW(data_one, data_two, v=0, not_dtw_dis=True, new=False, aver=True, if_save=False, save_p='.', dpi=100):
    data_one = mat_reshape(data_one)
    data_two = mat_reshape(data_two)

    if new == True:
        final = dtw.dtw(data_one, data_two, dist_method=mydistance)
    else:
        final = dtw.dtw(data_one, data_two, step_pattern=dtw.symmetric2)  # dist_method=euclidean  default

    # new=False not_dtw_dis=1 aver=True
    # new=True not_dtw_dis=0 aver=False distance->normalizedDistance
    # new=False not_dtw_dis=0 aver=False distance->normalizedDistance x
    # new=False not_dtw_dis=1 aver=True pattern=s1 x

    if not not_dtw_dis:
        if aver == False:
            fin_dis = final.normalizedDistance
            # fin_dis = final.distance
            # print(fin_dis)
        else:
            fin_dis = final.distance / len(final.index1)
        plt.plot(final.index1, final.index2)
    else:
        dist = 0
        # random.sample(final.index1, 100)
        for i in range(0, len(final.index1)):
            # nd = int(len(final.index1)/100*i)
            dist += euclidean(data_one[final.index1[i]], data_two[final.index2[i]])

        if aver == False:
            fin_dis = dist
            print(dist)
        else:
            fin_dis = dist / len(final.index1)  # same length as index2
        plt.plot(final.index1, final.index2)

    if v:
        plt.show()
    if if_save:
        plt.savefig('dtw.png', dpi=dpi)

    plt.close()
    return fin_dis

if __name__ == '__main__':
    parse = argparse.ArgumentParser("DTW calculate")
    parse.add_argument('point_path_a', help='data a')
    parse.add_argument('point_path_b', help='data b')
    parse.add_argument('-hit_method', help='how to find hit', default=0)
    parse.add_argument('-not_dtw_dis', help='how to calculate distance', default=True)
    parse.add_argument('-use_mydis', help='dtw func', default=False)
    parse.add_argument('-verbose', help='verbose mode', default=0)

    arg = parse.parse_args()
    [data_one, data_two] = prepare_data.prepare(arg.point_path_a, arg.point_path_b, hit_method=int(arg.hit_method),
                                                verbose=arg.verbose)

    ans = drawforDTW(data_one, data_two, v=arg.verbose, not_dtw_dis=bool(int(arg.not_dtw_dis)),
                     new=bool(int(arg.use_mydis)))  # res4
    print(ans, end='')

# -------------------------------------------------------------------
# drawforDTW(data_one, data_two, arg.verbose, new=True)     # res2


# drawforDTW_sameLen(data_one, data_two, arg.verbose)  # res1
# drawforDTW_sameLen(data_one, data_two, arg.verbose,new=True) # res3

# a. pyhon-dtw
# b. fastdtw 

#  remove
#  def drawforDTW_sameLen(data_one, data_two, v=0,num=100, new=False, aver=True):
#     data_one = matstd(data_one)
#     data_two = matstd(data_two)
#     if new == True:
#         final = dtw.dtw(data_one, data_two, dist_method = mydistance)
#     else:
#         final = dtw.dtw(data_one, data_two, dist_method = euclidean)
#
#     dist = 0
#     #     random.sample(final.index1, 100)
#     for i in range(0, num):
#         nd = int(len(final.index1) / num * i)
#         if new == True:
#             dist += mydistance(data_one[final.index1[nd]], data_two[final.index2[nd]])
#         else:
#             dist += euclidean(data_one[final.index1[nd]], data_two[final.index2[nd]])
#
#     if aver==True:
#         dist=dist/100.0
#
#     print(dist)
#
#     if v:
#         plt.plot(final.index1, final.index2)
#         plt.show()
