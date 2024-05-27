import cv2
import numpy as np
# from tools.model_utils import tools
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

def get_pipeline_obj(mode,img_path,isArray):
    obj = None
    match mode:
        # 如果 mode 的值是 1，则返回一个 human_detection 模型对象；
        # 如果 mode 的值是 2，则返回一个 portrait_matting 模型对象；
        # 如果 mode 的值是 3，则返回一个 image_portrait_enhancement 模型对象；
        # 如果 mode 的值是 4，则返回一个 face_detection 模型对象。
       case 1: obj=pipeline(Tasks.human_detection, model='damo/cv_resnet18_human-detection')
       case 2: obj=pipeline(Tasks.portrait_matting, model='damo/cv_unet_image-matting')
       case 3: obj=pipeline(Tasks.image_portrait_enhancement, model='damo/cv_gpen_image-portrait-enhancement')
       case 4: obj=pipeline(Tasks.face_detection, model='damo/cv_resnet_facedetection_scrfd10gkps')
    result = obj(img_path)
    if isArray :
         return np.array(result[OutputKeys.BOXES])
    else:
         return result[OutputKeys.OUTPUT_IMG]
def get_image(imagePath,bboxes, i):
        bbox = bboxes[i].astype(np.int32)
        im = cv2.imread(imagePath)
        # [h,w]根据自己图片中目标的位置修改
        x1, y1, x2, y2 = bbox
        im = im[y1:y2, x1:x2]
        return im
    

