from .ARIMA_GRNN_Pre import ARIMA_GRNN_Pre
from .ARIMA_Pre import ARIMA_Pre
def outbreak_prediction(outbreak_index,data,p,d,q,std=0.02,a=["ARIMA-GRNN","ARIMA"]):
    if a=="ARIMA-GRNN":
        outbreak_before=outbreak_index-4
        outbreak_after=outbreak_index+3
        All_prediction_data=[]
        for i in range(outbreak_before,outbreak_after):

            ARIMA_GRNN_data=ARIMA_GRNN_Pre(data=data,outbreak_size=outbreak_after+1,pre_size=i,p=p,d=d,q=q,std=std)
            All_prediction_data.append(ARIMA_GRNN_data)
    if a=="ARIMA":
        outbreak_before=outbreak_index-4
        outbreak_after=outbreak_index+3
        All_prediction_data=[]
        for i in range(outbreak_before,outbreak_after):
            ARIMA_data=ARIMA_Pre(data=data,outbreak_size=outbreak_after+1,pre_size=i,p=p,d=d,q=q)
            All_prediction_data.append(ARIMA_data)

    return All_prediction_data,outbreak_before,outbreak_after

