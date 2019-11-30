from neupy import algorithms
import numpy as np
import pandas as pd
from sklearn import datasets, preprocessing
from sklearn.model_selection import train_test_split
import tensorflow as tf
import matplotlib.pylab as plt
from sklearn.metrics import mean_squared_error
def Find_best_smoothing_factor(x_train, x_test, y_train,y_test):
    list=[]
    for x in np.linspace(0.01, 0.2, 40):
        SmoRMSE={"smoothing_factor":"","rmse":""}
        nn = algorithms.GRNN(std = x, verbose = False)
        nn.train(x_train,y_train)
        y_pred = nn.predict(x_test)
    #     print(x)
        RMSE = np.sqrt(mean_squared_error(y_pred, y_test))
        SmoRMSE["smoothing_factor"]=x
        SmoRMSE["rmse"]=RMSE
        list.append(SmoRMSE)
        SmoRMSE=pd.DataFrame(list)
    plt.plot(SmoRMSE.iloc[:,1],SmoRMSE.iloc[:,0])
    plt.title(" Find best smoothing factor for GRNN ")
    plt.xlabel('smoothing factor')
    plt.ylabel('RMSE')
    plt.show()
    a=SmoRMSE.ix[SmoRMSE["rmse"].idxmin()]
    print(a)
    best_smoothing_factor=a[1:2].values
    return best_smoothing_factor