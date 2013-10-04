# cad120 dataset helper, reorganize the rgbd data

import os
import cv2
#import numpy as np

root_dir = 'D:\\Liyalong\\cad120\\CAD-120\\CAD-120'

subject_ids = ('1', '3', '4', '5')
activity_types = ('arranging_objects', 'cleaning_objects', 'having_meal',
                 'making_cereal', 'microwaving_food', 'picking_objects',
                 'stacking_objects', 'taking_food', 'taking_medicine',
                 'unstacking_objects')

for subject_id in subject_ids:
    for activity_type in activity_types:
        annotation_dir = os.path.join(root_dir, 'Subject' + subject_id + 
        '_annotations', 'Subject' + subject_id + '_annotations', activity_type)
        
        # read activityLabel.txt to get activity ids
#        activityLabel = os.path.join(annotation_dir, 'activityLabel.txt')
#        activity_ids = []
#        
#        with open(activityLabel, 'r') as f:
#            for line in f:
#                index_of_id_end = line.find(',')
#                activity_id = line[0:index_of_id_end]
#                
#                activity_ids.append(activity_id)
        
        # read labeling.txt to get sub-activity label
        # get id and labels pair
        labeling = os.path.join(annotation_dir, 'labeling.txt')
        subactivity_labels = {}
        
        with open(labeling, 'r') as f:
           for line in f:
               items = line.split(',')
               
               subactivity_id = items[0]
               
               # start_frame, end_frame, subactivity_type
               subactivity_annot = (items[1], items[2], items[3])
               
               if subactivity_id in subactivity_labels:
                   subactivity_labels[subactivity_id].append(subactivity_annot)
               else:
                   subactivity_labels[subactivity_id] = [subactivity_annot]
       
        # set RGBD images folder
        rgbd_src_root = os.path.join(root_dir, 'Subject' + subject_id +
        '_rgbd_images', 'Subject' + subject_id + '_rgbd_images',
        activity_type)

        # set destination folder to save
        rgb_des_root = 'D:\\Liyalong\\datasets\\rgb'
        depth_des_root = 'D:\\Liyalong\\datasets\\depth'     
        
        # read activity one by one and save its subactivity to destination file
        for subactivity_id, subactivity_annots in subactivity_labels.iteritems():
            rgbd_src_curr = os.path.join(rgbd_src_root, subactivity_id)
            
            for subactivity_annot in subactivity_annots:
                subactivity_type = subactivity_annot[2]
                
                # find or create destination folders
                rgb_des_curr = os.path.join(rgb_des_root, subactivity_type)
                
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

                start_frame = subactivity_annot[0]
                end_frame = subactivity_annot[1]
                
                result_img_count = 0

                # start resize and save
                for i in range(int(start_frame), int(end_frame) + 1):
                    rgb_img_name = 'RGB_' + str(i) + '.png'
                    rgb_img_name = os.path.join(rgbd_src_curr, rgb_img_name)
                    depth_img_name = rgb_img_name.replace('RGB', 'Depth')
                    
                    rgb_img = cv2.imread(rgb_img_name, cv2.CV_LOAD_IMAGE_COLOR)
                    depth_img = cv2.imread(depth_img_name,
                                           cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    
                    # resize to 60 * 80 (width = 80, height = 60)
                    #rgb_img_res = np.zeros((60, 80))
                    #depth_img_res = np.zeros((60, 80))
                    
                    try:
                        rgb_img = cv2.resize(rgb_img, (80, 60))
                        depth_img = cv2.resize(depth_img, (80, 60))
                    except:
                        print subactivity_labels
                        print subactivity_id
                        print subactivity_annots
                        print subactivity_annot                        
                        print start_frame, end_frame
                        
                        exit(1)
                        
                    # save result images with name '1', '2', ...
                    result_img_count += 1
                    
                    rgb_img_res_name = os.path.join(rgb_des_curr, 
                                str(result_img_count) + '.png')
                    depth_img_res_name = os.path.join(depth_des_curr,
                                str(result_img_count) + '.png')
                    
                    cv2.imwrite(rgb_img_res_name, rgb_img)
                    cv2.imwrite(depth_img_res_name, depth_img)
                