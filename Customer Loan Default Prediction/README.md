# Customer Loan Default Prediction

## Predictive modeling
Goal is to build a model that predicts a probability that a given customer will default on a loan.

A customer profile consists of a list of bank transactions preceding the loan request. Each transaction is either a debit (money going out of account, negative values) or credit (money coming into account, positive values).

## Customer profile (attributes, 15000 customers total):
* **Id** – id of each customer
* **dates** – dates of each transaction
* **transaction_amount** – numpy array of credits and debits, length varies across different customers (predictions will be primarily based on information in this array)
* **days_before_request** – days before loan request for each transaction loan_amount – amount loaned to customer by bank
* **loan_date** – date of loan

## outcome:
* **isDefault** – did the customer pay back (isDefault=0) or not pay back (isDefault=1)?

*isDefault* is given for the first 10000 customers. The job is to assign a probability to isDefault for the remaining 5000 customers.
Train model on the training data (instances 0 - 9999) and make predictions on the test data (instances 10000- 14,999). The test data is the same format as training data, except it does not contain the isDefault column.


## Algorithm Explanation
In our solution, we used neural network (keras library) to build our model for customer paying back prediction. We set up a 3 dense layers neural network with dropout layers in both visible and hidden layers for regularization. As we have tried most algorithms in scikit-learn library, GradientBoostingClassifier performed best among them. After we carefully chose the hyper-parameters, it provided auc ≅ 0.68 in cross validation on training data (10500 instances). As deep learning is a more result orientated approach, we selected features with higher importance from tree algorithm which is robust to imbalanced data and fed to our neural network as input to reduce the complexity of the architecture. As the original dataset is imbalanced, we passed class weight into the model to adjust the weights for two classes.

## Result Certainty
We have strong confidence in our method, since we have tested most of the algorithms which are provided in scikit-learn library. However, due to time constraint, we couldn’t further tune hyper-parameters for our neural network to achieve better result. Even with GPU acceleration, to grid search the proper hyper-parameter is still a time-consuming job.

## Customers Analysis
As we have analyzed the features, it seems that customers with high average credit amount tend to pay back the loan. Meanwhile, customers with high average debit in recent several transactions are dangerous.

## Best Feature
Average credit amount

## Features Justification
We have included most of the features we can derive from dataset (sum, mean, median, variance, etc.) and we also took total, last quarter, and last 30 transactions into consideration. Standardize can increase the speed and score. Afterwards, we selected important features using SelectFromModel from GradientBoostingClassifier which is the best algorithm we have tested in scikit-learn.
