from diffusers import AutoPipelineForText2Image
import torch
from PIL import Image
        
pipeline = AutoPipelineForText2Image.from_pretrained('dataautogpt3/OpenDalleV1.1', torch_dtype=torch.float16).to('cuda')        
image = pipeline('a cartoon avatar of a spectacle wearing bull with only one pair of small horns, wearing a suit and looking very happy. 3D, clean and simple design').images[0]
image.save("image1.jpg")