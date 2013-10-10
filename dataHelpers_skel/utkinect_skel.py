# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
E:\Users\Administrator\.spyder2\.temp.py
"""

import os

def main():
    root_dir = 'D:\\Liyalong\\UTKinect\\joints\\joints'    
    skel_files_names = os.listdir(root_dir)
    
    for skel_file_name in skel_files_names:
        skel_file_path = os.path.join(root_dir, skel_file_name)
        skel_file_res_path = skel_file_path[:skel_file_path.find('.')] + '_g.txt'
        #skel_file_res_path = skel_file_path.replace('.', '_g.')
        print 'processing', skel_file_path, '...'    
    
        with open(skel_file_path, 'r') as f:
            with open(skel_file_res_path, 'w') as f_des:
                pre_frame_id = -1
                
                for line in f:
                    
                    # end of file, meaningless line
                    if len(line) < 10:
                        break
                    
                    frame_id, joints = line.split('   ')
                
                    # remove duplicate lines
                    if pre_frame_id == int(frame_id):
                        continue
                
                    # 3d
                    f_des.write(frame_id + ',')
                    f_des.write(joints.replace('  ', ','))
                
                    # 2d, -1
                    f_des.write(frame_id + ',')
                    #f_des.write(joints.replace('  ', ','))
                    f_des.write('-1,' * 20 + '\n')                    
                    
                    pre_frame_id = int(frame_id)
                                
        print 'finished...'
    
if __name__ == '__main__':
    main()
    print 'OK...'

