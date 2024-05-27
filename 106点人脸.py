# numpy >= 1.20
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import cv2
from modelscope.preprocessors.image import LoadImage
from modelscope.utils.cv.image_utils import draw_106face_keypoints
import torch
# print("mps : "+torch.backends.mps.is_built())

model_id = 'damo/cv_mobilenet_face-2d-keypoints_alignment'
face_2d_keypoints = pipeline(Tasks.face_2d_keypoints, model=model_id)
img_path = 'https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/keypoints_detect/test_img_face_2d_keypoints.png'
output = face_2d_keypoints(img_path)

# the output contains point and pose
print(output)
img = LoadImage.convert_to_ndarray(img_path)
cv2.imwrite('faceImg.jpg', img)
img_draw = draw_106face_keypoints('faceImg.jpg', output['keypoints'],output['boxes'])
