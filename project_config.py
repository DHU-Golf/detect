# use your own path for the PROJECT_ROOT

# for Linux
# PROJECT_ROOT = "/home/ao/Desktop/detect/"

# for Mac
# PROJECT_ROOT = "/Users/ao/Desktop/detect/"

# for Windows
PROJECT_ROOT = "C:/Users/ao/Desktop/detect/"


"""
how to run：
1. add project to PYTHONPATH
# for Windows powershell
$env:PYTHONPATH="C:/Users/ao/Desktop/detect"
# for *nix
export PYTHONPATH="/home/ao/Desktop/detect/":$PYTHONPATH

2. or run as a model
cd detect
python -m data.gui.gui
"""

# display the skeleton
gui_show_skeleton = True

# ----------------------
# how to find the hit events

# for gui-model setting
the_hit_method_for_gui = 0

# for non-gui-model setting
the_hit_method_for_out = 1

# DISTANCE
compress_for_gui = True
# -----------------------

# ----------------------
# 3D points setting

# 1. xx_point ori
# 2. xx_point_xx_vis vis

# the_name_of_typeof_3d_pose = '3d_point'
the_name_of_typeof_3d_pose = '3d_point_vis'
# the_name_of_typeof_3d_pose = '3d_point_form_vis'
# the_name_of_typeof_3d_pose = '3d_point_form'
# ----------------------

# ---------------------
# golfdb version setting
# golfdb_ver = 'orig'
golfdb_ver = 'CBAM'
# do not forget to change the file
# --------------------


