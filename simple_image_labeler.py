import os
import cv2
import numpy as np
import argparse
import shutil

ap = argparse.ArgumentParser()
ap.add_argument("-i","--input_folder",required=True,help="Path to the input folder")
ap.add_argument("-o","--output_folder",required=True,help="Path to the output folder")
ap.add_argument("-c","--classes",required=True,help="Names of the classes")
ap.add_argument("-k","--keys",required=True,help="Keys to be used for each of the classes")
args = vars(ap.parse_args())

class_raw = args['classes']
class_list = class_raw.split(",")
classes = [a.strip() for a in class_list]
class_cnt = len(classes)
output_folder = args['output_folder']

keys_raw = args['keys']
keys_list = keys_raw.split(",")
keys = [k.strip() for k in keys_list]
keys_cnt = len(keys)

inp_folder_path = args['input_folder']
if os.name == "nt":
    parent_folder = inp_folder_path.split("\\")[-1]
else:
    parent_folder = inp_folder_path.split("/")[-1]

if class_cnt != keys_cnt:
    print("[ERROR] Number of classes and keys not equal. Exiting.") 
else:
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    for c in classes:
        class_dest = os.path.join(output_folder,c)
        if not os.path.isdir(class_dest):
            os.mkdir(class_dest)

    count = 0
    all_images = os.listdir(inp_folder_path)
    for image in all_images:
        file_path = os.path.join(args['input_folder'],image)
        im = cv2.imread(file_path)
        h,w = im.shape[:2]
        max_dim = max(h,w)
        ratio = 500/max_dim
        new_dim = (int(w*ratio),int(h*ratio))
        im = cv2.resize(im,new_dim)
        count+=1
        cv2.imshow("Image {}".format(count),im)
        key = cv2.waitKey(0)
        if key == ord("m"):
            print("Good Bye !")
            cv2.destroyAllWindows()
            break
        for i,c in enumerate(classes):
            if key == ord(keys[i]):
                dest = os.path.join(output_folder,classes[i],parent_folder+"_"+image)
                shutil.copy(file_path,dest)
                cv2.destroyAllWindows()
