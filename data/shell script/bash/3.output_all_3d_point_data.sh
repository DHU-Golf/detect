#!/bin/bash
my_env
file_path=~/Desktop/detect/data/video_raw
items=$(ls $file_path)
cd ~/Desktop/detect/VideoPose3D/
for item in $items
do
       python run.py \
       -d custom -k myvideos \
       -arc 3,3,3,3,3 -c checkpoint \
       --evaluate pretrained_h36m_detectron_coco.bin \
       --render --viz-subject $item \
       --viz-action custom \
       --viz-camera 0 \
       --viz-video ~/Desktop/detect/data/video_raw/$item \
       --viz-export ~/Desktop/detect/data/3d_point/$item \
       --viz-size 6
done

read -n1 -p "press any key to continue..."