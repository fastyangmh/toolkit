# import
from timm import create_model
from pytorch_lightning import LightningModule
from typing import Any
import torch.nn as nn
import os

# class


class Net(LightningModule):
    def __init__(self, model_name, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.backbone_model = create_model(model_name=model_name)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x) -> Any:
        return self.softmax(self.backbone_model(x))


if __name__ == '__main__':
    models = ['tf_efficientnet_l2_ns', 'tf_efficientnet_b7_ns', 'tf_efficientnet_b6_ns', 'tf_efficientnet_b5_ns', 'tf_efficientnet_b4_ns', 'tf_efficientnet_b3_ns',
              'tf_efficientnet_b2_ns', 'tf_efficientnet_b1_ns', 'tf_efficientnet_b0_ns', 'efficientnet_b3_pruned', 'efficientnet_b2_pruned', 'efficientnet_b1_pruned']
    models_params = {}
    models_flops = {}

    for model_name in models:
        model = Net(model_name=model_name)
        models_params[model_name] = model.summarize().param_nums[0]
    os.system('clear')
    for k in models_params.keys():
        print(k, models_params[k]/1e+6)
