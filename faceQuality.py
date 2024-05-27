
import os
import shutil
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
from tools.Tools import get_file_logger
from filecompare import getMissFile

# 配置日志输出
logging=get_file_logger('', 'face质量.log')
loggError=get_file_logger('error', 'face质量_error.log')
source_path = "/Volumes/homepc/matting_person"
target_good_path = "/Volumes/homepc/matting_goodfaces"
target_noface_path = "/Volumes/homepc/matting_nofaces"

# 确保目标目录存在
os.makedirs(target_good_path, exist_ok=True)
os.makedirs(target_noface_path, exist_ok=True)

# file_list = os.listdir(source_path)
# batch_size = 1000
# file_batches = [file_list[i:i+batch_size] for i in range(0, len(file_list), batch_size)]
total =0 
file_batches = getMissFile()
# 进行人脸质量评估
face_quality_assessment_func = pipeline(Tasks.face_quality_assessment, 'damo/cv_manual_face-quality-assessment_fqa')
    
for file in file_batches:
    # 只处理图片文件
    if not file.endswith((".jpg", ".jpeg", ".png", ".bmp")):
        continue
    
    file_path = os.path.join(source_path, file)
    if not os.path.exists(file_path):
        logging.error(f"{file_path} 不存在")
        continue
    goodface_path = os.path.join(target_good_path, file)
    if not os.path.exists(goodface_path):
        logging.error(f"{goodface_path} 存在,不处理")
        continue
    noface_path = os.path.join(target_noface_path, file)
    try: 
     result = face_quality_assessment_func(file_path)[OutputKeys.SCORES]
    except Exception as e:
        shutil.copy2(file_path, noface_path)
        loggError.error(f"{file_path} error: {e}")
        continue
    # 判断face_quality_score是否小于0.8
    face_quality_score = result[0]
    logging.info(f"{file_path}:score: {face_quality_score}")
    if face_quality_score < 0.8:
        try : 
            shutil.copy2(file_path, noface_path)
            logging.info(f"{file_path}:score: {face_quality_score}，不复制")
        except Exception as e:
            loggError.error(f"读取文件 {file_path} 的人脸质量评估出错：{e}")
    else:
        total +=1
        shutil.copy2(file_path, goodface_path)
        logging.info(f"{file_path}:score: {face_quality_score},{total}复制到{goodface_path} 成功")
       