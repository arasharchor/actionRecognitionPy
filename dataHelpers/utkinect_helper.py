# -*- coding: utf-8 -*-
"""
Created on Thu Oct 03 20:51:47 2013

@author: Administrator
"""

# UTKinect dataset, reorganize the data
# Removed extra blank space and 'NaN' string in actionLabel.txt

import os
import cv2
import numpy as np

root_dir = 'D:\\Liyalong\\UTKinect'
rgb_root_dir = 'D:\\Liyalong\\UTKinect\\RGB\\RGB'
depth_root_dir = 'D:\\Liyalong\\UTKinect\\depth\\depth'
skel_root_dir = 'D:\\Liyalong\\UTKinect\\joints\\joints'

rgb_des_root = 'H:\\utkinect\\rgb'
depth_des_root = 'H:\\utkinect\\depth'
skel_des_root = 'H:\\utkinect\\skeleton'

action_label_path = os.path.join(root_dir, 'actionLabel.txt')
action_labels = {}

print 'Dataset UTKinect'
print 'To process ...'
print 'start...'

# read action label file
with open(action_label_path, 'r') as f:
    for line in f:
        items = line.split(' ')
        
        if len(items) == 1:
            if items[0] == '\n':    # skip empty line            
                continue
            
            # new actions folder
            folder = items[0][:-1]    #remove ending newline character
            action_labels[folder] = []
        else:
            action_type = items[0][:-1]    # remove ending colon
            start_frame = items[1]
            
            if items[2][-1] == '\n':
                end_frame = items[2][:-1]    # remove ending newline character
            else:
                end_frame = items[2]
                
            action_annot = (action_type, start_frame, end_frame)
            
            action_labels[folder].append(action_annot)
        
#        print items
    
#exit(0)

# read rgb image and depth xml file
for folder, action_annots in action_labels.iteritems():
    rgb_src_curr = os.path.join(rgb_root_dir, folder)
    depth_src_curr = os.path.join(depth_root_dir, folder)
    skel_src_curr = os.path.join(skel_root_dir, 'joints_' + folder + '_g.txt')
    
    print folder
#    if folder != 's01_e02':
 #       continue
    
    for action_annot in action_annots:
        action_type = action_annot[0]
        start_frame = action_annot[1]
        end_frame = action_annot[2]
        
        rgb_des_curr = os.path.join(rgb_des_root, action_type)
        
        # create destination folder    
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
            
            skel_des_curr = rgb_des_curr.replace('rgb', 'skeleton')
            os.mkdir(skel_des_curr)
        else:
                    
            # create a new action type folder and sub folder named '1'
            os.mkdir(rgb_des_curr)
            depth_des_curr = rgb_des_curr.replace('rgb', 'depth')
            os.mkdir(depth_des_curr)
            skel_des_curr = rgb_des_curr.replace('rgb', 'skeleton')
            os.mkdir(skel_des_curr)
                    
            rgb_des_curr = os.path.join(rgb_des_curr, '1')
            depth_des_curr = os.path.join(depth_des_curr, '1')
            skel_des_curr = os.path.join(skel_des_curr, '1')
            os.mkdir(rgb_des_curr)
            os.mkdir(depth_des_curr)
            os.mkdir(skel_des_curr)
            
        # save annotation and skeleton
        annot_name = os.path.join(skel_des_curr, 'annoation.txt')
        with open(annot_name, 'w') as f_annot:
            f_annot.write('utkinect, 640, 480, 320, 240, 1, 0,\n')
            

        result_skel_count = 0        

        f = open(skel_src_curr, 'r')        
        
        # save skeleton
        skel_des_name = os.path.join(skel_des_curr, 'skeleton.txt')
        with open(skel_des_name, 'w') as f_des:
            while True:
                line_3d = f.readline()
                line_2d = f.readline()
                curr_frame_id = int(line_3d[0:line_3d.find(',')])
                #print curr_frame_id
                
                if curr_frame_id < int(start_frame):
                    continue
                elif (curr_frame_id >= int(start_frame)) and (curr_frame_id < int(end_frame)):
                    result_skel_count += 1
                    
                    skel_res_line_3d = str(result_skel_count) + \
                                    line_3d[line_3d.find(','):]
                    skel_res_line_2d = str(result_skel_count) + \
                                    line_2d[line_3d.find(','):]
                                    
                    f_des.write(skel_res_line_3d + skel_res_line_2d)
                    continue
                elif curr_frame_id >= int(end_frame):
                    result_skel_count += 1
                    
                    skel_res_line_3d = str(result_skel_count) + \
                                    line_3d[line_3d.find(','):]
                    skel_res_line_2d = str(result_skel_count) + \
                                    line_2d[line_3d.find(','):]
                                    
                    f_des.write(skel_res_line_3d + skel_res_line_2d)
                    f.close()
                    break
                else:
                    print curr_frame_id, start_frame, end_frame
                    print 'parsing error...'
                    exit(1)
        
        f.close()
            
        result_img_count = 0
        
        try:
            start_frame = int(start_frame)
            end_frame = int(end_frame)
        except:
            #print action_labels
            print action_annots
            print action_annot
            print start_frame, end_frame
        
        for i in range((start_frame), (end_frame) + 1):
            rgb_img_name = os.path.join(rgb_src_curr, 'colorImg' + str(i) +
                                '.jpg')
            depth_img_name = os.path.join(depth_src_curr, 'depthImg' + str(i) +
                                '.xml')

            if os.path.exists(rgb_img_name) and os.path.exists(depth_img_name):
                pass
            else:
                continue

            try:                    
                rgb_img = cv2.imread(rgb_img_name, cv2.CV_LOAD_IMAGE_COLOR)
            
                # read xml file and transform type to darray          
                depth_img = cv2.cv.Load(depth_img_name)
                depth_img = cv2.cv.GetMat(depth_img)
                depth_img = np.asarray(depth_img)
            
              #  rgb_img = cv2.resize(rgb_img, (80, 60))
              #  depth_img = cv2.resize(depth_img, (80, 60))
            except:
                print depth_img_name
                #print depth_src_curr
                print action_labels
                exit(1)

            # save result images with name '1', '2', ...
            result_img_count += 1
                    
            rgb_img_res_name = os.path.join(rgb_des_curr, 
                                str(result_img_count) + '.png')
            depth_img_res_name = os.path.join(depth_des_curr,
                                str(result_img_count) + '.png')
                    
            cv2.imwrite(rgb_img_res_name, rgb_img)
            cv2.imwrite(depth_img_res_name, depth_img)
    
    print 'finished', folder, '...'

print 'OK...'