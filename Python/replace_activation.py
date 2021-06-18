# import
from timm import create_model
import torch
import torch.nn as nn
import torch.nn.functional as F

# def


def replace_activation(model, source_activation, target_activation):
    for child_name, child in model.named_children():
        if isinstance(child, source_activation):
            setattr(model, child_name, target_activation)
        else:
            replace_activation(
                model=child, source_activation=source_activation, target_activation=target_activation)

# class


class Mish(nn.Module):
    def __init__(self):
        super(Mish, self).__init__()

    def forward(self, x):
        return x * torch.tanh(F.softplus(x))


if __name__ == '__main__':
    model = create_model(model_name='resnet18', features_only=True)
    replace_activation(model=model, source_activation=nn.ReLU,
                       target_activation=Mish())

    x = torch.rand(1, 3, 224, 224)
    y = model(x)
