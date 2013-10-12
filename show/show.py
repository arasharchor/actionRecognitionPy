# -*- coding: utf-8 -*-
"""
Created on Wed Oct 09 21:28:32 2013

@author: Administrator
"""

import cv2
import os

def show():
    ''' show action with rgbd image and skeleton if possible
    '''
    
    JOINT_NUM = 20
    JOINT_2D_NOT_EXIST_FLAG = -1
    
    dataset = 'msra3d'
    root_dir = 'H:\\msra3d'
    rgb_root_dir = os.path.join(root_dir, 'rgb')
    depth_root_dir = os.path.join(root_dir, 'depth')
    skel_root_dir = os.path.join(root_dir, 'skeleton')
    
    action_types = os.listdir(rgb_root_dir)
    
    for action_type in action_types:
        action_sample_ids = os.listdir(os.path.join(rgb_root_dir, action_type))
        
        for sample_id in action_sample_ids:
            rgb_curr_dir = os.path.join(rgb_root_dir, action_type, sample_id)
            depth_curr_dir = rgb_curr_dir.replace('rgb', 'depth')
            skel_curr_dir = rgb_curr_dir.replace('rgb', 'skeleton')

            skel_file_name = os.path.join(skel_curr_dir, 'skeleton.txt')
            
            skel_file = open(skel_file_name)
            
            if not skel_file:
                print 'skeleton file does not exist...'
                return
            
            cv2.namedWindow('rgb_window', cv2.WINDOW_AUTOSIZE)
            cv2.namedWindow('depth_window', cv2.WINDOW_AUTOSIZE)
                
            frame_count = len(os.listdir(rgb_curr_dir))
                
            for frame_i in range(1, frame_count + 1):
                rgb_img_name = os.path.join(rgb_curr_dir,
                                            str(frame_i) + '.png')
                depth_img_name = rgb_img_name.replace('rgb', 'depth')
                    
                rgb_img = cv2.imread(rgb_img_name, cv2.CV_LOAD_IMAGE_COLOR)
                depth_img = cv2.imread(depth_img_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    
                # show skeleton if exist joints with 2d positions
                line_3d = skel_file.readline()
                line_2d = skel_file.readline()
                    
                # line_2d: frame_id,1_x,1_y,1_z,...,20_x,20_y,20_z,'\n'
                frame_id_and_joints_2d = line_2d.split(',')
                joints_2d = frame_id_and_joints_2d[1:-1]
                    
                # check if 2d position exist
                if float(joints_2d[0]) == JOINT_2D_NOT_EXIST_FLAG:
                    pass
                else:
                    # show skeleton joints on rgb image
                    for joint_i in range(0, JOINT_NUM):
                        if dataset == 'msra3d':
                            joint_pos = (int(float(joints_2d[joint_i * 3]) * 320),
                                         int(float(joints_2d[joint_i * 3 + 1]) * 240))
                        else:
                            joint_pos = (int(joints_2d[joint_i * 3]),
                                         int(joints_2d[joint_i * 3 + 1]))
                
                        cv2.circle(depth_img, joint_pos, 3, cv2.cv.CV_RGB(255, 0, 0))
                    
                cv2.imshow('rgb_window', rgb_img)
                cv2.imshow('depth_window', depth_img)
                    
                cv2.waitKey(10)
    

def main():
    show()

if __name__ == '__main__':
    main()
    print 'End of program...'