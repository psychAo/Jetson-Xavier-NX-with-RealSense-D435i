# TODO: 
# 1 muti-source (rgb and depth recording)
# 2 add 'clock' function 

import os
import datetime
import argparse
import cv2
import numpy as np
import pyrealsense2 as rs


def recording_rgb(video_fps, video_path, video_name, video_time, show_window):
    # make path
    os.makedirs(video_path, exist_ok=True)
    store_path = os.path.join(video_path, video_name+"_rgb"+".avi")

    # RealSense settings
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, video_fps)

    # start streaming
    pipeline.start(config)
    
    # fourcc == encoder of the video 
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    # out settings (OpenCV)
    out = cv2.VideoWriter(store_path, fourcc, video_fps, (1280, 720))

    # count the number of total frames
    total_frames_num = video_time * video_fps
    frame_count = 0

    # writing images
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())  # to array
        
        if show_window:
            cv2.imshow('frame', color_image)
        
        out.write(color_image)
        frame_count += 1

        if cv2.waitKey(1) & (frame_count >= total_frames_num):
            break
    
    pipeline.stop()
    out.release()

    if show_window:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # get time
    cur_time = datetime.datetime.now()
    time_str = str(cur_time.year) + '_' + str(cur_time.month) + '_' + str(cur_time.day) + '_' + \
    str(cur_time.hour) + '_' + str(cur_time.minute) + '_' + str(cur_time.second)
    del cur_time

    # video settings
    parser = argparse.ArgumentParser(description="Intel RealSense D435i Video Recorder Based on Python3.6 and cv2")
    parser.add_argument("--path", type=str, default='./videos', help="the path of file folder to store the video")
    parser.add_argument("--vname", type=str, default=time_str, help="the name of video, default using the current date")
    parser.add_argument("--fps", type=int, default=30, help="frame per second")
    parser.add_argument("--time", type=int, default=3, help="duration of the video in seconds")
    parser.add_argument("--show", type=bool, default=False, help="whether to show the video in a window")
    parser.add_argument("--source", type=int, default=0, help="0 for rgb, 1 for depth, 2 for both")
    opts = parser.parse_args()
    print(opts)

    if opts.source == 0:
        recording_rgb(opts.fps, opts.path, opts.vname, opts.time, opts.show)
    
    elif opts.source == 1:
        pass
        # recording_depth()

    elif opts.source == 2:
        pass
        # recording_both()
    
    else:
        print("invalid input of --source argument, 0 for rgb, 1 for depth, 2 for both")


