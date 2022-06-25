my_env
$items = Get-ChildItem 'C:\Users\ao\Desktop\detect\data\video_raw'
cd "C:\Users\ao\Desktop\detect\PoseFormer"
foreach ($item in $items) {
       python run_poseformer_vis.py `
       -d custom -k myvideos `
       -c checkpoint `
       --evaluate gt81f.bin `
       --render --viz-subject $item `
       --viz-action custom `
       --viz-camera 0 `
       --viz-video C:\Users\ao\Desktop\detect\data\video_raw\$item `
       --viz-export C:\Users\ao\Desktop\detect\data\3d_point_form\$item `
       --viz-size 6
}

pause