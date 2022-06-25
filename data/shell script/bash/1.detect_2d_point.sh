#!/bin/bash
my_env
cd ~/Desktop/detect/VideoPose3D/inference
python infer_video_d2.py \
    --cfg COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x.yaml \
    --output-dir ~/Desktop/detect/data/2d_point \
    --image-ext mp4 \
    ~/Desktop/detect/data/video_raw

read -n1 -p "Press any key to continue..."