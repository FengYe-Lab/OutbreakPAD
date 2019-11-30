#加载模块
from .Detection_Methods  import Kendall_change_point_detection,Pettitt_change_point_detection,\
    Buishand_U_change_point_detection,SNHT_change_point_detection,CUSUM,EWMA,Pvalue_CUSUM
from .Prediction import read_data
from matplotlib.pylab import rcParams
import matplotlib.pylab  as plt
import pandas as pd
rcParams['figure.figsize'] = 15, 6
plt.style.use('ggplot')
def Detection(data,pvalue_cusum_k,start_date="1/1/2014"):
    print("##############  Now Read the file  ####################")
    print("Detecting outbreak data\n")
    print("7 detection methods to detect outbreaks")
    if type(data)==str:#如果data输入为.csv文件路径
        data=read_data(data,start_date=start_date)
        print("Method 1: Mann-Kendall \n")
        MK=Kendall_change_point_detection(data)
        print("Method 2: Pettitt \n")
        Pettitt=Pettitt_change_point_detection(data)
        print("Method 3: Buishand_U_Test \n")
        BUT=Buishand_U_change_point_detection(data)
        print("Method 4: Standard Normal Homogeinity Test \n")
        SNHT=SNHT_change_point_detection(data)
        #if isinstance(data, pd.core.series.Series):
        # data = data.values
        print("Method 5: CUSUM \n")
        CUSUM_Test=CUSUM(data)
        print("Method 6: EWMA \n")
        EWMA_Test=EWMA(data)
        print("Method 7: Pvalue_CUSUM \n")
        Pvalue_CUSUM_Test=Pvalue_CUSUM(data,k=pvalue_cusum_k)
    else:#如果输入data为pandas.core.series.Series
        print("Method 1: Mann-Kendall \n")
        MK=Kendall_change_point_detection(data)
        print("Method 2: Pettitt \n")
        Pettitt=Pettitt_change_point_detection(data)
        print("Method 3: Buishand_U_Test \n")
        BUT=Buishand_U_change_point_detection(data)
        print("Method 4: Standard Normal Homogeinity Test \n")
        SNHT=SNHT_change_point_detection(data)
        #if isinstance(data, pd.core.series.Series):
        # data = data.values
        print("Method 5: CUSUM \n")
        CUSUM_Test=CUSUM(data)
        print("Method 6: EWMA \n")
        EWMA_Test=EWMA(data)
        print("Method 7: Pvalue_CUSUM \n")
        Pvalue_CUSUM_Test=Pvalue_CUSUM(data,k=pvalue_cusum_k)
    Pvalue_CUSUM_Test=list(Pvalue_CUSUM_Test)
    return MK,Pettitt,BUT,SNHT,CUSUM_Test,EWMA_Test,Pvalue_CUSUM_Test 
