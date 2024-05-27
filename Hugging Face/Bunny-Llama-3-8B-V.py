import torch
import transformers
from modelscope import AutoTokenizer, AutoModelForCausalLM
from modelscope.hub.snapshot_download import snapshot_download
from PIL import Image
import warnings

# disable some warnings
transformers.logging.set_verbosity_error()
transformers.logging.disable_progress_bar()
warnings.filterwarnings('ignore')

# set device
device = 'cuda'  # or cpu
torch.set_default_device(device)

# create model
snapshot_download(model_id='thomas/siglip-so400m-patch14-384')
model = AutoModelForCausalLM.from_pretrained(
    'BAAI/Bunny-Llama-3-8B-V',
    torch_dtype=torch.float16, # float32 for cpu
    device_map='auto',
    trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(
    'BAAI/Bunny-Llama-3-8B-V',
    trust_remote_code=True)

# text prompt
prompt = 'Why is the image funny?'
text = f"A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: <image>\n{prompt} ASSISTANT:"
text_chunks = [tokenizer(chunk).input_ids for chunk in text.split('<image>')]
input_ids = torch.tensor(text_chunks[0] + [-20] + text_chunks[1][1:], dtype=torch.long).unsqueeze(0).to(device)
print(input_ids)

# image, sample images can be found in images folder
image = Image.open('C:\\Users\\ycbd\\Pictures\\icon.jpg')
image_tensor = model.process_images([image], model.config).to(dtype=model.dtype, device=device)
print(image_tensor)
# generate
output_ids = model.generate(
    input_ids,
    images=image_tensor,
    max_new_tokens=100,
    use_cache=True)[0]
print(output_ids)
print(input_ids.shape)
print(tokenizer.decode(output_ids[input_ids.shape[1]:], skip_special_tokens=True).strip())