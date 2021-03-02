import torch
from torchvision.transforms.functional import to_tensor, to_pil_image
from PIL import Image

model = torch.jit.load('model/TorchScript/torchscript_resnet50_fp32.pth').eval() 
"""
RuntimeError: Attempting to deserialize object on a CUDA device but torch.cuda.is_available() is False. If you are running on a CPU-only machine, please use torch.load with map_location=torch.device('cpu') to map your storages to the CPU.
"""

# model = torch.load('model/TorchScript/torchscript_resnet50_fp32.pth',map_location ='cpu')

src = Image.open('dataset/img/12.png')
bgr = Image.open('dataset/bgr/12.png')

src = to_tensor(src).unsqueeze(0)
bgr = to_tensor(bgr).unsqueeze(0)

if src.size(2) <= 2048 and src.size(3) <= 2048:
  model.backbone_scale = 1/4
  model.refine_sample_pixels = 80_000
else:
  model.backbone_scale = 1/8
  model.refine_sample_pixels = 320_000

pha, fgr = model(src, bgr)[:2]

com = pha * fgr + (1 - pha) * torch.tensor([120/255, 255/255, 155/255], device='cpu').view(1, 3, 1, 1)

to_pil_image(com[0].cpu())

to_pil_image(pha[0].cpu()).save('result/pha.png')
to_pil_image(fgr[0].cpu()).save('result/fgr.png')
to_pil_image(com[0].cpu()).save('result/com.png')
