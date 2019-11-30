import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pylab as plt
import pandas as pd
from .ARIMA_Find_Parameter import *
def ARIMA_Pre(data,outbreak_size,pre_size,p,d,q):
    X = data[:outbreak_size].values
    X = np.array(X, dtype=np.float64)
    # size = int(len(X) * 0.66)
    train, test = X[0:pre_size], X[pre_size:len(X)]
    history = [x for x in train]
    p, q = p_q_Parameter(train)
    predictions = list()
    # print(history)
    for t in range(len(test)):
        model = ARIMA(history, order=(p,0,q))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
#        print('predicted=%f, expected=%f' %(yhat, obs))
    bk_pre=np.append(train,predictions)
    bk=np.append(train,test)
#    plt.xlim(pre_size-2,outbreak_size)
#    plt.plot(bk,"b",label="origin")
#    plt.plot(bk_pre,"r",label="prediction")
#    plt.legend(loc="best")
#    plt.show()
    return bk_pre
