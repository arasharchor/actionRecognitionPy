# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:11:58 2013

@author: Administrator
"""

import os
import shutil

def cad120_f():
    ''' copy rgbd data of cad120'''
    
    root_dir = r'D:\Liyalong\cad120\CAD-120\CAD-120'

    subject_ids = ('1', '2', '3', '4')
    activity_types = ('arranging_objects', 'cleaning_objects', 'having_meal',
                      'making_cereal', 'microwaving_food', 'picking_objects',
                      'stacking_objects', 'taking_food', 'taking_medicine',
                      'unstacking_objects')
                      
    des_root_dir = r'E:\cad120_new_new'
    
    # create destination folders
    for activity_type in activity_types:
        os.mkdir(os.path.join(des_root_dir, activity_type))
        
#        for subject_id in subject_ids:
#            os.mkdir(os.path.join(des_root_dir, activity_type, subject_id))
    
    
    # loop source folders and copy data
    for subject_id in subject_ids:
        for activity_type in activity_types:
            src_dir = os.path.join(root_dir, 'Subject' + subject_id +
                '_rgbd_images', 'Subject' + subject_id + '_rgbd_images',
                activity_type)
                
            des_dir = os.path.join(des_root_dir, activity_type, subject_id)
            shutil.copytree(src_dir, des_dir)
        
            print 'finished', subject_id, activity_type, '...'
    
    print 'End of program'


def main():
    '''main function'''
    
    print 'Start...'
    cad120_f()
    print 'OK...'


if __name__ == '__main__':
    main()