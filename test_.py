import torch
from model import MattingRefine

device = torch.device('cpu')
precision = torch.float32

model = MattingRefine(backbone='torchscript_resnet50_fp32',
                      backbone_scale=0.25,
                      refine_mode='sampling',
                      refine_sample_pixels=80_000)

model.load_state_dict(torch.jit.load('model/TorchScript/torchscript_resnet50_fp32.pth').eval())
model = model.eval().to(precision).to(device)

src = torch.rand(1, 3, 1080, 1920).to(precision).to(device)
bgr = torch.rand(1, 3, 1080, 1920).to(precision).to(device)

with torch.no_grad():
    pha, fgr = model(src, bgr)[:2]
