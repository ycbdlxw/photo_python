import shutil
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
import os
from tools.Tools import setup_file_logger
# 配置日志输出
setup_file_logger('', '人像质量.log')

dir_path="/Users/ycbd/photo/faces"
target_path = "/Users/ycbd/photo/nofaces"
target_photo_path = "/Users/ycbd/photo/goodfaces"


# 确保目标目录存在
os.makedirs(target_path, exist_ok=True)
os.makedirs(target_photo_path, exist_ok=True)
face_quality_assessment_func = pipeline(Tasks.face_quality_assessment, 'damo/cv_manual_face-quality-assessment_fqa')
for root, dirs, files in os.walk(dir_path):
    for file in files:
        # 只处理图片文件
        if not file.endswith((".jpg", ".jpeg", ".png", ".bmp")):
            continue
        img_path =os.path.join(dir_path, file) 
        try:
             face_quality_score = face_quality_assessment_func(img_path)[OutputKeys.SCORES]
             shutil.copy2(img_path, target_photo_path)
        except Exception as e:
             target_file_path = os.path.join(target_path, file)
             shutil.copy2(img_path, target_file_path)
        
            

