import argparse
import random

import matplotlib.pyplot as plt
import numpy as np

import data.tool.hit as hit
from data.tool.prepare_data import PATH_ex
from test.npzcompress import get_video
import project_config as cf

# random Japanese traditional color
sandbox = ["#DC9FB4", "#E16B8C", "#8E354A", "#F8C3CD", "#F4A7B9", "#64363C", "#F596AA", "#B5495B", "#E87A90", "#D05A6E",
           "#DB4D6D", "#FEDFE1", "#9E7A7A", "#D0104C", "#9F353A", "#CB1B45", "#EEA9A9", "#BF6766", "#86473F", "#B19693",
           "#EB7A77", "#954A45", "#A96360", "#CB4042", "#AB3B3A", "#D7C4BB", "#904840", "#734338", "#C73E3A", "#554236",
           "#994639", "#F19483", "#B54434", "#B9887D", "#F17C67", "#884C3A", "#E83015", "#D75455", "#B55D4C", "#854836",
           "#A35E47", "#CC543A", "#724832", "#F75C2F", "#6A4028", "#9A5034", "#C46243", "#AF5F3C", "#FB966E", "#724938",
           "#B47157", "#DB8E71", "#F05E1C", "#ED784A", "#CA7853", "#B35C37", "#563F2E", "#E3916E", "#8F5A3C", "#F0A986",
           "#A0674B", "#C1693C", "#FB9966", "#947A6D", "#A36336", "#E79460", "#7D532C", "#C78550", "#985F2A", "#E1A679",
           "#855B32", "#FC9F4D", "#FFBA84", "#E98B2A", "#E9A368", "#B17844", "#96632E", "#43341B", "#CA7A2C", "#ECB88A",
           "#78552B", "#B07736", "#967249", "#E2943B", "#C7802D", "#9B6E23", "#6E552F", "#EBB471", "#D7B98E", "#82663A",
           "#B68E55", "#BC9F77", "#876633", "#C18A26", "#FFB11B", "#D19826", "#DDA52D", "#C99833", "#F9BF45", "#DCB879",
           "#BA9132", "#E8B647", "#F7C242", "#7D6C46", "#DAC9A6", "#FAD689", "#D9AB42", "#F6C555", "#FFC408", "#EFBB24",
           "#CAAD5F", "#8D742A", "#B4A582", "#877F6C", "#897D55", "#74673E", "#A28C37", "#6C6024", "#867835", "#62592C",
           "#E9CD4C", "#F7D94C", "#FBE251", "#D9CD90", "#ADA142", "#DDD23B", "#A5A051", "#BEC23F", "#6C6A2D", "#939650",
           "#838A2D", "#B1B479", "#616138", "#4B4E2A", "#5B622E", "#4D5139", "#89916B", "#90B44B", "#91AD70", "#B5CAA0",
           "#646A58", "#7BA23F", "#86C166", "#4A593D", "#42602D", "#516E41", "#91B493", "#808F7C", "#1B813E", "#5DAC81",
           "#36563C", "#227D51", "#A8D8B9", "#6A8372", "#2D6D4B", "#465D4C", "#24936E", "#86A697", "#00896C", "#096148",
           "#20604F", "#0F4C3A", "#4F726C", "#00AA90", "#69B0AC", "#26453D", "#66BAB7", "#268785", "#405B55", "#305A56",
           "#78C2C4", "#376B6D", "#A5DEE4", "#77969A", "#6699A1", "#81C7D4", "#33A6B8", "#0C4842", "#0D5661", "#0089A7",
           "#336774", "#255359", "#1E88A8", "#566C73", "#577C8A", "#58B2DC", "#2B5F75", "#3A8FB7", "#2E5C6E", "#006284",
           "#7DB9DE", "#51A8DD", "#2EA9DF", "#0B1013", "#0F2540", "#08192D", "#005CAF", "#0B346E", "#7B90D2", "#6E75A4",
           "#261E47", "#113285", "#4E4F97", "#211E55", "#8B81C3", "#70649A", "#9B90C2", "#8A6BBE", "#6A4C9C", "#8F77B5",
           "#533D5B", "#B28FCE", "#986DB2", "#77428D", "#3C2F41", "#4A225D", "#66327C", "#592C63", "#6F3381", "#574C57",
           "#B481BB", "#3F2B36", "#572A3F", "#5E3D50", "#72636E", "#622954", "#6D2E5B", "#C1328E", "#A8497A", "#562E37",
           "#E03C8A", "#60373E", "#FCFAF2", "#FFFFFB", "#BDC0BA", "#91989F", "#787878", "#828282", "#787D7B", "#707C74",
           "#656765", "#535953", "#4F4F48", "#52433D", "#373C38", "#3A3226", "#434343", "#1C1C1C", "#080808", "#0C0C0C"]

coco_map = ["nose", "left_eye", "right_eye", "left_ear", "right_ear",
            "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
            "left_wrist", "right_wrist", "left_hip", "right_hip",
            "left_knee", "right_knee", "left_ankle", "right_ankle"]


# as for coco visual, see model test

def npztodata(path: str, name: str):
    keypoints = np.load(path, allow_pickle=True)
    data = keypoints['positions_2d'].item()
    output = np.array(data[name]['custom'])
    output = output[0]
    return output


def info(path: str, name: str):
    a = np.load(path, allow_pickle=True)
    b = a['metadata'].item()
    x = b['video_metadata'][name]['w']
    y = b['video_metadata'][name]['h']
    return [x, y]


def draw_pic(path_3d, name, save=None, hit_method=0):
    td_data = np.load(path_3d)
    data = npztodata(path, name=name)
    max_x, max_y = info(path, name=name)
    v_info = get_video(name)

    # Vertical transformation
    data[:, :, 1] = abs(data[:, :, 1] - v_info['h'])

    if hit_method:
        hit_time = hit.events(PATH_ex(path_3d))
    else:
        hit_time = hit.findhit(td_data)

    fig = plt.figure(figsize=(20, 10), dpi=200)
    plt.axes().set_aspect('auto')
    for i in range(data.shape[2]):
        for j in range(data.shape[1]):
            if j != 7 and j != 8 and j!=9 and j!=10:
                continue
            c_str = sandbox[int(random.random() * 250)]
            if i == 0:
                continue
                clip = data[:, j, i] / max_x
                plt.plot(range(len(clip)), clip, label=coco_map[j] + '-x', color=c_str)
            else:
                clip = data[:, j, i] / max_y
                plt.plot(range(len(clip)), clip, label=coco_map[j] + '-y', color=c_str)

    plt.vlines(hit_time[0], 0.1, .9)
    plt.vlines(hit_time[1], 0.1, .9)

    plt.xlabel('frame')
    plt.ylabel('location')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize="small")
    if save is None:
        plt.show()
    else:
        plt.savefig(save + '.png')
    plt.close()


path = f'{cf.PROJECT_ROOT}VideoPose3D/data/data_2d_custom_myvideos.npz'

if __name__ == '__main__':
    """
    default use distance to find event
    """

    parse = argparse.ArgumentParser("use 2d points to draw chart")
    parse.add_argument('--save', '-s', help='save_path')
    parse.add_argument('point_path', help='3d point path')
    parse.add_argument('video_name', help='video full name')

    arg = parse.parse_args()
    path_3d = arg.point_path
    name = arg.video_name

    draw_pic(path_3d, name, arg.save)
