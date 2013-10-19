# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 23:38:26 2013

@author: yalong.li
"""

# ucf50
import my_ulity
import os
import cv2

def ucf50_video2image():
    rgb_des_root_dir = 'H:\\Datasets\\Action2D\\umdb'
    root_dir = 'D:\\new_datasets\\hmdb'
    
    action_types = os.listdir(root_dir)
    
    for action_type in action_types:
        action_folder = os.path.join(root_dir, action_type)        
            
        samples_names = os.listdir(action_folder)
            
        for sample_name in samples_names:
                
            # get video path, and read video
            video_path = os.path.join(action_folder, sample_name)
            video_cap = cv2.VideoCapture(video_path)
            
            if not video_cap:
                continue
            else:
                
                # create destination folder
                rgb_des_curr = os.path.join(rgb_des_root_dir, action_type)
                rgb_des_curr = my_ulity.create_des_folder(rgb_des_curr)
            
                my_ulity.video2image(video_cap, rgb_des_curr)
        
        print 'finished', action_type, 'folder ...'
                

def main():
    ucf50_video2image()
    print 'OK...'
    
if __name__ == '__main__':
    main()