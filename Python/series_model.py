# import
import pandas as pd
import numpy as np
import pytorch_lightning as pl
import torch.nn as nn
from typing import Any
import torch
from torch.utils.data import Dataset, DataLoader
from pytorch_lightning.callbacks import ModelCheckpoint
from os.path import join
import warnings
warnings.filterwarnings("ignore")

# class


class MyDataset(Dataset):
    def __init__(self, features, labels) -> None:
        super().__init__()
        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.features)

    def __getitem__(self, index):
        x = self.features[index]
        if self.labels is not None:
            y = self.labels[index]
            return x, y
        else:
            return x


class CrossPartialResidualLayer(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_sizes):
        super().__init__()
        self.base_channels = in_channels[0]
        layers = []
        for in_chan, out_chan, ks in zip(in_channels, out_channels, kernel_sizes):
            layers.append(nn.Conv1d(in_chan, out_chan,
                                    ks, padding=ks//2, bias=False))
            layers.append(nn.ReLU())
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return torch.cat((x[:, :self.base_channels, :], self.layers(x[:, self.base_channels:, :])), 1)


class Flatten(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        return x.view(x.shape[0], -1)


class Net(pl.LightningModule):
    def __init__(self, out_features, lr, data_weight) -> None:
        super().__init__()
        self.model = nn.Sequential(nn.Conv1d(1, 32, 10, bias=False),
                                   CrossPartialResidualLayer(in_channels=[16, 32, 32], out_channels=[
                                                             32, 32, 16], kernel_sizes=[5, 5, 5]),
                                   nn.Conv1d(32, 16, 10, bias=False),
                                   CrossPartialResidualLayer(in_channels=[8, 16, 16], out_channels=[
                                                             16, 16, 8], kernel_sizes=[5, 5, 5]),
                                   nn.AdaptiveMaxPool1d(1),
                                   nn.Conv1d(16, out_features, 1),
                                   nn.ReLU(),
                                   Flatten()
                                   )
        self.lr = lr
        self.loss_function = nn.CrossEntropyLoss(
            weight=torch.Tensor(list(data_weight.values())))
        self.softmax = nn.Softmax(dim=-1)

    def training_forward(self, x):
        return self.model(x)

    def forward(self, x) -> Any:
        return self.softmax(self.model(x))

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=self.lr)
        return optimizer

    def training_step(self, train_batch, batch_idx):
        x, y = train_batch
        y_hat = self.training_forward(x)
        loss = self.loss_function(y_hat, y)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, val_batch, batch_idx):
        x, y = val_batch
        y_hat = self.training_forward(x)
        loss = self.loss_function(y_hat, y)
        self.log('val_loss', loss)

    def test_step(self, test_batch, batch_idx):
        x, y = test_batch
        y_hat = self.training_forward(x)
        loss = self.loss_function(y_hat, y)
        self.log('test_loss', loss)


if __name__ == '__main__':
    # parameters
    random_seed = 0
    data_path = 'Finger_Electromyography_Dataset'
    batch_size = 128
    lr = 0.001
    use_cuda = True if torch.cuda.is_available() else False
    num_workers = 0
    gpus = -1 if use_cuda else 0
    max_epochs = 100
    save_path = 'save/'

    # set random seed
    pl.seed_everything(seed=random_seed)

    # load data and label and classes
    x_train = np.load(join(data_path, 'train/x_train.npy')).astype(np.float32)
    y_train = np.load(join(data_path, 'train/y_train.npy'))
    x_val = np.load(join(data_path, 'val/x_val.npy')).astype(np.float32)
    y_val = np.load(join(data_path, 'val/y_val.npy'))
    x_test = np.load(join(data_path, 'test/x_test.npy')).astype(np.float32)
    y_test = np.load(join(data_path, 'test/y_test.npy'))
    classes = np.loadtxt(join(data_path, 'classes.txt'), dtype=str)
    idx_to_class = {idx: k for idx, k in enumerate(classes)}
    out_features = len(classes)

    # reshape the data
    x_train = x_train[:, None]
    x_val = x_val[:, None]
    x_test = x_test[:, None]

    # calculate data weight
    data_weight = {}
    for idx in idx_to_class.keys():
        data_weight[idx] = sum(y_train == idx)
    data_weight = {c: 1-(data_weight[c]/sum(data_weight.values()))
                   for c in data_weight.keys()}

    # create dataset
    train_set = MyDataset(features=x_train, labels=y_train)
    val_set = MyDataset(features=x_val, labels=y_val)
    test_set = MyDataset(features=x_test, labels=y_test)

    # create data loader
    train_loader = DataLoader(dataset=train_set, batch_size=batch_size,
                              shuffle=True, pin_memory=use_cuda, num_workers=num_workers)
    val_loader = DataLoader(dataset=val_set, batch_size=batch_size,
                            shuffle=False, pin_memory=use_cuda, num_workers=num_workers)
    test_loader = DataLoader(dataset=test_set, batch_size=batch_size,
                             shuffle=False, pin_memory=use_cuda, num_workers=num_workers)

    # create model
    model = Net(out_features=out_features, lr=lr, data_weight=data_weight)

    # create trainer
    trainer = pl.Trainer(callbacks=[ModelCheckpoint(monitor='val_loss', mode='min')],
                         gpus=gpus,
                         max_epochs=max_epochs,
                         check_val_every_n_epoch=1,
                         default_root_dir=save_path)

    # train model
    trainer.fit(model, train_loader, val_loader)

    # test model
    for stage, data_loader in zip(['train data', 'val data'], [train_loader, val_loader]):
        print('the {} test result is:'.format(stage))
        trainer.test(test_dataloaders=data_loader)
        print('\n')
