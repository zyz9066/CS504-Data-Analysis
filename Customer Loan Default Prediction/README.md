# Customer Loan Default Prediction

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
