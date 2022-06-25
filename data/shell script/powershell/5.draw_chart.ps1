my_env
$items = Get-ChildItem 'C:\Users\ao\Desktop\detect\data\video_raw'
foreach ($item in $items) {
    echo "video $item"
    python C:\Users\ao\Desktop\detect\data\draw_chart.py   C:\Users\ao\Desktop\detect\data\example\pic\ "C:\Users\ao\Desktop\detect\data\3d_point\$item.npy" $item
}

pause