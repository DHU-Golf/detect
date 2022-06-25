# Automatic DTW-Based Grading for Golf Swing in Sports

![gui](picture/gui.png)

## how to run

```shell
# follow VideoPose3d PoseFormer to download some model weights
# install requirements
pip install -r requirements.txt

# set your path
vim project_config.py

# for GUI
python -m data.gui.gui

# for 2d points visualization
# example (use PE4.mp4)
python -m data.tool.draw_chart data/3d_point_vis/PE4.mp4.npy PE4.mp4

# for analysis see the script folder('data/shell script')
```

## DHU-Golf and data 

```
video -> data/video_raw
grades -> data/grades
hit events label -> data/tag
posture data -> data/3d_point* data/2d_point
```

## model weights

```
# CBAM-SwingNet
data/golfdb/models/split_4_flip+affine_7700.pth.tar
# others to follow VideoPose3d, PoseFormer and SwingNet
```

## results
> PCE of CBAM-SwingNet in golfdb evaluate

| model         | PCE                                      |
| ----- | --------|
| SwingNet | 76.1% (reported in the paper) |
| CBAM-SwingNet | 80.5% (split_4_flip+affine_7700.pth.tar) |

> F1-score for start-end detect (1~396 remove defective video)

|Methods |F1-score-aver|
|---|---|
|SwingNet-based|0.7425|
|distance_threshold-based| 0.7599|
|CBAM-SwingNet-based | 0.779|

> Pearson Correlation Coefficient (distance_threshold + dtw based)

| No.   | mean     | var      | pearson  | p-value |
| ----- | -------- | -------- | -------- | ------- |
| 1~190 | 0.497646 | 0.008536 | -0.21548 | 0.0028  |
| 1~396 | 0.531162 | 0.011472 | -0.15446 | 0.0021  |

For details, see the csv and txt files in the results.



## Acknowledgement

[VideoPose3d](https://github.com/facebookresearch/VideoPose3D)

[PoseFormer](https://github.com/zczcwh/PoseFormer)

[golfdb](https://github.com/wmcnally/golfdb)

[dtw-python](https://pypi.org/project/dtw-python/)
