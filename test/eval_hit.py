import sys

import numpy as np
import tqdm

import data.tool.hit as hit
import project_config as cf


def relation(interval_a, interval_b):

    min1, max1 = interval_a[0], interval_a[1]
    min2, max2 = interval_b[0], interval_b[1]
    if min1 == min2 and max1 == max2: return 0
    if max1 < min2 or max2 < min1: return 1
    if min1 < min2 <= max1 < max2 or min2 < min1 <= max2 < max1: return 2
    if min1 <= min2 <= max2 <= max1 or min2 <= min1 <= max1 <= max2: return 3


def intersection(interval_a, interval_b):
    nums = sorted(interval_a + interval_b)
    if relation(interval_a, interval_b) != 1:
        return [nums[1], nums[2]]
    else:
        return []


def eval_hit(test_id, csv_p, hit_method=0):
    np_data_one_p = f'{cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/{test_id}.mp4.npy'
    np_data_one_v = f'{cf.PROJECT_ROOT}data/video_raw/{test_id}.mp4'

    # np_data_two_p = f'{cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/PE4.mp4.npy'
    np_data_one = np.load(f'{cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/{test_id}.mp4.npy')
    # np_data_two = np.load(f'{cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/PE4.mp4.npy')

    # data = prepare_data.prepare(np_data_one_p, np_data_two_p, hit_method=2)

    if hit_method == 0:
        ans = hit.findhit(np_data_one)

    elif hit_method == 1:
        ans = hit.findevent(np_data_one_v)

    std_ans = hit.find_hit_by_ao(csv_p, np_data_one_p)
    if ans is None:
        print("ans is None", file=sys.stderr)
        raise KeyError
    else:
        # err_len = abs(std_ans[0] - ans[0]) + abs(std_ans[1] - ans[1])
        f1s = f1_socre(std_ans[:2], ans)
        # print(f1s)
    # return [err_len / (std_ans[1] - std_ans[0]), ans, std_ans[:2], std_ans[2]]
    return [f1s, ans, std_ans[:2], std_ans[2]]
    # return [len(np_data_one), a0, a1, a2]


def f1_socre(std_ans, ans):
    true_set = intersection(std_ans, ans)
    if len(true_set) == 2:
        true_len = true_set[1] - true_set[0]
    else:
        return 0
    pre = true_len / (ans[1] - ans[0])
    rec = true_len / (std_ans[1] - std_ans[0])
    if pre + rec == 0:
        return 0
    return 2 * pre * rec / (pre + rec)


def eval_whole(start, end, csv_p, hit_method, pass_err_video=True):
    data = []
    for i in tqdm.tqdm(range(start, end)):
        ans = eval_hit(i, csv_p, hit_method)
        if pass_err_video and ans[3]:
            # print("pass happened")
            pass
        else:
            data.append(ans[0])
    return sum(data) / len(data)


if __name__ == '__main__':
    # test_id = 5
    # ans = eval_hit(test_id, f'{cf.PROJECT_ROOT}data/tag/tag.csv', hit_method=1)
    # print(f'video {test_id} f1', "{:.2f}".format(ans[0]))
    # print(f'video {test_id} 测量区间', ans[1])
    # print(f'video {test_id} 实际区间', ans[2])
    # print(f'video {test_id} 存在视频缺陷{ans[3]}')

    # aver = eval_whole(1, 397, f'{cf.PROJECT_ROOT}data/tag/tag.csv', 0, True)
    # print("基于距离", aver)
    # print("\n")
    aver = eval_whole(1, 397, f'{cf.PROJECT_ROOT}data/tag/tag.csv', 1, True)
    print("based golfdb", aver)
