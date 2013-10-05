# -*- coding: utf-8 -*-
"""
Created on Fri Oct 04 14:53:22 2013

@author: Administrator
"""

import os
import cv2

rgb_src_root = 'F:\\Liyalong\\datasets\\ACT42_partial\\RGB'
depth_src_root = 'F:\\Liyalong\\datasets\\ACT42_partial\\Depth'

rgb_des_root = 'D:\\Liyalong\\datasets\\rgb'
depth_des_root = 'D:\\Liyalong\\datasets\\depth'

person_ids = os.listdir(depth_src_root)

for person_id in person_ids:
    view_ids = os.listdir(os.path.join(depth_src_root, person_id))
    
    for view_id in view_ids:
        depth_src_work = os.path.join(depth_src_root, person_id, view_id)        
        action_types = os.listdir(depth_src_work)

        for action_type in action_types:
            action_perform_ids = os.listdir(
                                    os.path.join(depth_src_work, action_type))
            
            for action_perform_id in action_perform_ids:
                depth_src_curr = os.path.join(depth_src_work, action_type,
                                              action_perform_id)
#                print depth_src_work
#                print action_type
#                print depth_src_curr
                video_name = action_type + action_perform_id + '_rgb.avi'
                video_path = os.path.join(rgb_src_root, person_id,
                                            view_id, video_name)
                                            
                # find or create destination folders
                rgb_des_curr = os.path.join(rgb_des_root, action_type)
                
                if os.path.exists(rgb_des_curr):
                    
                    # create a new sub-folder to save
                    exist_folders_count = len(os.listdir(rgb_des_curr))
                    os.mkdir(os.path.join(rgb_des_curr,
                                          str(exist_folders_count + 1)))
                    rgb_des_curr = os.path.join(rgb_des_curr,
                                        str(exist_folders_count + 1))
                    
                    # create corresponding depth folder
                    depth_des_curr = rgb_des_curr.replace('rgb', 'depth')
                    os.mkdir(depth_des_curr)
                else:
                    
                    # create a new action type folder and sub folder named '1'
                    os.mkdir(rgb_des_curr)
                    depth_des_curr = rgb_des_curr.replace('rgb', 'depth')
                    os.mkdir(depth_des_curr)
                    
                    rgb_des_curr = os.path.join(rgb_des_curr, '1')
                    depth_des_curr = os.path.join(depth_des_curr, '1')
                    os.mkdir(rgb_des_curr)
                    os.mkdir(depth_des_curr)

                # get name list of depth images
                depth_img_names = os.listdir(depth_src_curr)
                depth_img_names.sort()
                
                # start read action video and depth images
                cap = cv2.VideoCapture(video_path)
                
                if cap.isOpened():
                    img_count = 0
                    
                    while True:
                        retval, rgb_img = cap.read()
                    
                        if retval:
                            depth_img = cv2.imread(
                                os.path.join(depth_src_curr,
                                             depth_img_names[img_count]),
                                                   cv2.CV_LOAD_IMAGE_GRAYSCALE)
                            img_count += 1
                            
                            rgb_img = cv2.resize(rgb_img, (80, 60))
                            depth_img = cv2.resize(depth_img, (80, 60))
                            
                            rgb_des_img_name = os.path.join(rgb_des_curr,
                                            str(img_count) + '.png')
                            depth_des_img_name = os.path.join(depth_des_curr,
                                            str(img_count) + '.png')
                                            
                            cv2.imwrite(rgb_des_img_name, rgb_img)
                            cv2.imwrite(depth_des_img_name, depth_img)
                        else:
                            break
                        
        print 'finished person', person_id, 'view', view_id, '...'
print 'OK...'