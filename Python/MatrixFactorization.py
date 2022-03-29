#import
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import pandas as pd
import numpy as np


#class
class MatrixFactorization:
    def __init__(self, len_r, len_c, num_features, lr, max_epochs) -> None:
        #parameters
        self.max_epochs = max_epochs

        #initilize weight
        self.w_r = nn.Parameter(torch.randn(size=(len_r, num_features)))
        self.w_c = nn.Parameter(torch.randn(size=(num_features, len_c)))

        #create optimizer
        self.optimizer = optim.Adam(params=[self.w_r, self.w_c], lr=lr)

    def loss_function(self, y_pred, y_true):
        return torch.pow(y_pred - y_true, 2)

    def predict(self):
        w_r = self.w_r.cpu().data.numpy()
        w_c = self.w_c.cpu().data.numpy()
        print('predicted:\n', pd.DataFrame(np.dot(w_r, w_c).round(),
                                           dtype=int))

    def check_nan_index(self, data):
        row, col = data.shape
        index = []
        for i in range(row):
            for j in range(col):
                if not torch.isnan(data[i, j]):
                    index.append((i, j))
        self.index = index

    def fit(self, data):
        self.check_nan_index(data=data)
        for epoch in tqdm(range(self.max_epochs)):
            self.optimizer.zero_grad()
            loss = 0
            for (i, j) in self.index:
                y_pred = torch.dot(self.w_r[i, :], self.w_c[:, j])
                loss += self.loss_function(y_pred=y_pred, y_true=data[i, j])
            loss.backward()
            self.optimizer.step()
            print(f'epoch: {epoch+1}, loss: {loss}')


if __name__ == '__main__':
    #parameters
    random_seed = 0
    len_r = 5
    len_c = 4
    num_features = 2
    lr = 1e-1
    max_epochs = 100

    #set random seed
    torch.manual_seed(seed=random_seed)

    #create data
    '''
            c_1	c_2	c_3	c_4
    r_A	    5	3	?	1
    r_B	    4	3	?	1
    r_C	    1	1	?	5
    r_D	    1	?	4	4
    r_E	    ?	1	5	4
    '''
    data = torch.tensor([[5, 3, torch.nan, 1], [4, 3, torch.nan, 1],
                         [1, 1, torch.nan, 5], [1, torch.nan, 4, 4],
                         [torch.nan, 1, 5, 4]])

    #create object
    obj = MatrixFactorization(len_r=len_r,
                              len_c=len_c,
                              num_features=num_features,
                              lr=lr,
                              max_epochs=max_epochs)

    #fit
    obj.fit(data=data)

    #predict
    obj.predict()