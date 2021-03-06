# -*- coding: utf-8 -*-
"""HW2_UdayKumarKamalapuram.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dFs_kqJVq6Vjt0AAOtvziAqV01bDaY6H
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from google.colab import files
uploaded = files.upload()

df = pd.read_csv("1644871288_9762487_cleveland-train.csv")
df.head()

df = df.rename(columns = {"heartdisease::category|-1|1": "res"})
df["res"] = df.res.replace(-1,0)
df

# a = pd.get_dummies(df['cp'], prefix = "cp")
# b = pd.get_dummies(df['thal'], prefix = "thal")
# c = pd.get_dummies(df['slope'], prefix = "slope")
# frames = [df, a, b, c]
# df = pd.concat(frames, axis = 1)
# df = df.drop(columns = ['cp', 'thal', 'slope'])
# df

y = df.res.values
x_data = df.drop(['res'], axis = 1)

# from sklearn import preprocessing

# x_data_array = x_data.values #returns a numpy array
# min_max_scaler = preprocessing.MinMaxScaler()
# x_scaled = min_max_scaler.fit_transform(x_data_array)
# x = pd.DataFrame(x_scaled)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# transform data
x = scaler.fit_transform(x_data)

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.2,random_state=0)
#transpose matrices
x_train = x_train.T
y_train = y_train.T
x_test = x_test.T
y_test = y_test.T

print(x_train)

def initialize(dimension):
    weight = np.full((dimension,1),0)
    bias = 0.0
    return weight,bias

def sigmoid(z):
    y_hyp = 1/(1+ np.exp(-z))
    return y_hyp

def gradientCalculation(weight,bias,x_train,y_train):
    y_hyp = sigmoid(np.dot(weight.T,x_train) + bias)
    loss = -(y_train*np.log(y_hyp) + (1-y_train)*np.log(1-y_hyp))
    m = x_train.shape[1]
    cost = (1/m) * np.sum(loss) 
    derWeight = (1/m) *np.dot(x_train,((y_hyp-y_train).T))
    derBias = (1/m)* np.sum(y_hyp-y_train)
    gradients = {"DerWeight" : derWeight, "DerBias" : derBias}
    return cost,gradients

def updateWeights(weight,bias,x_train,y_train,learningRate,iteration):
    costList = []
    index = []
    for i in range(iteration):
        cost,gradients = gradientCalculation(weight,bias,x_train,y_train)
        if(np.all(gradients["DerWeight"]<0.001) and gradients["DerBias"]<0.001):
          print("uday",i)
          break 
        weight = weight - learningRate * gradients["DerWeight"]
        bias = bias - learningRate * gradients["DerBias"]  
        costList.append(cost)
        index.append(i)
    parameters = {"weight": weight,"bias": bias}
    print(gradients["DerWeight"].shape)
    print("Iteration:",iteration)
    print("Cross Entropy Cost:",cost)
    plt.plot(index,costList)
    plt.xlabel("Number of Iteration")
    plt.ylabel("Cross Entropy Cost")
    plt.show()
    return parameters, gradients

from pandas.core.frame import DataFrame
def predictTest(weight,bias,x_test):
    test=[]
    z = np.dot(weight.T,x_test) + bias
    y_head = sigmoid(z)
    
    for i in range(y_head.shape[1]):
        if y_head[0,i] <= 0.5:
            test.append(0)
        else:
            test.append(1)
    return pd.DataFrame(test)

from sklearn.metrics import accuracy_score

def logistic_regression_training(x_train,y_train,x_test,y_test,learningRate,iteration):
    dimension = x_train.shape[0]
    weight,bias = initialize(dimension)
    parameters, gradients = updateWeights(weight,bias,x_train,y_train,learningRate,iteration)
    print("shape", x_test.shape)
    y_prediction = predictTest(parameters["weight"],parameters["bias"],x_test)
    print("Accuracy:",accuracy_score(y_test, y_prediction))
    from sklearn.metrics import classification_report
    print(classification_report(y_test,y_prediction))
    from sklearn.metrics import confusion_matrix
    print(confusion_matrix(y_test,y_prediction))
    sns.heatmap(confusion_matrix(y_test,y_prediction),annot=True, cmap="Blues")
    return parameters
parameters = logistic_regression_training(x_train,y_train,x_test,y_test,0.00001,10000)

lr = LogisticRegression()
lr.fit(x_train.T,y_train.T)
print("Test Accuracy {:.2f}%".format(lr.score(x_test.T,y_test.T)*100))

y_pred = lr.predict(x_test.T)

from sklearn.metrics import accuracy_score

print("Accuracy:",accuracy_score(y_test.T, y_pred))

df_test = pd.read_csv("1644871288_9775174_cleveland-test.csv")
df_test.head()

# a = pd.get_dummies(df_test['cp'], prefix = "cp")
# b = pd.get_dummies(df_test['thal'], prefix = "thal")
# c = pd.get_dummies(df_test['slope'], prefix = "slope")
# frames = [df_test, a, b, c]
# df_test = pd.concat(frames, axis = 1)
# df_test = df_test.drop(columns = ['cp', 'thal', 'slope'])
# df_test

# from sklearn import preprocessing

# df_test_array = df_test.values #returns a numpy array
# min_max_scaler = preprocessing.MinMaxScaler()
# x_scaled_test = min_max_scaler.fit_transform(df_test_array)
# test_x_data = pd.DataFrame(x_scaled_test)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# transform data
test_x_data = scaler.fit_transform(df_test)

test_x_data.T.shape

from pandas.core.frame import DataFrame
def predictTest(weight,bias,x_test):
    test=[]
    z = np.dot(weight.T,x_test) + bias
    y_head = sigmoid(z)
    #y_prediction = np.zeros((1,x_test.shape[1]))
    
    for i in range(y_head.shape[1]):
        if y_head[0,i] <= 0.5:
            test.append("-1")
        else:
            test.append("1")
    #print(y_prediction)
    return pd.DataFrame(test)

test_y_prediction = predictTest(parameters["weight"],parameters["bias"],test_x_data.T)

test_y_prediction

output=open('./assignOut.txt', 'w')

output.write(test_y_prediction.to_string(header=False, index=False))

output.close()