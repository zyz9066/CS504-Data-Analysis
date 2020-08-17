# Predict disease classes using genetic microarray data

## Objective

The purpose of this project is to develop a method that uses genetic data for disease classification. Data is extracted from a DNA microarray which measures the expression levels of large numbers of genes simultaneously.

Samples in the datasets represent patients. For each patient 7070 genes expressions (values) are measured in order to classify the patient’s disease into one of the following cases: EPD, JPA, MED, MGL, RHB

## Data

Gene data is in genes-in-rows format, comma-separated values. You will find a Zip file named: final_project_data.zip file. Unzip to extract the following 3 files:

* Training dataset: pp5i_train.gr.csv
* Training data classes: pp5i_train_class.txt
* Test dataset: pp5i_test.gr.csv

## Instructions

**Training data**: file pp5i_train.gr.csv, with 7070 genes for 69 samples. A separate file pp5i_train_class.txt has classes for each sample, in the order corresponding to the order of samples in pp5i_train.gr.csv.

**Test data**: file pp5i_test.gr.csv, with 23 **unlabelled** samples and same genes. You can assume that the class distribution is similar.

**Your goal is to learn the best model from the training data and use it to predict the label (class) for each sample in test data.** You will also need to write a paper describing your effort.

Randomization experiments showed that one can get about 10-12 (from 23) correct answers with random guessing.

## Important Hints

Be sure that you don't use the sample number as one of the predictors. Training data is ordered by class, so sample number will appear to be a good predictor on cross- validation, but it will not work on the test data!

One of the MED samples in the training data is very likely misclassified (by a human). So the best result you can expect to get on cross validation is one error (on a MED sample) out of 69. However, this should not affect your accuracy on the test set.
