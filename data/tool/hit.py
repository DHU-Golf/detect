import re

import pandas as pd

import data.tool.mat_rotate as mat_rotate
from data.golfdb.events import events
import project_config as cf

def findhit(data):
    d_array = []
    start = 0
    end = 0
    interval = 3  
    max_d = 0.15
    for i in range(data.shape[0] - interval):
        ans = mat_rotate.calculate_dis(data[i], data[i + interval])
        d_array.append(ans)

    for i in range(len(d_array)):
        if d_array[i] > max_d:
            start = i
            break

    d_array.reverse()
    for i in range(len(d_array)):
        if d_array[i] > max_d:
            end = len(d_array) - i
            break

    return [start, end]

# @profile('include_children')
def findevent(v_path):
    el = events(v_path)
    return [min(el), max(el)]


# for ground truth
def find_hit_by_ao(csv_path, data_path):
    data = pd.read_csv(csv_path, sep=',', header=0,keep_default_na=False)
    t = re.search(r'PE4\.mp4', data_path)
    if t is not None:
        return [73, 136]
    else:
        m = re.search(r'\d+\.mp4', data_path)
        assert m is not None
        mpv_id = int(re.search(r'\d+', m.group(0)).group(0))
        if data['tips'][int(mpv_id - 1)] != '':
            tips = True
        else:
            tips = False
        return [int(data['start'][int(mpv_id - 1)]), int(data['end'][int(mpv_id - 1)]), tips]


if __name__ == '__main__':
    print(find_hit_by_ao(f'{cf.PROJECT_ROOT}data/tag/tag.csv', f'{cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/1.mp4.npy')[:2])
