# -*- coding: utf-8 -*-
"""
Created on Thu Oct 03 19:16:28 2013

@author: Administrator
"""

# cad60 dataset helper, reorganize the rgbd images
import os
import cv2

root_dir = 'E:\\Liyalong\\rgbd_datas'

data_id = ('1', '2', '3', '4')

rgb_des_root = 'D:\\Liyalong\\datasets\\rgb'
depth_des_root = 'D:\\Liyalong\\datasets\\depth'

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
        else:
                    
            # create a new action type folder and sub folder named '1'
            os.mkdir(rgb_des_curr)
            depth_des_curr = rgb_des_curr.replace('rgb', 'depth')
            os.mkdir(depth_des_curr)
                    
            rgb_des_curr = os.path.join(rgb_des_curr, '1')
            depth_des_curr = os.path.join(depth_des_curr, '1')
        
        # RGB images and Depth Images are in the same file
        rgbd_images_count = len(os.listdir(rgbd_src_curr)) / 2
        
        for i in range(1, rgbd_images_count + 1):
            rgb_img_name = os.path.join(rgbd_src_curr,
            'RGB_' + str(i) + '.png')
            depth_img_name = rgb_img_name.replace('RGB', 'Depth')
            
            rgb_img = cv2.imread(rgb_img_name, cv2.CV_LOAD_IMAGE_COLOR)
            depth_img = cv2.imread(depth_img_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            
            try:
                rgb_img = cv2.resize(rgb_img, (80, 60))
                depth_img = cv2.resize(depth_img, (80, 60))
            except:
                print activity_labels
                print activity_label
                print activity_id
                print rgb_img_name

                exit(1)                
                
            rgb_img_res_name = os.path.join(rgb_des_curr, str(i) + '.png')
            depth_img_res_name = os.path.join(depth_des_curr, str(i) + '.png')
            
            cv2.imwrite(rgb_img_res_name, rgb_img)
            cv2.imwrite(depth_img_res_name, depth_img)
            
    print 'finish data i...'

print 'OK...'
            