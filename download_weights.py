import torchvision.models as models
import torch
import os

tpath = os.path.join(os.getenv('TORCH_HOME'), 'checkpoints')
os.makedirs(tpath, exist_ok=True)

alexnet = models.alexnet(pretrained=True)
resnet101 = models.resnet101(pretrained=True)
inception_v3 = models.inception_v3(pretrained=True)

torch.save(alexnet, os.path.join(tpath, "alexnet.model"))
torch.save(resnet101, os.path.join(tpath, "resnet101.model"))
torch.save(inception_v3, os.path.join(tpath, "inception_v3.model"))