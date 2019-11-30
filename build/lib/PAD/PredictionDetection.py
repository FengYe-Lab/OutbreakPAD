from .Detection import Detection
from .Prediction import outbreak_prediction
#from .pad import pad
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
def PredictionDetection(data,n,p,d,q,std=0.02,a=["ARIMA-GRNN","ARIMA"]):
 #   Detection={};recent_data={}
##    global data_pre_all#定义全局变量
#    std 是GRNN的最佳平滑因子参数
   #####################################################    预测    ####################################################
    """数据在第n天暴发，所以将n-4前的数据预测第n天的数据以及检测其暴发"""
    if a=="ARIMA-GRNN":
        ARIMA_GRNN_data,outbreak_before,outbreak_after=outbreak_prediction(outbreak_index=n,data=data,p=p,d=d,q=q,std=std,a="ARIMA-GRNN")
        data_pre_all=[]
        for i,j in zip(range(len(range(outbreak_before,outbreak_after-3))),range(outbreak_before,outbreak_after-3)):
 #           print("检测从第"+str(j)+"数据开始预测的数据")
            data_pre=np.append(data[:j],ARIMA_GRNN_data[i])
            data_pre_all.append(data_pre)
#        print("#####################################################    画图  ##################################################")
     #   for i,j in zip(range(len(range(outbreak_before,outbreak_after-3))),range(outbreak_before,outbreak_after-3)):
     #       plt.xlim((outbreak_before-4,outbreak_after+3))
     #       plt.plot(data_pre_all[i],"--",label=str("prediction")+str(j))

     #   plt.plot(data[:outbreak_after+1].values,color="blue",label="origin")
     #   plt.legend()
     #   plt.show()

#####################################################    检测   ####################################################
 #       for i,j in zip(range(len(range(outbreak_before,outbreak_after-3))),range(outbreak_before,outbreak_after-3)):
      #      print("检测从第"+str(j)+"数据开始预测的数据")
 #       #     data_pre=np.append(aba[:j],ARIMA_GRNN_data[i])
 #           DT1,RT1=pad(data_pre_all[i],pvalue_cusum_k=pvalue_cusum_k)
 #           Detection[str(j)]=DT1;recent_data[str(j)]=RT1
    if a=="ARIMA":
        ARIMA_data,outbreak_before,outbreak_after=outbreak_prediction(outbreak_index=n,data=data,p=p,d=d,q=q,a="ARIMA")
        data_pre_all=[]
        for i,j in zip(range(len(range(outbreak_before,outbreak_after-3))),range(outbreak_before,outbreak_after-3)):
 #           print("检测从第"+str(j)+"数据开始预测的数据")
            data_pre=np.append(data[:j],ARIMA_data[i])
            data_pre_all.append(data_pre)

     #   print("######################################    画图  ##################################################")
     #   for i,j in zip(range(len(range(outbreak_before,outbreak_after-3))),range(outbreak_before,outbreak_after-3)):
     #       plt.xlim((outbreak_before-4,outbreak_after))
     #       plt.plot(data_pre_all[i],"--",label=str("prediction")+str(j))

      #  plt.plot(data[:outbreak_after+1].values,color="blue",label="origin")
      #  plt.legend()
      #  plt.show()

#####################################################    检测   ####################################################
  #      for i,j in zip(range(len(range(outbreak_before,outbreak_after-3))),range(outbreak_before,outbreak_after-3)):
     #       print("检测从第"+str(j)+"数据开始预测的数据")
        #     data_pre=np.append(aba[:j],ARIMA_GRNN_data[i])
  #          DT2,RT2=pad(data_pre_all[i][:outbreak_after],pvalue_cusum_k=pvalue_cusum_k)
  #          Detection[str(j)]=DT2;recent_data[str(j)]=RT2
  #  df=pd.DataFrame.from_dict(Detection, orient='index')
  #  print(df.T)
  #  df.T.to_csv("PredictionDetection_output.csv")
  #  df1=pd.DataFrame.from_dict(recent_data, orient='index')
  #  print(df1.T)
  #  df1.T.to_csv("PredictionRecentOutbreak_output.csv")

    return data_pre_all,outbreak_before,outbreak_after
