# -*- coding: utf-8 -*-
"""
Created on Sun Oct 06 15:33:12 2013

@author: Administrator
"""

# data selector and store them using cPickle

import os
import cv2
import cPickle

root_dir = 'F:\\Liyalong\\datasets\\subDataset'
rgb_root_dir = os.path.join(root_dir, 'rgb')
depth_root_dir = os.path.join(root_dir, 'depth')

sample_res_dir = 'F:\\Liyalong\\sample'

def sample_dump():
    action_types = os.listdir(rgb_root_dir)

    for action_type in action_types:
        #sample_ids = os.listdir(os.path.join(rgb_root_dir, action_type))
    
        # store sample in this format:
        # [[id, label, frame_count, [np, np...], [np, np...]]
        sample_res = []
    
    #    for sample_id in sample_ids:
        for dir_i in range(1, 51):
            sample_id = str(dir_i)
            rgb_sample_dir = os.path.join(rgb_root_dir, action_type, sample_id)

            rgb_img_frames = []
            depth_img_frames = []        
        
            for img_i in range(1, 8):
                rgb_img_name = os.path.join(rgb_sample_dir, str(img_i) + '.png')
                depth_img_name = rgb_img_name.replace('rgb', 'depth')
            
                rgb_img = cv2.imread(rgb_img_name, cv2.CV_LOAD_IMAGE_COLOR)
                depth_img = cv2.imread(depth_img_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            
                rgb_img_frames.append(rgb_img)
                depth_img_frames.append(depth_img)
                
            one_sample = [dir_i, action_type, 7, rgb_img_frames, depth_img_frames]
            sample_res.append(one_sample)
    
        action_sample_file = os.path.join(sample_res_dir, action_type + '.pkl')
        action_sample_file = open(action_sample_file, 'wb')
    
        cPickle.dump(sample_res, action_sample_file)

def sample_load():
    sample_type_names = os.listdir(sample_res_dir)

    all_samples = []    
    
    for sample_type_name in sample_type_names:
        sample_file = open(os.path.join(sample_res_dir, sample_type_name), 'rb')
        sample = cPickle.load(sample_file)
        
        all_samples = all_samples + sample
        
        print 'load', sample_type_name, 'success...'

    print 'OK...'
    print all_samples
    
# main
#sample_dump()
sample_load()