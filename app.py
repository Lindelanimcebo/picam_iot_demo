from picam_iot.image import *
from picam_iot.video import *
from picam_iot.storage import *

import json
import threading

file = open('setup.json')
setup = json.load(file)
local = local_storage(setup['img_local'], setup['vid_local'])
dbx = dropbox_storage(access_token = setup['dbx_access_token'])
vid = video(local.get_videos_dir())

def take_image(name):
    img.capture(name)
    return name

def welcome():
    print("Surveillance System with picam_iot")
    print("Options:")
    print("start<space><name> - start recording a video")
    print("stop - stop recording")
    print("rec<space><duration_in_seconds><space><name> - records a video")
    print("sv - starts surveillance mode")
    print("exit or Ctrl+C to exit")

def main():

    opt = input("Enter option:\n")
    while(opt != "exit"):
        opts = opt.split()
        if opts[0] == "start":
            print("starting video..")
            vid.start(opts[1])
        
        elif opts[0] == "stop":
            vid.stop()
            print("video saved")
        
        elif opts[0] == "rec":
            print("recording video")
            vid.record(opts[2], int(opts[1]))
            print("video saved")
        
        elif opts[0] == "sv":
            print("Enabling Surveillance mode..\nMotion detection videos will be logged to the configured dropbox storage\n Ctrl+C to exit")
            vid.motion_detect(videos = True, dbx = dbx)
        
        elif opt[0] == "exit":
            break
        else:
            print("Enter a valid option:")
        
        opt = input("Enter option:\n")
    


if __name__ == "__main__":
    welcome()
    main()