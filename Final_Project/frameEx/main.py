#!/usr/bin/python 3

"""
Author: Daniel Blanchette
Date: 6/29/2022

Copyright (c) 2002, Daniel Blanchette
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. 
"""
import frameEx as fex

def main():
    # input for demo version
    # ../tst_files/dataFiles/zebrafish_video.avi
    # get user input for video file path
    vidpath = input("please enter the video's file path:")
    # create a directory for image files
    dirpath = input("Please enter a directory path and name:")
    # convert video to .png files
    fex.frame_extractor(vidpath, dirpath)
    # get frames per second
    fex.fps(vidpath)
    frame_tot = fex.count_frames(vidpath)
    print("Total frames in video:", frame_tot)
    
if __name__ == "__main__":
    main()
