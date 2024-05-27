
import cv2
import os
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import numpy as np
from modelscope.outputs import OutputKeys
import logging

from tools.Tools import get_image_var
from tools.Tools import get_file_logger
# 配置日志输出
logging=get_file_logger('', 'face.log')
loggError=get_file_logger('error', 'face_error.log')

source_path = '/Volumes/homepc/matting_goodfaces'
target_path = '/Volumes/homepc/matting_faces'

os.makedirs(target_path, exist_ok=True)
# 批量生成face脸部图片
def face_image(bboxes, i, imagePath,target_path):
    result1 = os.path.split(imagePath)
    file_name = os.path.splitext(result1[1])
    for i in range(len(bboxes)):
        bbox = bboxes[i].astype(np.int32)
        # file_path=os.path.join(im_path,'')
        im = cv2.imread(imagePath)
        # [h,w]根据自己图片中目标的位置修改
        x1, y1, x2, y2 = bbox
        width= int(x2-x1)
        heigh = int(y2 -y1)
        if heigh > 80 and width > 100:
            im = im[y1:y2, x1:x2]
            if i==0 :
               save_path_file = os.path.join(target_path, file_name[0][:15] + '.jpg')
            else:
               save_path_file = os.path.join(target_path, file_name[0][:15] + '_' + str(i) + '.jpg')
            if  os.path.exists(save_path_file):
                logging.info(f'{save_path_file}is exit')
                continue
            cv2.imwrite(save_path_file, im)
            if not os.path.exists(save_path_file):
                continue

            image_var = get_image_var(save_path_file)
            if image_var < 100:
                logging.info(f'{save_path_file} image_var:{image_var}')
                os.remove(save_path_file)
                continue
            # file_stats = os.stat(save_path_file)
            # i = i + 1
            # list1 = [result1[1], i - 1, width, heigh, file_stats.st_size, image_var]
            # tup = tuple(list1)
            # datas.append(tup)


face_detection = pipeline(Tasks.face_detection, 'damo/cv_resnet_facedetection_scrfd10gkps')
file_list = os.listdir(source_path)
batch_size = 1000
file_batches = [file_list[i:i+batch_size] for i in range(0, len(file_list), batch_size)]
total =0 
for batch in file_batches:
    for file in batch:
        img_path =os.path.join(source_path, file) 
        try:
             result = face_detection(img_path)
        except Exception as e:
             loggError.error(f" {img_path} face_detection：{e}")
        bboxes = np.array(result[OutputKeys.BOXES])
        if len(bboxes) > 0:
            try : 
               face_image(bboxes, 1, img_path,target_path)
               total+=1
               logging.info(f'第{total}:{img_path} face ')
            except Exception as e:
                    loggError.error(f" {img_path} face_image：{e}")
            
