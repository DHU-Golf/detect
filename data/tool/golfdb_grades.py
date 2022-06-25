"""
use swingNet or our CBAM-swingNet to detect 8 key frames and evaluate
"""

import project_config as cf
from data.golfdb.events import events
from data.tool.compare import Load_DATA
from data.tool.mat_rotate import calculate_dis


def cal_DB(res_path, std_v="PE4"):
    teacher = cf.PROJECT_ROOT + "data/video_raw/%s.mp4" % std_v
    f = open(res_path, 'w')

    for i in range(1, 397):
        stu = cf.PROJECT_ROOT + "data/video_raw/%s.mp4" % i
        # T = events(teacher)
        # T = [75  90  93 107 110 114 90 156]  # program
        T = [68, 85, 92, 102, 108, 113, 115, 140]  # here T is for PE4
        S = events(stu)
        [data_one, data_two] = Load_DATA(cf.PROJECT_ROOT + f"data/{cf.the_name_of_typeof_3d_pose}/%s.mp4.npy" % std_v,
                                         cf.PROJECT_ROOT + f"data/{cf.the_name_of_typeof_3d_pose}/%s.mp4.npy" % i, if_hit=0)

        sum = 0
        for index in range(8):
            sum += calculate_dis(data_one[T[index]], data_two[S[index]])
        sum /= 8
        print(i, sum)
        f.write(str(i) + ',' + str(sum) + '\n')
    f.close()


if __name__ == "__main__":
    res_path = r"./DBF.txt"
    cal_DB(res_path)
