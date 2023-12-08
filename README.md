# DNN_Verification

Docker image containing verifiers, models, and properties, and instructions on how to run verifier/s on each model+property

## To Run

### MN-BAB

`cd mn-bab-verification`  
`source mn-bab-env/bin/activate`  
`export PYTHONPATH=$PYTHONPATH:$PWD`  
`src/verify.py -c configs/SE4ML/AGL-STAN.json [--test_num] [n]`  

### Fairify

## Verified Models and Properties

Table listing each verified model, with its application domain, network type, size (in neurons), input size and type, and the properties verified on the model

|            | AGL-STAN - Chicago Model     |
|------------|------------------------------|
|Domain      |Crime Prediction              |
|Network Type|Graph -> MultiAttention -> FFN|
|Size        |1,892,352                     |
|Input Size  |8 x 77 x 8 matrix             |
|Input Type  |1 (crime happened) or 0       |
|Properties  |Robustness                    |
|            |Adversarial Examples          |
|            |Spatial Invariance            |
|            |                              |
|            |                              |

| Verified Model       | Application Domain | Network Type                 | Size (in  neurons) | Input Size and Type | Properties |
| -------------------- | ------------------ | ---------------------------- | ------------------ | ------------------- | ---------- |
| AGL-Inspired Model 1 | Crime Prediction   | 1-ReLu with Adjacency Matrix | 1176               | 221920 x 20 matrix  | Fairness   |
| AGL-Inspired Model 2 | Crime Prediction   | 2-ReLu with Adjacency Matrix | 2352               | 221920 x 20 matrix  | Fairness   |
| AGL-Inspired Model 3 | Crime Prediction   | 3-ReLu with Adjacency Matrix | 3528               | 221920 x 20 matrix  | Fairness   |
| AGL-Inspired Model 4 | Crime Prediction   | 4-ReLu with Adjacency Matrix | 4704               | 221920 x 20 matrix  | Fairness   |
| AGL-Inspired Model 5 | Crime Prediction   | 5-ReLu with Adjacency Matrix | 5880               | 221920 x 20 matrix  | Fairness   |

## Data and Model Source

