# -*- coding: utf-8 -*-
"""
Created on Sat Oct 05 16:14:20 2013

@author: Administrator
"""

# MSRA3D-daily-Act3D datasets

import numpy as np
import struct
import cv2

INT_CHUNK_SIZE = 4

def read_depth_map_skl_bin_file_header(f, header):
    '''read depth file header
    '''
    if not f:
        pass
    else:
        header_data = f.read(INT_CHUNK_SIZE * 3)
        header[:] = struct.unpack('@iii', header_data)

def read_depth_map_skl_bin_file_next_frame(f, num_cols, num_rows, depth_img):
    '''read depth frame, ignore the skeleton id
    '''
    if not f:
        pass
    else:
        for i in range(0, num_rows):
            row_data = f.read(INT_CHUNK_SIZE * num_cols)
            skl_data = f.read(num_cols)
            
            
            fmt = '@' + str(num_cols) + 'i'
            depth_img[i, :] = struct.unpack(fmt, row_data)
            
    
def main():
    depth_file_name = 'F:\\Liyalong\\datasets\\MSR3D\\a01_s01_e01_depth.bin'

    cv2.namedWindow('depth_window', cv2.CV_WINDOW_AUTOSIZE)
    
    with open(depth_file_name, 'rb') as f:
        
        # header: num_frames, num_cols, num_rows
        header = [0, 0, 0]
        read_depth_map_skl_bin_file_header(f, header)
        
        depth_img = np.zeros((header[2], header[1]), dtype = 'int32')

        for i in range(0, header[0]):
            read_depth_map_skl_bin_file_next_frame(f, header[1], header[2], depth_img)
            depth_img = depth_img.astype('ubyte')
            cv2.normalize(depth_img, depth_img, 0, 255, cv2.cv.CV_MINMAX)
             
            cv2.imshow('depth_window', depth_img)
            cv2.waitKey(10)

if __name__ == '__main__':
    main()