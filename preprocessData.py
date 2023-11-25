import os
#from PIL import Image
import torch
import csv
#from transformers import YolosForObjectDetection, YolosImageProcessor
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

# Predict if x^k_i is 1 or 0
# with open("data/res/chi/chi.csv", "w+") as f:
#     writer = csv.writer(f)
#     xs = []
#     ys = []
#     # (8, 77, 8), (1, 77, 8)
#     for x, y in val_loader.dataset:
#         x1 = x.tolist()
#         y1 = y.tolist()
#         xs.append(x1)
#         ys.append(y1)
    
#     xs = np.array(xs).astype(int)
#     ys = np.array(ys).astype(int)

#     xs = np.transpose(xs, (2, 3, 0, 1))
#     ys = np.transpose(ys, (2, 3, 0, 1))

#     for i in range(77):
#         for j in range(8):
#             for k in range(8):
#                 x2 = xs[i][j][k]
#                 y2 = ys[i][j][k]
#                 row = y2.tolist() + x2.tolist()
#                 writer.writerow(row)
            #row = y2.tolist() + x2.tolist()
            #writer.writerow(row)
        # x1 = np.transpose(x1, (2, 1, 0))
        # y1 = np.transpose(y1, (2, 1, 0))

        # for i in range(8):
        #     for j in range(77):
        #         x2 = x1[i][j]
        #         y2 = y1[i][j]
        #         row = y2.tolist() + x2.tolist()
        #         writer.writerow(row)
        # print(f"X: {x.shape}, Y: {y.shape}")
# for x, y in train_loader.dataset:
#     x1 = x.tolist()
#     y1 = y.tolist()
#     print(f"X: {x.shape}, Y: {y.shape}")

print()
