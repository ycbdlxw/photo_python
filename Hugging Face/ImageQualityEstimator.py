import torch
import torchvision.models as models
import torchvision.transforms as transforms
from transformers import RealESRGAN

from PIL import Image

# 加载 VGG16 模型
model = models.vgg16(pretrained=True)
model.eval()
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

# 将图像张量传递给模型
with torch.no_grad():
    output = model(image_tensor.unsqueeze(0))

# 获取模型的特定输出（例如，特征图）
# 假设我们想要使用 VGG16 的第一个卷积层的特征图来评估图像质量
features = output[0]

# 评估图像质量（这里只是一个示例，你可能需要使用不同的方法来评估图像质量）
# 例如，我们可以计算特征图的平均值和标准差
average_feature = features.mean()
std_feature = features.std()

# 判断是否需要修复
if average_feature < 0.5 or std_feature < 0.5:
    # 清晰修复
    repaired_image = real_esrgan(image_tensor)
    repaired_image = repaired_image.permute(0, 2, 3, 1).cpu().numpy()
    repaired_image = Image.fromarray(repaired_image[0])
    repaired_image.save('C:\\Users\\ycbd\\Pictures\\repaired\\IMG_0009.JPG')
else:
    print("Image quality is good, no need for repair.")
