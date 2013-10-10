# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:00:25 2013

@author: Administrator
"""

import os
import cv2

# show one action, put the file under action rgb folder

def show_action():
    '''show one action, read rgbd images and skeleton if possible
    '''
    dataset = '213'    
    
    rgb_curr_dir = os.getcwd()
    depth_curr_dir = rgb_curr_dir.replace('rgb', 'depth')
    skel_curr_dir = rgb_curr_dir.replace('rgb', 'skeleton')

    cv2.namedWindow('rgb_window', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('depth_window', cv2.WINDOW_AUTOSIZE)

    skel_file_name = os.path.join(skel_curr_dir, 'skeleton.txt')              
    skel_file = open(skel_file_name, 'r')
              
    frame_count = len(os.listdir(rgb_curr_dir)) - 1
                
    for frame_i in range(1, frame_count + 1):
        rgb_img_name = os.path.join(rgb_curr_dir,
                                    str(frame_i) + '.png')
        depth_img_name = rgb_img_name.replace('rgb', 'depth')
        
                    
        rgb_img = cv2.imread(rgb_img_name, cv2.CV_LOAD_IMAGE_COLOR)
        depth_img = cv2.imread(depth_img_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    
        # show skeleton if exist joints with 2d positions
        if True:
            line_3d = skel_file.readline()
            line_2d = skel_file.readline()
                    
            # line_2d: frame_id,1_x,1_y,1_z,...,20_x,20_y,20_z,'\n'
            frame_id_and_joints_2d = line_2d.split(',')
            joints_2d = frame_id_and_joints_2d[1:-1]
                    
            # check if 2d position exist
            if float(joints_2d[0]) == -1:
                pass
            else:
                # show skeleton joints on rgb image
                for joint_i in range(0, 20):
                    if dataset == 'msra3d':
                        joint_pos = (int(float(joints_2d[joint_i * 3]) * 320),
                                     int(float(joints_2d[joint_i * 3 + 1]) * 240))
                    else:
                        joint_pos = (int(joints_2d[joint_i * 3]),
                                     int(joints_2d[joint_i * 3 + 1]))
                
                    cv2.circle(depth_img, joint_pos, 3, cv2.cv.CV_RGB(255, 0, 0), 3)
                    
        cv2.imshow('rgb_window', rgb_img)
        cv2.imshow('depth_window', depth_img)
                    
        cv2.waitKey(10)    
    

def main():
    show_action()
    print 'End of program...'
    
if __name__ == '__main__':
    main()
    