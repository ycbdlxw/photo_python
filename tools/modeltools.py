import cv2
import os
import numpy as np
from tools.Tools import insert, get_image_var

def check_save_file_exit(filepath):
    result1 = os.path.split(filepath)
    file_name = os.path.splitext(result1[1])


def bboxes_save_image(bboxes, subfile, filepath):
    result1 = os.path.split(filepath)
    file_name = os.path.splitext(result1[1])
    for i in range(len(bboxes)):
        bbox = bboxes[i].astype(np.int32)
        # file_path=os.path.join(im_path,'')
        im = cv2.imread(filepath)
        # [h,w]根据自己图片中目标的位置修改
        x1, y1, x2, y2 = bbox
        width = int(x2 - x1)
        heigh = int(y2 - y1)
        if heigh > 80 and width > 100:
            im = im[y1:y2, x1:x2]
            save_path = result1[0] + '/' + subfile + '/'
            save_path_file = os.path.join(save_path, file_name[0] + '_' + subfile + '_' + str(i) + '.jpg')
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            cv2.imwrite(save_path_file, im)
            if not os.path.exists(save_path_file):
                continue
            image_var = get_image_var(save_path_file)
            if image_var < 100:
                os.remove(save_path_file)
                continue
            print("bboxes save file: " + save_path_file)


def bboxes_save_db(bboxes, filepath, table):
    datas = []
    result1 = os.path.split(filepath)
    for i in range(len(bboxes)):
        bbox = bboxes[i].astype(np.int32)
        # [h,w]根据自己图片中目标的位置修改
        x1, y1, x2, y2 = bbox
        width = int(x2 - x1)
        heigh = int(y2 - y1)
        image_var = get_image_var(filepath)
        file_stats = os.stat(filepath)
        i = i + 1
        list1 = [result1[1], i - 1, width, heigh, file_stats.st_size, image_var]
        tup = tuple(list1)
        datas.append(tup)
    if len(datas) > 0:
        insert(table, "file_name,face_index,width,height,fileSize,rate", datas)
