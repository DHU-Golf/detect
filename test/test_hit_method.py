import numpy as np

import data.tool.hit as hit
import data.tool.prepare_data as prepare_data
import project_config as cf

def test_hit(test_id, csv_p):
    np_data_one_p = f'{cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/{test_id}.mp4.npy'
    np_data_one_v = f'{cf.PROJECT_ROOT}data/video_raw/{test_id}.mp4'

    # np_data_two_p = f'{cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/PE4.mp4.npy'
    np_data_one = np.load(f'{cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/{test_id}.mp4.npy')
    # np_data_two = np.load(f'{cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/PE4.mp4.npy')

    # data = prepare_data.prepare(np_data_one_p, np_data_two_p, hit_method=2)
    a0 = hit.findhit(np_data_one)
    # video path
    a1 = hit.findevent(np_data_one_v)
    # point path
    a2 = hit.find_hit_by_ao(csv_p, np_data_one_p)[:2]

    return [len(np_data_one), a0, a1, a2]


if __name__ == '__main__':
    test_id = 314
    ans=test_hit(test_id,f'{cf.PROJECT_ROOT}/data/tag/tag.csv')
    print(f'video {test_id} 长度', ans[0])
    print(f'hit_method 0 to video {test_id} 打击区间:', ans[1])
    print(f'hit_method 1 to video {test_id} 打击区间:', ans[2])
    print(f'hit_method 2 (std) to video {test_id} 打击区间:', ans[3])
