from .Detection3 import Detection3
import pandas as pd
def Detection2(data_pre_all,outbreak_before,outbreak_after,pvalue_cusum_k):
#	Detection={};recent_data={}
	for i,j in zip(range(len(range(outbreak_before,outbreak_after-3))),range(outbreak_before,outbreak_after-3)):
      #      print("检测从第"+str(j)+"数据开始预测的数据")
        #     data_pre=np.append(aba[:j],ARIMA_GRNN_data[i])
		Detection3(data_pre_all[i][:outbreak_after+1],pvalue_cusum_k=pvalue_cusum_k)
		#Detection[str(j)]=DT1;recent_data[str(j)]=RT1
#	df=pd.DataFrame.from_dict(Detection, orient='index')
#	print(df.T)
#	df.T.to_csv("PredictionDetection_output.csv")
#	df1=pd.DataFrame.from_dict(recent_data, orient='index')
	#print(df1.T)
#	df1.T.to_csv("PredictionRecentOutbreak_output.csv")

