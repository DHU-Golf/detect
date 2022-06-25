my_env
$items = Get-ChildItem 'C:\Users\ao\Desktop\detect\data\video_raw'
foreach ($item in $items) {
    echo "video $item"
#   python C:\Users\ao\Desktop\detect\data\anime.py C:\Users\ao\Desktop\detect\data\3d_point\PE4.mp4.npy C:\Users\ao\Desktop\detect\data\3d_point\$item C:\Users\ao\Desktop\detect\data\example\video\ PE4-1-b
    python C:\Users\ao\Desktop\detect\data\tool\anime.py C:\Users\ao\Desktop\detect\data\3d_point\191.mp4.npy "C:\Users\ao\Desktop\detect\data\3d_point\$item.npy" "R:\"  "PE4-$item-new"
}
pause