# -*- coding: utf-8 -*-
"""
Created on Tue Oct 08 21:24:53 2013

@author: Administrator
"""

import os

def main():
    ''' skel...'''

    root_dir = 'F:\\Liyalong\\datasets\\MSR3D'

    # 16 types of activities, each performed twice with 2 num_subjectss 
    num_activities = 16
    num_subjects = 10
    num_events = 2
    
    activity_skl_file_names = []
    
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
                
                activity_skl_file_name = 'a' + activity_id + '_s' + subject_id + \
                                        '_e0' + str(k) + '_skeleton.txt'
                activity_skl_file_names.append(activity_skl_file_name)
    
    for skl_file_name in activity_skl_file_names:
        skl_file_path = os.path.join(root_dir, skl_file_name)
        skl_des_file_path = skl_file_path.replace('.', '_g.')

        with open(skl_file_path, 'r') as f:
            with open(skl_des_file_path, 'w') as f_des:

                # first line: frames_count, joints_num                
                line = f.readline()
                elements = line.split(' ')
                
                for frame_i in range(1, int(elements[0]) + 1):
                    skl_data_3d = str(frame_i) + ','
                    skl_data_2d = str(frame_i) + ','
                    
                    try:
                        line = f.readline()
                        rows_num = int(line[0:-1])
                    except:
                        #print skl_file_name
                        #print frame_i
                        print line
                        print 'hhhhhh'
                        return
                    
                    # no skeleton detected
                    if rows_num == 0:
                        skl_data_3d = skl_data_3d + '-1,' * 20
                        skl_data_2d = skl_data_3d
                     
                    elif rows_num == 40:
                        for joint_i in range(0, 20):
                            line = f.readline()
                            line = line[0:-2].replace(' ', ',')
                            skl_data_3d = skl_data_3d + line
                            
                            line = f.readline()
                            line = line[0:-2].replace(' ', ',')
                            skl_data_2d = skl_data_2d + line

                    elif rows_num == 80:
                        #print '=====80'
                        for joint_i in range(0, 20):
                            line = f.readline()
                            #print line
                            line = line[0:-2].replace(' ', ',')
                            skl_data_3d = skl_data_3d + line
                            
                            line = f.readline()
                            #print line
                            line = line[0:-2].replace(' ', ',')
                            skl_data_2d = skl_data_2d + line             
                        
                        # skip person 2
                        for joint_i in range(0, 40):
                            f.readline()
                        
                    else:
                        print 'nali..., not 0, 40 or 80...'
                
                    # save one frame
                    f_des.write(skl_data_3d + '\n')
                    f_des.write(skl_data_2d + '\n')

if __name__ == '__main__':
    main()
    print 'OK...'