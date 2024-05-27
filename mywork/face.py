from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
import numpy as np

face_quality_assessment_func = pipeline(Tasks.face_quality_assessment, 'damo/cv_manual_face-quality-assessment_fqa')
img = 'https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/face_recognition_1.png'
face_quality_score = face_quality_assessment_func(img)[OutputKeys.SCORES]
print(f'Face quality score={face_quality_score}')