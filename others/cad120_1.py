# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:11:58 2013

@author: Administrator
"""

import os
import shutil
import numpy as np
import cv2
import cPickle

def cad120_f():
    ''' dump rgbd data of cad120'''
    
    root_dir = r'D:\Liyalong\cad120\CAD-120\CAD-120'

    subject_ids = ('1', '2', '3', '4')
    activity_types = ('arranging_objects', 'cleaning_objects', 'having_meal',
                      'making_cereal', 'microwaving_food', 'picking_objects',
                      'stacking_objects', 'taking_food', 'taking_medicine',
                      'unstacking_objects')
                      
    des_root_dir = r'I:\Datasets\Action3D\cad120_new'
    des_root_dir_rgb = os.path.join(des_root_dir, 'rgb')
    des_root_dir_depth = os.path.join(des_root_dir, 'depth')
    
    # create destination folders
    # for activity_type in activity_types:
    #     for subject_id in subject_ids:
    #         os.makedirs(os.path.join(des_root_dir_rgb, activity_type, subject_id))
    #         os.makedirs(os.path.join(des_root_dir_depth, activity_type, subject_id))

    # read data and dump
    for subject_id in subject_ids:
        if subject_id != '4':
            continue

        for activity_type in activity_types:
            if activity_type == 'arranging_objects':
                continue
                
            samples_dir = os.path.join(root_dir, 'Subject' + subject_id +
                '_rgbd_images', 'Subject' + subject_id + '_rgbd_images',
                activity_type)

            samples_ids = os.listdir(samples_dir)
            sample_count = 0

            for sample_id in samples_ids:
                work_dir = os.path.join(samples_dir, sample_id)

                rgbd_img_count = len(os.listdir(work_dir))
                img_count = rgbd_img_count / 2

                sample_rgb = np.empty((img_count, 480, 640), dtype='float32') 

                for img_i in range(1, img_count + 1):
                    rgb_img_name = os.path.join(work_dir, 'RGB_' + str(img_i) + '.png')

                    if os.path.exists(rgb_img_name):
                        rgb_img = cv2.imread(rgb_img_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)

                        sample_rgb[img_i - 1, :, :] = rgb_img / 255.0
                    else:
                        print 'Image file', rgb_img_name, 'missing ...'
                        continue

                # dump
                sample_count += 1

                sample_des_file_rgb = os.path.join(des_root_dir_rgb, activity_type,
                                        subject_id, str(sample_count) + '.pkl')
                sample_des_file_rgb = open(sample_des_file_rgb, 'wb')
        
                cPickle.dump(sample_rgb, sample_des_file_rgb)

                del sample_rgb
                sample_des_file_rgb.close()
                
                ################################################
                # depth 
                # sample_depth = np.empty((img_count, 480, 640), dtype='float32') 

                # for img_i in range(1, img_count + 1):
                #     depth_img_name = os.path.join(work_dir, 'Depth_' + str(img_i) + '.png')

                #     if os.path.exists(depth_img_name):
                #         depth_img = cv2.imread(depth_img_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)

                #         sample_depth[img_i - 1] = depth_img / 1.0
                #     else:
                #         print 'Image file', depth_img_name, 'missing ...'
                #         continue

                # # dump
                # sample_des_file_depth = os.path.join(des_root_dir_depth, activity_type,
                #                         subject_id, str(sample_count) + '.pkl')
                # sample_des_file_depth = open(sample_des_file_depth, 'wb')

                # cPickle.dump(sample_depth, sample_des_file_depth)

                # del sample_depth
                # sample_des_file_depth.close()
                

            print 'finished', subject_id, activity_type, '...'


def main():
    '''main function'''
    
    print 'Start...'
    cad120_f()
    print 'OK...'


if __name__ == '__main__':
    main()