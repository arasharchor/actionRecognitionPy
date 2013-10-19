# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 23:38:26 2013

@author: yalong.li
"""

# ucf11
import my_ulity
import os
import cv2

def ucf11_video2image():
    rgb_des_root_dir = 'D:\\Datasets\\Action2D\\ucf11'
    root_dir = 'F:\\new_datasets\\ucf11\\UCF11_updated_mpg\\UCF11_updated_mpg'
    
    action_types = os.listdir(root_dir)
    action_types.sort()
    action_types = action_types[8:]
    
    for action_type in action_types:
        action_folder = os.path.join(root_dir, action_type)        
        
        samples_folders_names = os.listdir(action_folder)
        for sample_folder_name in samples_folders_names:
            if sample_folder_name == 'Annotation':
                continue
            
            samples_names = os.listdir(os.path.join(action_folder,
                                                    sample_folder_name))
            
            for sample_name in samples_names:
                
                # get video path, and read video
                video_path = os.path.join(action_folder, sample_folder_name,
                                          sample_name)
                #print video_path
                video_cap = cv2.VideoCapture(video_path)
            
                if not video_cap:
                    #print video_path
                    continue
            
                # create destination folder
                rgb_des_curr = os.path.join(rgb_des_root_dir, action_type)
                rgb_des_curr = my_ulity.create_des_folder(rgb_des_curr)
            
                my_ulity.video2image(video_cap, rgb_des_curr)
        
        print 'finished', action_type, 'folder ...'
                

def main():
    ucf11_video2image()
    print 'OK...'
    
if __name__ == '__main__':
    main()
