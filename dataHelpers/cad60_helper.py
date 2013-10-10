# -*- coding: utf-8 -*-
"""
Created on Thu Oct 03 19:16:28 2013

@author: Administrator
"""

# cad60 dataset helper, reorganize the rgbd images
import os
import cv2
import shutil

root_dir = 'E:\\Liyalong\\rgbd_datas'

data_id = ('1', '2', '3', '4')

rgb_des_root = 'H:\\cad60\\rgb'
depth_des_root = 'H:\\cad60\\depth'
skel_des_root = 'H:\\cad60\\skeleton'

print 'Dataset cad60'
print 'To process data_id, 1, 2, 3, 4'
print 'start...'

for i in data_id:
    work_dir = os.path.join(root_dir, 'data' + i, 'data' + i)
    
    # read activityLabel.txt to find all activities
    activity_labels_path = os.path.join(work_dir, 'activityLabel.txt')    
    activity_labels = []

    with open(activity_labels_path, 'r') as f:
        for line in f:
            items = line.split(',')

            # break out if reaching end
            if len(items) < 2:
                break
            
            # activity_id, activity_type
            activity_labels.append((items[0], items[1]))

    
    for activity_label in activity_labels:
        activity_id = activity_label[0]
        activity_type = activity_label[1]
        
        rgbd_src_curr = os.path.join(work_dir, activity_id)
        
        rgb_des_curr = os.path.join(rgb_des_root, activity_type)
    
        # create destination folder    
        if os.path.exists(rgb_des_curr):

            # create a new sub-folder to save
            exist_folders_count = len(os.listdir(rgb_des_curr))
            os.mkdir(os.path.join(rgb_des_curr,
                                  str(exist_folders_count + 1)))
            rgb_des_curr = os.path.join(rgb_des_curr,
                                str(exist_folders_count + 1))
                                
            # create corresponding depth folder
            depth_des_curr = rgb_des_curr.replace('rgb', 'depth')
            os.mkdir(depth_des_curr)
            
            # create skeleton folder
            skel_des_curr = rgb_des_curr.replace('rgb', 'skeleton')
            os.mkdir(skel_des_curr)
        else:
                    
            # create a new action type folder and sub folder named '1'
            os.mkdir(rgb_des_curr)
            depth_des_curr = rgb_des_curr.replace('rgb', 'depth')
            os.mkdir(depth_des_curr)
            skel_des_curr = rgb_des_curr.replace('rgb', 'skeleton')
            os.mkdir(skel_des_curr)
                    
            rgb_des_curr = os.path.join(rgb_des_curr, '1')
            depth_des_curr = os.path.join(depth_des_curr, '1')
            skel_des_curr = os.path.join(skel_des_curr, '1')
            os.mkdir(rgb_des_curr)
            os.mkdir(depth_des_curr)
            os.mkdir(skel_des_curr)
            
        
        # save skeleton file
        annot_name = os.path.join(skel_des_curr, 'annoation.txt')
        with open(annot_name, 'w') as f_annot:
            f_annot.write('cad60, 320, 240, 320, 240, 1, 1,\n')
            
        
        skel_name = os.path.join(work_dir, activity_id + '_g.txt')
        skel_des_name = os.path.join(skel_des_curr, 'skeleton.txt')
        
        shutil.copy(skel_name, skel_des_name)
        
        # RGB images and Depth Images are in the same file
        rgbd_images_count = len(os.listdir(rgbd_src_curr)) / 2
        
        for i in range(1, rgbd_images_count + 1):
            rgb_img_name = os.path.join(rgbd_src_curr,
            'RGB_' + str(i) + '.png')
            depth_img_name = rgb_img_name.replace('RGB', 'Depth')
            
#            rgb_img = cv2.imread(rgb_img_name, cv2.CV_LOAD_IMAGE_COLOR)
#            depth_img = cv2.imread(depth_img_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
#            
#            try:
#                rgb_img = cv2.resize(rgb_img, (80, 60))
#                depth_img = cv2.resize(depth_img, (80, 60))
#            except:
#                print activity_labels
#                print activity_label
#                print activity_id
#                print rgb_img_name
#
#                exit(1)                
            
            rgb_img_res_name = os.path.join(rgb_des_curr, str(i) + '.png')
            depth_img_res_name = os.path.join(depth_des_curr, str(i) + '.png')

#            cv2.imwrite(rgb_img_res_name, rgb_img)
#            cv2.imwrite(depth_img_res_name, depth_img)
            shutil.copy(rgb_img_name, rgb_img_res_name)
            shutil.copy(depth_img_name, depth_img_res_name)            
            
    print 'finished data', data_id, '...'

print 'OK...'
            