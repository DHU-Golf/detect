"""
batch evaluate
"""
import os
import platform
import re
import subprocess

import project_config as cf


def output(video_path, res_path, cmd_s, std_v='PE4.mp4', num=0):
    # video_p_root=r"C:\Users\ao\Desktop\detect\data\3d_point"
    video_p_root = video_path
    video_p_files = [name for name in os.listdir(video_p_root) if (name.endswith('.npy'))]
    # f = open('/Users/yanting/Desktop/Projects/Golf/detect-new/data/Result.txt', 'w')
    f = open(res_path, 'w')

    for i in range(1, num + 1):
        print(std_v + ' and ' + str(i) + '.mp4')
        if platform.system() == 'Windows':
            cmd = cmd_s + f" {cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/%s.npy {cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/%s.mp4.npy" % (
                std_v, i)
        else:
            cmd = cmd_s + f" {cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/%s.npy {cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}/%s.mp4.npy" % (
                std_v, i)
            cmd = cmd + r" 2>/dev/null"  # to remove warning for matplotlib in *nix
        ans = subprocess.getoutput(cmd)
        print(re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]').sub('', ans))  # to remove ESC[Xm in Windows Powershell
        f.write(str(i) + ',' + re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]').sub('', ans) + '\n')
    f.close()


if __name__ == "__main__":
    video_p_root = f"{cf.PROJECT_ROOT}data/{cf.the_name_of_typeof_3d_pose}"
    res_path = r"../grades/Resultstd.txt"
    # res_path = r"../grades/Result1o-form.txt"

    # use_mydis for use mydistance or not
    # hit_method    2 -> maual chart 1 -> golfdb  0 -> distance 
    # for paper -hit_method 0 -use_mydis 0 -not_dtw_dis 1

    cmd_s = f"python {cf.PROJECT_ROOT}data/tool/mydtw.py -hit_method {cf.the_hit_method_for_out} -use_mydis 0 -not_dtw_dis 1"
    # cmd_s = f"python {cf.PROJECT_ROOT}data/tool/mydtw.py -hit_method 0 "
    # cmd_s=r"python.exe C:\Users\ao\Desktop\detect\data\tool\compare.py"
    # num for min=1 to max=video.num
    output(video_p_root, res_path, cmd_s, num=396)
