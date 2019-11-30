from .Detection2 import Detection2
from .Detection3 import Detection3
from .PredictionDetection import PredictionDetection
def PAD(ts,p=2,d=0,q=1,a=["ARIMA-GRNN","ARIMA"],pvalue_cusum_k=1.5):
        import datetime,os
        import numpy as np
        time_start=datetime.datetime.now()
        if not os.path.exists("./Outbreak_result/"):
                os.mkdir("./Outbreak_result/")

        if not os.path.exists("./Outbreak_result/History_records/"):
                os.mkdir("./Outbreak_result/History_records/")
        pwd=os.getcwd()  
        os.chdir(pwd+"/Outbreak_result/History_records/")
        Detection3(data=ts,pvalue_cusum_k=pvalue_cusum_k)
        print("Detection Done !!!\n")
        print("Now using {} model prediction,and you may have to wait for 16 hours, so you need to run in the background.".format(a))
        data_pre_all,outbreak_before,outbreak_after=PredictionDetection(data=ts,n=len(ts),p=2,d=0,q=1,a="ARIMA")
        print("Prediction Done !!!\n")
        os.chdir(pwd)
        if not os.path.exists("./Outbreak_result/Prediction/"):
                os.mkdir("./Outbreak_result/Prediction/")
        os.chdir(pwd+"/Outbreak_result/Prediction/")
        np.savetxt('Prediction.txt', data_pre_all, fmt='%s')
        Detection2(data_pre_all=data_pre_all,outbreak_before=outbreak_before,outbreak_after=outbreak_after,pvalue_cusum_k=pvalue_cusum_k)
        time_end=datetime.datetime.now()
        print('time cost',time_end-time_start)
	
