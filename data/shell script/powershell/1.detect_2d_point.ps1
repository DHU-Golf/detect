my_env
cd "C:\Users\ao\Desktop\detect\VideoPose3D\inference"
python infer_video_d2.py `
    --cfg COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x.yaml `
    --output-dir C:\Users\ao\Desktop\detect\data\2d_point `
    --image-ext mp4 `
    'C:\Users\ao\Desktop\detect\data\video_raw'

pause