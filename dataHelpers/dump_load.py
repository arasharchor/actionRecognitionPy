# -*- coding: utf-8 -*-
"""
Created on Sun Oct 06 15:33:12 2013

@author: Administrator
"""

# data selector and store them using cPickle

import os
import cv2
import cPickle

root_dir = 'D:\\Liyalong\\datasets'
rgb_root_dir = os.path.join(root_dir, 'rgb')
depth_root_dir = os.path.join(root_dir, 'depth')

sample_res_dir = 'F:\\Liyalong\\sample'

def sample_dump():
    # parameters to dump
    frames_need = 7

    action_types = os.listdir(rgb_root_dir)
    type_map_label = []   # using id represent actio type
    label_id = 0

    for action_type in action_types:
        action_type_tmp = action_type.replace(' ', '_')
        
        type_map_label.append((label_id, action_type_tmp))
        label_id += 1

        sample_ids = os.listdir(os.path.join(rgb_root_dir, action_type))

        # store sample in this format:
        # [[id, label, frame_count, [np, np...], [np, np...]]
        sample_res = []
    
        for sample_id in sample_ids:
            rgb_sample_dir = os.path.join(rgb_root_dir, action_type, sample_id)

            rgb_img_frames = []
            depth_img_frames = []        

            # select [frames_nedd] frames with equal separation
            frames_count = len(os.listdir(rgb_sample_dir))

            if frames_count < 10:
                continue

            frames_selected = range(1, frames_count + 1, frames_count // frames_need)
            frames_selected = frames_selected[0:frames_need]

            for img_i in frames_selected:
                rgb_img_name = os.path.join(rgb_sample_dir, str(img_i) + '.png')
                depth_img_name = rgb_img_name.replace('rgb', 'depth')
            
                rgb_img = cv2.imread(rgb_img_name, cv2.CV_LOAD_IMAGE_COLOR)
                depth_img = cv2.imread(depth_img_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            
                rgb_img_frames.append(rgb_img)
                depth_img_frames.append(depth_img)
                
            one_sample = [sample_id, label_id, frames_need, rgb_img_frames, depth_img_frames]
            sample_res.append(one_sample)
    
        action_sample_file = os.path.join(sample_res_dir, action_type_tmp + '.pkl')
        action_sample_file = open(action_sample_file, 'wb')
    
        cPickle.dump(sample_res, action_sample_file)
        print 'dump', action_type_tmp, '...'

    # save action type-label map
    label_file = os.path.join(sample_res_dir, 'label.pkl')
    label_file = open(label_file, 'wb')

    cPickle.dump(type_map_label, label_file)
    print 'OK...'

def sample_load():
    sample_type_names = os.listdir(sample_res_dir)

    all_samples = []    
    
    for sample_type_name in sample_type_names:
        sample_file = open(os.path.join(sample_res_dir, sample_type_name), 'rb')
        sample = cPickle.load(sample_file)
        
        all_samples += sample
        
        print 'load', sample_type_name, 'success...'

    print 'OK...'
    

def main():
    sample_dump()


if __name__ == '__main__':
    main()
