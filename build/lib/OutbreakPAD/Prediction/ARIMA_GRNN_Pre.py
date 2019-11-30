import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pylab as plt
from sklearn.metrics import mean_squared_error
import pandas as pd
from .GRNN_Predict_Model import GRNN_Predict_Model
from .read_data import read_data
from .ARIMA_Find_Parameter import *
import warnings
warnings.simplefilter("ignore")
def ARIMA_GRNN_Pre(data,outbreak_size,pre_size,p,d,q,std=0.02):
#    data=read_data(file)
    X = data[:outbreak_size].values
    X = np.array(X, dtype=np.float64)
    # size = int(len(X) * 0.66)
    train, test = X[0:pre_size], X[pre_size:len(X)]
    history = [x for x in train]
    p,q=p_q_Parameter(train)
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
    #     print('predicted=%f, expected=%f' % (yhat, obs))
   ###################################################################
    yeast_bk_pre=np.append(train,predictions)
    yeast_bk=np.append(train,test)
    input_data, output_data =yeast_bk_pre[pre_size-8:],yeast_bk[pre_size-8:]
    ARIMA_GRNN_data=GRNN_Predict_Model(input_data, output_data,std=std)

    ################################################################
    error = mean_squared_error(output_data,ARIMA_GRNN_data)
#    print('Test MSE: %.3f' % error)
#    plt.title("test part")
    output_data=output_data[8:]
    ARIMA_GRNN_data=ARIMA_GRNN_data[8:]
#    plt.plot(output_data,color='green')
#    plt.plot(ARIMA_GRNN_data, color='red')
#    plt.show()
    yeast_bk_pre=np.append(train,ARIMA_GRNN_data)
    yeast_bk=np.append(train,test)
#    for i in range(len(ARIMA_GRNN_data)):
#        print('predicted=%f, expected=%f'%(ARIMA_GRNN_data[i], output_data[i]))
    return ARIMA_GRNN_data
