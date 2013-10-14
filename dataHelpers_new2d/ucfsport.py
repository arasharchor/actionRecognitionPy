# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 23:38:26 2013

@author: yalong.li
"""

# ucf11
import my_ulity
import os
import cv2

def ucfsport_video2image():
    rgb_des_root_dir = 'H:\\new_datasets_2d\\ucfsport'
    root_dir = 'E:\\new_datasets\\ucf_sports_actions\\ucf_sports_actions\\ucf action'
    
    action_types = os.listdir(root_dir)
    
    for action_type in action_types:
        action_folder = os.path.join(root_dir, action_type)        
        
        samples_folders_names = os.listdir(action_folder)
        for sample_folder_name in samples_folders_names:
            
            samples_names = os.listdir(os.path.join(action_folder,
                                                    sample_folder_name))
            
            for sample_name in samples_names:
                if sample_name.find('avi') == -1:
                    continue
                
                # get video path, and read video
                video_path = os.path.join(action_folder, sample_folder_name,
                                          sample_name)
                video_cap = cv2.VideoCapture(video_path)
            
                if not video_cap:
                    continue
            
                # create destination folder
                rgb_des_curr = os.path.join(rgb_des_root_dir, action_type)
                my_ulity.create_des_folder(rgb_des_curr)
            
                my_ulity.video2image(video_cap, rgb_des_curr)
        
        print 'finished', action_type, 'folder ...'
                

def main():
    ucfsport_video2image()
    print 'OK...'
    
if __name__ == '__main__':
    main()