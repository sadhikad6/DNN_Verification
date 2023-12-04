# DNN_Verification

Docker image containing verifiers, models, and properties, and instructions on how to run verifier/s on each model+property

Readme containing

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
|            |Temporal                      |
|            |                              |
|            |                              |

A paragraph explaining the motivation behind the choice of a particular model+property (being different from anything else verified in VNNcomp competitions is a compelling reason -- make sure to avoid verifying something similar to what has been done in VNNComp 2020-2023)

Table of results for each model+property (verified or not, if falsified show the counter-example found, time to produce the result, and a comment/observation on the result )

Summary of findings 

TODO:

Report will have to clearly explain sources of the data+models, how the models were tailored/reimplemented to run through the verifiers - Please follow project instructions on to how to share artifact+verifier to enable reproduction and grading