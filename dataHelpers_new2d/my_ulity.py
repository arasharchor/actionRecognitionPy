# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 23:06:14 2013

@author: yalong.li
"""

# my_ulity.py

import os
import cv2

def create_des_folder(rgb_des_curr):
    '''create a new folder to save rgb_2d images list
    '''
    if os.path.exists(rgb_des_curr):
        # create a new sub-folder to save
        exist_folders_count = len(os.listdir(rgb_des_curr))
        os.mkdir(os.path.join(rgb_des_curr,
                                str(exist_folders_count + 1)))
        rgb_des_curr = os.path.join(rgb_des_curr,
                                str(exist_folders_count + 1))
                    
        
    else:
        # create a new action type folder and sub folder named '1'
        os.mkdir(rgb_des_curr)
        rgb_des_curr = os.path.join(rgb_des_curr, '1')
        os.mkdir(rgb_des_curr)

    return rgb_des_curr
        
def video2image(video_cap, rgb_des_curr):
    ''' video to image list
    '''
    img_count = 0
            
    while True:
        retval, gray_img = video_cap.read()
                
        if retval:
            img_count += 1
                    
            gray_img_des_name = os.path.join(rgb_des_curr,
                                             str(img_count) + '.png')
            cv2.imwrite(gray_img_des_name, gray_img)
        else:
            break
        
if __name__ == '__main__':
    pass