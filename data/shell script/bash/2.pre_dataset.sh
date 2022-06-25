#!/bin/bash
my_env
cd ~/Desktop/detect/VideoPose3D/data/
python prepare_data_2d_custom.py -i ~/Desktop/detect/data/2d_point/ -o 'myvideos'

read -n1 -p "press any key to continue..."