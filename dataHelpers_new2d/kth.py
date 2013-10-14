# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 23:02:49 2013

@author: yalong.li
"""

# KTH datasets helper
# video file to images list

import my_ulity

import os
import cv2

def kth_video2image():
    gray_des_root_dir = 'H:\\new_datasets_2d\\kth'    
    
    root_dir = 'F:\\new_datasets\\KTH'
    action_types = ('boxing', 'handclapping', 'handwaving',
                    'jogging', 'running', 'walking')
    
    for action_type in action_types:
        action_folder = os.path.join(root_dir, action_type)
        
        samples_names = os.listdir(action_folder)
        for sample_name in samples_names:
            
            # get video path, and read video
            video_path = os.path.join(action_folder, sample_name)
            video_cap = cv2.VideoCapture(video_path)
            
            if not video_cap:
                continue
            
            # create destination folder
            gray_des_curr = os.path.join(gray_des_root_dir, action_type)
            my_ulity.create_des_folder(gray_des_curr)
            
            my_ulity.video2image(video_cap, gray_des_curr)
        
        print 'finished', action_type, 'folder ...'

def main():
    kth_video2image()
    print 'OK...'
    
if __name__ == '__main__':
    main()