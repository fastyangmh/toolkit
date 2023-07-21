#import
from pytorch_lightning import LightningModule
from timm import create_model
import pandas as pd
import numpy as np
from tqdm import tqdm
import torch
from time import time


#class
class Model(LightningModule):
    def __init__(self, model_name, in_chans) -> None:
        super().__init__()
        self.model = create_model(model_name=model_name,
                                  pretrained=False,
                                  in_chans=in_chans)

    def forward(self, x):
        return self.model(x)


if __name__ == '__main__':
    #parameters
    url = 'https://github.com/rwightman/pytorch-image-models/blob/master/results/results-imagenet.csv'
    iteration = 100
    batch_size = 1
    in_chans = 3
    width = 224
    height = 224
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    device_name = torch.cuda.get_device_name().replace(
        ' ', '_') if torch.cuda.is_available() else 'cpu'
    filename = f'model_information_{device_name}.csv'

    #get gpu name if available
    if device == 'cuda':
        device_name = torch.cuda.get_device_name()
    else:
        device_name = 'cpu'

    #load result from timm github
    csv = pd.read_html(io=url)[0].iloc[:, 1:]

    #get models
    models = csv.model.values.tolist()

    #get inference time
    inference_time = {}
    for model_name in tqdm(models):
        temp = []
        try:
            model = Model(model_name=model_name, in_chans=in_chans)
        except:
            print(f'unknow model: {model_name}')
            continue
        if device == 'cuda':
            model = model.cuda()
        model = model.eval()
        for idx in range(iteration):
            x = torch.rand(batch_size, in_chans, width, height)
            if device == 'cuda':
                x = x.cuda()
            with torch.no_grad():
                try:
                    start = time()
                    y = model(x)
                    end = time()
                    temp.append(end - start)
                except:
                    print(
                        f'{model_name} cannot inference by image size {width}x{height}x{in_chans}'
                    )
                    break
        if temp:
            inference_time[model_name] = np.mean(temp)
            print(model_name, inference_time[model_name])
        model = None

    #insert inference time to csv
    csv[f'inference time on {device_name} (image size {width}x{height}x{in_chans})'] = csv[
        'model'].map(inference_time)

    #save csv
    csv.to_csv(filename, index=False)
