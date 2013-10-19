# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:48:20 2013

@author: Administrator
"""
# foreground ...

import os
import cv2
import numpy as np

# method 1
# get moving pixles with difference of rgb images
def deal_one_action(rgb_dir_curr):
    # parameters
    MIN_FRAME_COUNT = 8

    depth_dir_curr = rgb_dir_curr.replace('rgb', 'depth')
    skel_dir_curr = rgb_dir_curr.replace('rgb', 'skeleton')
    skel_file_name = os.path.join(skel_dir_curr, 'skeleton.txt')

    # get frames count    
    frames_count_rgb = len(os.listdir(rgb_dir_curr))
    frames_count_depth = len(os.listdir(depth_dir_curr))
    frames_count = min(frames_count_rgb, frames_count_depth)
    
    if frames_count < MIN_FRAME_COUNT:
        return
        
    # window
#    cv2.namedWindow('rgb_window', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('depth_window', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('gray_window', cv2.WINDOW_AUTOSIZE)
#    cv2.namedWindow('gray_diff_window', cv2.WINDOW_AUTOSIZE)
#    cv2.namedWindow('depth_diff_window', cv2.WINDOW_AUTOSIZE) 
#    cv2.namedWindow('mask_window', cv2.WINDOW_AUTOSIZE)

    # read the first frame    
    rgb_img_name = os.path.join(rgb_dir_curr, '1.png')
    depth_img_name = os.path.join(depth_dir_curr, '1.png')
    
    rgb_img = cv2.imread(rgb_img_name, cv2.CV_LOAD_IMAGE_COLOR)
    depth_img = cv2.imread(depth_img_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)

    # save one frame
    rgb_img_pre = rgb_img
    gray_img_pre = gray_img
    depth_img_pre = depth_img
    
    print frames_count
    
    for frame_i in range(2, frames_count + 1):
        
        # read next frame
        rgb_img_name = os.path.join(rgb_dir_curr, str(frame_i) + '.png')
        depth_img_name = os.path.join(depth_dir_curr, str(frame_i) + '.png')
        
        rgb_img = cv2.imread(rgb_img_name, cv2.CV_LOAD_IMAGE_COLOR)
        depth_img = cv2.imread(depth_img_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        
        gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
        
        # calculate gray_diff
        gray_img_diff = gray_img.astype('int32') - gray_img_pre.astype('int32')
        np.abs(gray_img_diff)
        gray_img_diff = gray_img_diff.astype('uint8')
        
        cut_off = gray_img_diff > 20
        gray_img_diff[cut_off] = 0
        cut_off = gray_img_diff < 10
        gray_img_diff[cut_off] = 0
        #body_part = gray_img_diff > 0
#        gray_img_diff[body_part] = 255
      #  cv2.medianBlur(gray_img_diff, 3, gray_img_diff)
     #   cv2.medianBlur(gray_img_diff, 3, gray_img_diff)

        #cv2.normalize(gray_img_diff, gray_img_diff, 0, 255, cv2.cv.CV_MINMAX)
        cv2.imshow('gray_diff_window', gray_img_diff)
        
        #print gray_img_diff.shape
        moving_pixels_indice = gray_img_diff >= 10
        #print depth_img[moving_pixels_indice].shape
        #return
        moving_pixels_count = len(depth_img[moving_pixels_indice])
        moving_pixels_depth_sum = depth_img[moving_pixels_indice].sum()
        
        average_depth = moving_pixels_depth_sum / moving_pixels_count
        delta_depth = 7
        
        print average_depth 
        
        cut_off = depth_img > average_depth + delta_depth
        depth_img[cut_off] = 0
        cut_off = depth_img < average_depth - delta_depth
        depth_img[cut_off] = 0
        
        body_part = depth_img > 0
        depth_img[body_part] = 255

        # calculate depth_diff
#        depth_img_diff = depth_img.astype('int32') - depth_img_pre.astype('int32')
#        np.abs(depth_img_diff)
#        depth_img_diff = depth_img_diff.astype('uint8')
#        
#        delta = depth_img_diff > 5
#        depth_img_diff[delta] = 0
#        
#        delta = depth_img_diff > 2
#        depth_img_diff[delta] = 255
        
#        cv2.imshow('rgb_window', rgb_img)
        cv2.imshow('gray_window', gray_img)
        cv2.imshow('depth_window', depth_img)
        
#        cv2.imshow('rgb_diff_window', rgb_img_diff)
#        cv2.imshow('gray_diff_window', gray_img_diff)
 #       cv2.imshow('depth_diff_window', depth_img_diff)

        k = cv2.waitKey()
        if k == ord('a'):
            cv2.destroyAllWindows()
            return

        # update pre-frame        
        rgb_img_pre = rgb_img
        gray_img_pre = gray_img
        depth_img_pre = depth_img
        
    
    cv2.waitKey()
    cv2.destroyAllWindows()
    print 'End of action...'
    
# method 2
# get moving pixels with difference of depth images
def method2():
    pass

# method
# skeleton
def method3():
    # rgb_img_pre, rgb_img
    # depth_img_pre, depth_img
    # skel = []
    pass          
    

def main():
    rgb_curr_dir = 'F:\\cad120\\rgb\\opening\\1'
    deal_one_action(rgb_curr_dir)

if __name__ == '__main__':
    main()
    print 'End of program...'