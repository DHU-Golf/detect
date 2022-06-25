my_env
$items = Get-ChildItem 'C:\Users\ao\Desktop\detect\data\video_raw'
cd "C:\Users\ao\Desktop\detect\VideoPose3D\"
foreach ($item in $items) {
       python run.py `
       -d custom -k myvideos `
       -arc 3,3,3,3,3 -c checkpoint `
       --evaluate pretrained_h36m_detectron_coco.bin `
       --render --viz-subject $item `
       --viz-action custom `
       --viz-camera 0 `
       --viz-video C:\Users\ao\Desktop\detect\data\video_raw\$item `
       --viz-export C:\Users\ao\Desktop\detect\data\3d_point\$item `
       --viz-size 6
}

pause