The data and model used for this project are from the paper "Spatial-Temporal Attention Network for Crime Prediction with Adaptive Graph Learning" by Mingjie Sun, Pengyuan Zhou, Hui Tian, Yong Liao, and Haiyong Xie. The paper can be found [here](https://link.springer.com/chapter/10.1007/978-3-031-15931-2_54). The data and model can be found [at the this public github repository](https://github.com/Yonoi/AGL-STAN/tree/main). Within this repo, the trained model that is used is found in AGL-STAN/res/chi/best_model.pth. The data used is found in AGL-STAN/data/chi/adj_mat.npy and AGL-STAN/data/chi/crime.npy. The crime and adjacency matrix are combined in AGL-STAN/code/utils/dataloader.py to generate the input data for the model. This data is structured as a &alpha; x 77 x 8 matrix, where &alpha; is the window for previous times to use. The dataloader also provides a 77 x 8 predicted matrix as a corresponding label.

Data specific to MN-BAB verification can be found in data/chi/crime.csv. This csv is simply the output of the dataloader specified above. The first column is the i, j index of the predicted matrix, then rest is the 77 x 8 matrix flattened.

Data specific to Fairify Verification can be found in data/crime/crima.data. This data file is a compressed output of the dataloader that breaks up each entry into it's time, community, category and amount, as well as a 4x4 grid of its nearest neighbors located in the Adjacency columns. Thus, we have (365 * 77 * 8) points of data for 365 days of 77 communites with 8 crime categories each.

### Tailoring the model for the verifiers

For robustness verification, the model was tailored by removing the BatchNorm2D layers that were found. We took the model defined in AGL-STAN/code/model and combined the multiple layers and forward layers in one comprehensive nn.Sequential layer and forward function. MN-BAB does not support BatchNorm2D layers, so we could not map them to their abstract verifier layers. Otherwise, the model was left unchanged. The implementation can be found in mn-bab-verification/src/utilities/loading/network.py in the AglStan class.

In more detail, we can pass in the node embeddings and their weight and bias pools that are stored in the saved model. The AGL layers are simple 77 -> 77 linear layers using the passed in node embeddings, weights, and bias in the forward function. We then define the MultiHeadAttention layer as the q, k, v linear layers with a cooresponding output layer. These are used in the forward function by doing passing in the input to q, k, v layers. We transpose, do matrix multiplication, and softmax the intial q, k, v outputs and pass them through the layers again. This shapes our output which is sent to a simple FFN consisting of a linear, ReLU, and linear layer. We end with a convolution from the 8 x 77 x 8 -> 1 x 77 x 8 crime matrix.

It was noted in our presentation that the number of correct instances was only 10/20. This has since increased with changes made to the mapping within the mn-bab verifier.

For fairness verification, the data was loaded through predefined models that were compatible with the Fairness identifier. This is due to the addition of translating the layers to Z3 solvers in order to verify the problem. Thus, ReLu and their associated Z3ReLu layers were used to create 5 increasingly complex models to test this property. These were run to create .h5 models and their model functions and set-up are described in detail in the utils folder.

## Motivation

A paragraph explaining the motivation behind the choice of a particular model+property (being different from anything else verified in VNNcomp competitions is a compelling reason -- make sure to avoid verifying something similar to what has been done in VNNComp 2020-2023)

## Results

Table of results for each model+property (verified or not, if falsified show the counter-example found, time to produce the result, and a comment/observation on the result )

|            | AGL-STAN - Chicago Model - Robustness                     |
|------------|-----------------------------------------------------------|
|Verified    | Y                                                         |
|Falsified   |                                                           |
|Avg Time    | 1.0699505589225076                                        |
|Comment     | Even with slight perturbation of the data by flipping a   |
|            | few bits, the model still predicts that the crime will    |
|            | happen in the same community.                             |

|            | AGL-STAN - Chicago Model - Spatial Adversarial Example    |
|------------|-----------------------------------------------------------|
|Verified    | N                                                         |
|Falsified   | Instance 2 - For community 1, crimes 1,2 4-8 were set to 1|
|Time        | 1.113703727722168                                         |
|Comment     | We manipulate the surrounding crime stats to see if the   |
|            | model will predict a different crime in that community    |
|            | because there was other crimes happening at the same time |

|            | AGL-STAN - Chicago Model - Spatial Invariance             |
|------------|-----------------------------------------------------------|
|Verified    | Y                                                         |
|Falsified   |                                                           |
|Time        | 1.0985028743743896                                        |
|Comment     | Input data was perturbted such that crime statistics in   |
|            | non-adjacent communities were changed. We expect the model|
|            | to still accurately predict if the crime type would happen|
|            | in that community.                                        |

| Model                | Verified        | Time                                         | Comment/Observation                                                                                  | Counter-Example                                                                                                 |
| -------------------- | --------------- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| AGL-Inspired Model 1 | Unknown         | 612.83 seconds                               | Model was not complex enough for verifiable results                                                  | –                                                                                                               |
| AGL-Inspired Model 2 | Unknown         | 849.15 seconds                               | Model was not complex enough for verifiable results                                                  | –                                                                                                               |
| AGL-Inspired Model 3 | SAT             | 616.43 seconds (159.75 for specific example) | Listed counter-example for partition ID 2; was also SAT for partition ID 3                           | C1: [100.   1.   3.  76.  23.  41.  76.  53.   7.  72.  19.  68.  25.   0.

  64.  68.  43.   0.   0.  26.]<br> |
| AGL-Inspired Model 4 | Primarily UNSAT | 348.56 seconds (33.34 for specific example)  | Model was UNSAT for all partitions except the counter example listed (Partition ID: 1)               | C1: [200.   0.   0.   0.   0.   0.   0.   7.   0.  76.   0.   0.   0.   0.

   0.   0.   0.   0.   0.   0.]     |
| AGL-Inspired Model 5 | Unknown         | 417.07 seconds                               | Model may have been too complex enough for verifiable results or timed out before conclusive results | –                                                                                                               |

## Summary of findings

TODO:

Report will have to clearly explain sources of the data+models, how the models were tailored/reimplemented to run through the verifiers - Please follow project instructions on to how to share artifact+verifier to enable reproduction and grading||
