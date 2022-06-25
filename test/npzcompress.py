import sys

import numpy as np
import project_config as cf
from PoseFormer.coco_h36m import coco_h36m

def get_video(video_name):
    try:
        loaded = np.load(f'{cf.PROJECT_ROOT}VideoPose3D/data/data_2d_custom_myvideos.npz', allow_pickle=True)
    except:
        print("read error", file=sys.stderr)
    data = loaded['metadata'].item()['video_metadata'][video_name]
    return data


def read_coco_2d_17(video_name, frame):
    try:
        loaded = np.load(f'{cf.PROJECT_ROOT}VideoPose3D/data/data_2d_custom_myvideos.npz', allow_pickle=True)
    except:
        print("read error", file=sys.stderr)
    data = loaded['positions_2d'].item()
    return data[video_name]['custom'][0][frame]


def read_human_2d_17(video_name, frame):
    try:
        loaded = np.load(f'{cf.PROJECT_ROOT}VideoPose3D/data/data_2d_custom_myvideos.npz', allow_pickle=True)
    except:
        print("read error", file=sys.stderr)
    data = loaded['positions_2d'].item()
    ans = coco_h36m(data[video_name]['custom'][0])
    return ans[frame]


if __name__ == '__main__':
    loaded = np.load(f'{cf.PROJECT_ROOT}PoseFormer/data/data_2d_custom_myvideos_coco17.npz', allow_pickle=True)
    # for i in loaded:
    #     print(i)
    data = loaded['positions_2d'].item()
    for i in data:
        # if ".mp4" in i:
        data[i]['custom'][0] = coco_h36m(data[i]['custom'][0])

    np.savez_compressed(f'{cf.PROJECT_ROOT}PoseFormer/data/data_2d_custom_myvideos', positions_2d=data,
                        metadata=loaded['metadata'])
