from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

model_id = 'damo/cv_hrnetv2w32_body-2d-keypoints_image'
body_2d_keypoints = pipeline(Tasks.body_2d_keypoints, model=model_id)
output = body_2d_keypoints('https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/keypoints_detect/000000438862.jpg')

# the output contains poses, scores and boxes
print(output)