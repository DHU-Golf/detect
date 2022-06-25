my_env
$items = Get-ChildItem 'C:\Users\ao\Desktop\detect\data\video_raw'
foreach ($item in $items) {
    echo "video $item"
    python.exe C:\Users\ao\Desktop\detect\data\myDTW.py "C:\Users\ao\Desktop\detect\data\3d_point\$std_name.npy" "C:\Users\ao\Desktop\detect\data\3d_point\$item.npy"
}

pause