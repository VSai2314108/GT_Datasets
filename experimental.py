# -*- coding: utf-8 -*-
"""experimental.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14vh5_Y0x8w2r2kroXFFMbrZYeoXckiOz
"""

import torch
from torch import nn
from torch.utils.data import DataLoader

import pandas as pd
device = "cuda" if torch.cuda.is_available() else "cpu"
batch = 2048

df = pd.read_csv("https://raw.githubusercontent.com/VSai2314108/gt_datasets/master/datasetwords.csv")

column_index = {}
for x, y in enumerate(df.columns):
  column_index[y] = x

import numpy as np
days = 512
future_interval = 60
words = 154
feats = 11

class TimeseriesDataset(torch.utils.data.Dataset):   
    def __init__(self, X):
        X = X.to_numpy()[:, 4:].astype("f")
        X[:feats] += 1e-12
        assert np.all(X>=0), X[X<0]
        max_col = torch.tensor(X.max(0, keepdims=True)).to(device)
        self.min_col = torch.tensor(X.min(0, keepdims=True)).to(device)
        self.range = (max_col - self.min_col) + 1e-12
        self.X = torch.tensor(X, device=device)
        assert (self.X >= 0).all()

        assert(np.all(~np.isnan(X)))

    def __len__(self):
        return len(self.X) - days - 1 - future_interval

    def _get_x(self, index):
        this_x = self.X[index:index+days].detach().clone()

        this_x[:, :feats] -= self.min_col[:, :feats]
        this_x[:, :feats] /= self.range[:, :feats]

        assert not torch.any(torch.isnan(this_x))
        return this_x

    def __getitem__(self, index: int):
        this_x = self._get_x(index)

        this_y = ((self.X[index+days+future_interval]-self.min_col[0])[:feats]+1e-12)
        return (this_x, this_y.log())
  

class TimeseriesDatasetForPrediction(TimeseriesDataset):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
    def __len__(self):
        return len(self.X) + 1 - days

    def __getitem__(self, index: int):
        return self._get_x(index)

dataset = TimeseriesDataset(df)

dataset[-10]

from torch.utils.data import DataLoader
train_dataloader = DataLoader(dataset, batch_size=batch, shuffle=True)

list(train_dataloader)

import os
import torch
from torch import nn
from torch.utils.data import DataLoader

device = "cuda" if torch.cuda.is_available() else "cpu"

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 28),
            nn.ReLU(),
            nn.Linear(28, 14),
            nn.ReLU(),
            nn.Linear(14, 10),
        )

    def forward(self, x):
        x = x.view(x.shape[0], -1)
        logits = self.linear_relu_stack(x)
        return logits

net = NeuralNetwork().to(device)

x = torch.randn(23, 28, 28).to(device)

out = net(x)

nn.Linear(10, 11).weight.shape

class NeuralNetwork(nn.Module):
    def __init__(self, feats, days, words):
        super(NeuralNetwork, self).__init__()
        self.days = days
        self.input_dims = feats + words
        self.linear = nn.Linear((feats+words)*days, feats)

    def forward(self, x):
        x = x.reshape(-1, self.days * self.input_dims)
        return self.linear(x)

net = NeuralNetwork(feats, days, words).to(device)
for (x, y) in train_dataloader:
  assert y.shape == net(x).shape, [y.shape, net(x).shape]

df.columns

loss_fn = nn.MSELoss()

optimizer = torch.optim.Adam(net.parameters(), lr = 1e-3)

from tqdm import tqdm

def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    for batch, (X, y) in enumerate(dataloader):
        # Compute prediction and loss
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)


def test_loop(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0

    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= num_batches
    correct /= size

epochs = 1000
for t in tqdm(range(epochs)):
    train_loop(train_dataloader, net, loss_fn, optimizer)
    # test_loop(test_dataloader, model, loss_fn)

f = lambda i: np.arange(days) * (feats + words) + i
f(2)
net.linear.weight.shape
net.linear.weight[:, f(2)]

[net.linear.weight[:, f(i)].detach().abs().mean().item() for i in range(words)]

predictions = []

for (x, y) in tqdm(dataset):
  predictions.append(net(x[None, :]).detach().cpu())

prediction_dataset = TimeseriesDatasetForPrediction(df)
out = net(prediction_dataset[len(prediction_dataset)-1]).exp()
final = out[0].detach().cpu().numpy().tolist()
initial = df.iloc[len(df)-60]
initial = initial.values.tolist()
initial = initial[4:15]
perchg = []
names = ['Consumer Discretionary','Consumer Staples','Energy','Financials','Health','Industrials','Materials','Technology','Utilities','Communication Services','Real Estate']
for ind,elem in enumerate(initial):
  out = (final[ind]-elem)/elem
  out = round(out,2)
  perchg.append({'name': names[ind], 'percent': out, 'type':'2'})
perchg = perchg[::-1]

import json
with open('final_predictions.json', 'w') as fp:
    json.dump(perchg,fp)