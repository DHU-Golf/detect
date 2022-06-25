#!/bin/bash
source ~/mypython_env/bin/activate 
export PYTHONPATH=~/Desktop/detect/:$PYTHONPATH

file_path=~/Desktop/detect/data/3d_point
items=$(ls $file_path)
for item in $items
do
    echo "video $item"
    python ~/Desktop/detect/data/tool/mydtw.py ~/Desktop/detect/data/3d_point/$1.mp4.npy ~/Desktop/detect/data/3d_point/$item
done

read -n1 -p "press any key to continue..."

# for warning
# sh 4.mark_all.sh PE4 2>/dev/null 