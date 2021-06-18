# import
import torch
from pytorch_lightning import LightningModule
from timm import create_model, list_models
from torch import nn
from time import time
from tqdm import tqdm
import numpy as np

# class


class Net(LightningModule):
    def __init__(self, model_name):
        super().__init__()
        self.backbone_model = create_model(
            model_name=model_name, num_classes=10)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        return self.softmax(self.backbone_model(x))


if __name__ == '__main__':
    # parameters
    models_name = list_models(filter='*ns') + list_models(filter='*ghost*') + list_models(
        filter='*dla*')+list_models(filter='*mobile*')+list_models(filter='*csp*')+list_models(filter='*nas*')
    models_name = [v for v in models_name if 'iabn' not in v]
    models_param = {}
    models_time = {k: [] for k in models_name}
    iteration = 100

    #
    for model_name in models_name:
        model = Net(model_name=model_name)
        models_param[model_name] = model.summarize().param_nums[0]

    #
    for model_name in tqdm(models_name):
        model = Net(model_name=model_name).cuda().eval()
        for idx in range(iteration):
            x = torch.rand(1, 3, 224, 224).cuda()
            start = time()
            y = model(x)
            end = time()
            models_time[model_name].append(end-start)

    #
    for model_name in models_name:
        print(model_name, models_param[model_name],
              np.mean(models_time[model_name]))
