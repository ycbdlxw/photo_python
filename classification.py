import requests

import gradio as gr
import torch
from timm import create_model
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform

device = "cuda" if torch.cuda.is_available() else "cpu"
# device = "mps" if torch.backends.mps.is_available() else "cpu"

IMAGENET_1k_URL = "https://storage.googleapis.com/bit_models/ilsvrc2012_wordnet_lemmas.txt"
LABELS = requests.get(IMAGENET_1k_URL).text.strip().split('\n')

model = create_model('convnext_tiny.fb_in22k_ft_in1k', pretrained=True) #.to(device)

transform = create_transform(
    **resolve_data_config({}, model=model)
)
model.eval()

def predict_fn(img):
    img = img.convert('RGB')
    img = transform(img).unsqueeze(0)   #.to(device)

    with torch.no_grad():
        out = model(img)
    
    probabilities = torch.nn.functional.softmax(out[0], dim=0)

    values, indices = torch.topk(probabilities, k=5)

    return {LABELS[i]: v.item() for i, v in zip(indices, values)}

iface = gr.Interface(
    fn = predict_fn, 
    inputs = gr.components.Image(type='pil'),   #gr.inputs.Dropdown(choices=["..."], type="value", default="...", label="model")
    outputs='label',    #gr.components.Label()
    # theme=gr.themes.Glass(),
    title="Image classification demo",
    description="<div><center>A ConvNeXt image classification model pretrained on ImageNet-22k and finetuned on ImageNet-1k</center></div>",
    examples=[
        "./examples/917k.jpg",
        "./examples/312t.jpg",
        "./examples/312t2.jpg"
    ]
    )

if __name__ == "__main__":
    iface.launch()