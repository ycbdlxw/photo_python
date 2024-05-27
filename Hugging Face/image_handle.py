from matplotlib import transforms
from transformers import DualEncoderModel, ViTFeatureExtractor, ViTForImageClassification, ImageQualityEstimator, RealESRGAN
from PIL import Image
import torch

# 加载模型
quality_estimator = ImageQualityEstimator.from_pretrained("pharmadaddy/image-quality-estimator")
classifier = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")
dual_encoder = DualEncoderModel.from_pretrained("microsoft/ViLT-base")
real_esrgan = RealESRGAN.from_pretrained("ZhangWei2023/RealESRGAN_x4plus")

# 定义预处理函数
def preprocess_image(image):
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])(image)

# 读取图片
image = Image.open('C:\\Users\\ycbd\\Pictures\\IMG_0009.JPG')
image_tensor = preprocess_image(image)

# 质量判断
quality_score = quality_estimator(image_tensor)['score']

# 分类
classification = classifier(image_tensor)

# 生成标题
title = dual_encoder(image_tensor, text='A beautiful sunset')

# 找出模糊的图片
if quality_score < 0.5:  # 假设质量分数小于0.5表示图片模糊
    # 清晰修复
    repaired_image = real_esrgan(image_tensor)
    repaired_image = repaired_image.permute(0, 2, 3, 1).cpu().numpy()
    repaired_image = Image.fromarray(repaired_image[0])
    repaired_image.save('C:\\Users\\ycbd\\Pictures\\repaired\\IMG_0009.JPG')
