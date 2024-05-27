
# Use a pipeline as a high-level helper
from PIL import Image
from transformers import pipeline

img = Image.open("C:\\Users\\ycbd\\Pictures\\IMG_0012.JPG")
classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
classifier(img)
