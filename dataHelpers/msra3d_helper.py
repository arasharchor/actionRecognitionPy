# -*- coding: utf-8 -*-
"""
Created on Sat Oct 05 16:14:20 2013

@author: Administrator
"""

# MSRA3D-daily-Act3D datasets

import msra3d_depth_reader as depth_reader
import os
import cv2
import numpy as np
import shutil

def main():
    src_root_dir = 'F:\\Liyalong\\datasets\\MSR3D'
    
#    rgb_des_root = 'D:\\Liyalong\\datasets\\rgb'	
 #   depth_des_root = 'D:\\Liyalong\\datasets\\depth'	
    rgb_des_root = 'H:\\msra3d\\rgb'
    depth_des_root = 'H:\\msra3d\\depth'
    skel_des_root = 'H:\\msra3d\\skeleton'

    activities_types = ['drink', 'eat', 'read book', 'call cellphone',
            'write on a paper', 'use laptop', 'use vacuum cleaner', 'cheer up',
            'sit still', 'toss paper', 'play game', 'lie down on sofa', 'walk',
            'play guitar', 'stand up', 'sit down']

    # 16 types of activities, each performed twice with 2 num_subjectss 
    num_activities = 16
    num_subjects = 10
    num_events = 2
    
    #[(id, file_name), (id, file_name), ...]
    activity_file_annots = []
    
    for i in range(1, num_activities + 1):
        for j in range(1, num_subjects + 1):
            for k in range(1, num_events + 1):
                if i < 10:
                    activity_id = '0' + str(i)
                else:
                    activity_id = str(i)
                
                if j < 10:
                    subject_id = '0' + str(j)
                else:
                    subject_id = str(j)
                
                activity_file_name = 'a' + activity_id + '_s' + subject_id + \
                                        '_e0' + str(k)
                activity_file_annots.append((i, activity_file_name))

    for activity_file_annot in activity_file_annots:                            
        activity_type = activities_types[activity_file_annot[0] - 1]
        activity_file_name = activity_file_annot[1]
        

        #print activity_file_name, activity_type
        #return

        # find or create destination folders
        rgb_des_curr = os.path.join(rgb_des_root, activity_type)
                
        if os.path.exists(rgb_des_curr):
            # create a new sub-folder to save
            exist_folders_count = len(os.listdir(rgb_des_curr))
            os.mkdir(os.path.join(rgb_des_curr, str(exist_folders_count + 1)))
            rgb_des_curr = os.path.join(rgb_des_curr,
                                        str(exist_folders_count + 1))
                    
            # create corresponding depth folder
            depth_des_curr = rgb_des_curr.replace('rgb', 'depth')
            os.mkdir(depth_des_curr)
            
            # create corresponding skeleton folder
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
            
        # save annotation file
        annot_name = os.path.join(skel_des_curr, 'annotation.txt')
        with open(annot_name, 'w') as f_annot:
            f_annot.write('msra3d, 640, 480, 320, 240, 1, 1,\n')
            
        # save skeleton
        skel_file = os.path.join(src_root_dir, activity_file_name +
                                        '_skeleton_g.txt')
        skel_des_file = os.path.join(skel_des_curr, 'skeleton.txt')
        shutil.copy(skel_file, skel_des_file)

        # save rgbd images
        rgb_video_path = os.path.join(src_root_dir, activity_file_name +
        								'_rgb.avi')
        depth_file_path = os.path.join(src_root_dir, activity_file_name +
        								'_depth.bin')

        # start read
        rgb_video = cv2.VideoCapture(rgb_video_path)

        if rgb_video.isOpened():
            with open(depth_file_path, 'rb') as depth_f:
                
                #print rgb_video,
                #print depth_f
                #return
                
                # header = [frames, cols, rows]
                header = [0, 0, 0]
                depth_reader.read_depth_map_skl_bin_file_header(
                            depth_f, header)

                #print header
                #return

                depth_img_tmp = np.zeros((header[2], header[1]), dtype='int32')
                
                for i in range(1, header[0] + 1):
                    retval, rgb_img = rgb_video.read()

                    if retval:
                        depth_reader.read_depth_map_skl_bin_file_next_frame(
                            depth_f, header[1], header[2], depth_img_tmp)
                        
                        cv2.normalize(depth_img_tmp, depth_img_tmp, 0, 255, cv2.cv.CV_MINMAX)
                        depth_img = depth_img_tmp.astype('uint8')

                        #rgb_img = cv2.resize(rgb_img, (80, 60))
                        #depth_img = cv2.resize(depth_img, (80, 60))

                        rgb_des_img_name = os.path.join(rgb_des_curr,
        									str(i) + '.png')  
                        depth_des_img_name = os.path.join(depth_des_curr,
        									str(i) + '.png')

                        cv2.imwrite(rgb_des_img_name, rgb_img)
                        cv2.imwrite(depth_des_img_name, depth_img)
                    else:
                        break
       	rgb_video.release()

       	print 'finished', activity_file_name, '...'

if __name__ == '__main__':

    print 'Dataset Msra3D-daily-Action'
    print 'process 16 types of activities'
    print 'start...'    
    
    main()
    print 'OK...'