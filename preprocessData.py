'''
Preprocess the data to be used for the verifier
Loads in the combined adjacency and crime matrices and uses AGLSTAN dataloader
to format the data in a 8 x 77 x 8 input matrix with a singular label matrix.
This label cooresponds to the [idx // 77][idx % 8] entry of the crime matrix
'''
import os
import torch
import csv
import numpy as np

import AGLSTAN.code.model.AGLSTAN as AGLSTAN
import AGLSTAN.code.utils.dataloader as dl

# Load from .npy file
data = np.load("AGLSTAN/data/chi/adj_mat.npy")
data = data.astype(int)

with open("data/chi/adj_mat.csv", "w+") as f:        
    writer = csv.writer(f)
    for vec in data:
        writer.writerow(vec)


best_model = torch.load("AGLSTAN/res/chi/best_model.pth", map_location=torch.device('cpu'))
state_dict = best_model['state_dict']
args = best_model['config']
args.data_path = "AGLSTAN/data/chi"
args.res_path = "AGLSTAN/res/chi"
args.device = torch.device('cpu')

loader = dl.DatasetLoader(args)
data, adj, scaler, pos_weight, threshold = loader.get_dataset()
train_loader, val_loader, test_loaders = data

# Predicts the crime matrix which is just the 77 x 8 matrix of communities x crime types
# So we can format data such that we predict each entry of the matrix from the input

with open("data/chi/crime.csv", "w+") as f:
    writer = csv.writer(f)

    # Loops eight times, once for each date t
    for x, y in val_loader.dataset:
        # (8, 77, 8), (1, 77, 8)
        x = np.array(x.tolist()).astype(int).flatten().tolist()
        y = y.tolist()
        for i in range(77):
            for j in range(8):
                row = [int(y[0][i][j])] + x
                writer.writerow(row)