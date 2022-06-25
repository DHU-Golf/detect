import subprocess as sp
import project_config as cf
def get():
    command = ['ffprobe', '-loglevel', 'error', '-select_streams', 'v:0', '-show_entries', 'stream_tags=rotate', '-of',
                   'default=nw=1:nk=1', '-i', f"{cf.PROJECT_ROOT}data/video_raw/191.mp4"]
    pipe_r = sp.Popen(command, stdout=sp.PIPE, bufsize=-1)

    for line in pipe_r.stdout:
        rotate = line.decode().strip()
        if int(rotate) == 90:
            print("video is rotate")
            is_rotate = True

    command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
               '-show_entries', 'stream=width,height', '-of', 'csv=p=0', r"/home/ao/Desktop/detect/data/video_raw/191.mp4"]
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=-1)
    for line in pipe.stdout:
        w, h = line.decode().strip().split(',')
        print(line.decode().strip().split(','))
        # a error about rotate in VideoPose3d
        if is_rotate==True:
            return int(w), int(h)

w, h = get()
print(w,h)