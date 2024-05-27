import os
import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained('openbmb/MiniCPM-V-2', trust_remote_code=True, torch_dtype=torch.bfloat16)
model = model.to(device='cuda', dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V-2', trust_remote_code=True)
model.eval()

# 指定目录
directory = '\\\\homenas\\homes\\ycbd\\Photos\\广州\\沙面'

# 列出目录中的所有文件
files = os.listdir(directory)

# 遍历所有文件
for file in files:
    # 检查文件是否为图片
    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        # 构建完整的文件路径
        file_path = os.path.join(directory, file)
        # 打开图片
        image = Image.open(file_path).convert('RGB')
        question = '请用中文对这张图片进行描述'
        msgs = [{'role': 'user', 'content': question}]

        res, context, _ = model.chat(
            image=image,
            msgs=msgs,
            context=None,
            tokenizer=tokenizer,
            sampling=True,
            temperature=0.7
        )
        # 生成标题的提示
        title_prompt = '取一个符合图片的标题'
        title_msgs = [{'role': 'user', 'content': title_prompt}]
        title, context, _ = model.chat(
            image=image,
            msgs=title_msgs,
            context=None,
            tokenizer=tokenizer,
            sampling=True,
            temperature=0.7
        )
        template_info = f"[文件名称：{file}, 描述：'{res}', 标题：'{title}']"
        print(template_info)
