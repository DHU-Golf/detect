#!/bin/bash
my_env
file_path=~/Desktop/detect/data/video_raw
items=$(ls $file_path)
cd ~/Desktop/detect/PoseFormer/
for item in $items
do
       python run_poseformer_vis.py \
       -d custom -k myvideos \
       -c checkpoint \
       --evaluate detected81f.bin \
       --render --viz-subject $item \
       --viz-action custom \
       --viz-camera 0 \
       --viz-video ~/Desktop/detect/data/video_raw/$item \
       --viz-export ~/Desktop/detect/data/3d_point_form/$item \
       --viz-size 6
done

read -n1 -p "press any key to continue..."