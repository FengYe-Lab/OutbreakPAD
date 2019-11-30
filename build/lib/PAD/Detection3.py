from .Prediction import *
import re,os
from itertools import groupby
#from operator import itemgetter

from .Detection import Detection
from .PredictionDetection import PredictionDetection
def Tran_time(data,list_a):
    list_a.sort()
    num=[]
    fun = lambda x: x[1]-x[0]
    for k, g in groupby(enumerate(list_a), fun):
        l1 = [j for i, j in g]    # 连续数字的列表
        if len(l1) > 1:
            scop = str(min(l1)) + '-' + str(max(l1))    # 将连续数字范围用"-"连接
        else:
            scop = l1[0]
        num.append(scop)
    #print(num)
    b=[]
#     if len(list_a)>0:
    for i in num:
        if isinstance(i, str):
            scop_=i.split("-")
            scop_time=[]
            for j in scop_:
                tmp=data.index[int(j)-1] 
                scop_time.append(tmp.strftime("%Y/%m/%d"))
            b.append(str(scop_time[0]) + '-' + str(scop_time[1]))
        if isinstance(i, int): 
#         print(i.split("-"))
            tmp=data.index[i-1]
            b.append(tmp.strftime("%Y/%m/%d"))
    return b
def Detection3(data,pvalue_cusum_k):
#    if not os.path.exists("./Outbreak_result"):
#        os.mkdir("./Outbreak_result")

    # data=read_data(file=file)
    MK, Pettitt, BUT, SNHT, CUSUM_Test, EWMA_Test, Pvalue_CUSUM_Test = \
        Detection(data=data, pvalue_cusum_k=pvalue_cusum_k)  # Detection模块中的data参数可以是文件路径，也可以是时间序列数据
    #print("Method 5: CUSUM \n")
    print(CUSUM_Test)
    #print("Method 6: EWMA \n")
    print(EWMA_Test)
    MK=Tran_time(data,MK)
    Pettitt=Tran_time(data,[Pettitt])
    BUT=Tran_time(data,[BUT])
    SNHT=Tran_time(data,[SNHT])
    CUSUM_Test = CUSUM_Test[0]['violation-points'][1]
    CUSUM_Test=Tran_time(data,CUSUM_Test)
    EWMA_Test = EWMA_Test[0]['violation-points'][1]
    EWMA_Test=Tran_time(data,EWMA_Test)
    Pvalue_CUSUM_Test=Tran_time(data,Pvalue_CUSUM_Test)
    All_detection = [MK, Pettitt, BUT, SNHT, CUSUM_Test, EWMA_Test, Pvalue_CUSUM_Test]
    All_detection_name = ['Mann-Kendall', 'Pettitt', 'Buishand_U_Test ', 'Standard Normal Homogeinity Test', 'CUSUM', 'EWMA', 'P value-CUSUM']
#    retE = []
#    retC = []
#    for i in range(len(All_detection) - 1):
#        retA = ([All_detection_name[i] + "-" + All_detection_name[i + 1]])
#        retB = [a for a in All_detection[i] if a in All_detection[i + 1]]  # 两两方法之间的交集
#        retC.append(list(retA + retB))
        # print(retC)
#        if len(retC[i]) != 1:
            #         print("{}没有交集  \n".format(retC[i]))
            #     else:
            #         print("{}有交集:\n  {}\n".format(retC[i][0],retC[i][1:]))
#            retD = [b for b in range(len(data) - 4, len(data) + 1) if b in retC[i][1:]]  # 检测的暴发是否在数据的最近时间
#            retE.append(retA + retD)
#    Detection_value={};recent_data=[]
#    if len(retE)>1:
#        for i in range(len(retE)):
        #     print(retE[i])
#            if len(retE[i]) > 1:
           #     print("No!最近没有检测出暴发")
           # else:
#                F1=list(filter(lambda x: type(x)==int, retE[i]))
               # print(F1)
#                Detection_value[retE[i][0]]=F1
#                recent_data.append(retE[i][1])
#                print("Yes！最近有暴发，且暴发时间为第{}天".format(retE[i][1]))  # The list is empty
 #           PredictionDetection(data=data,n=retE[i][1],p=2,d=0,q=1,pvalue_cusum_k=1.5,a="ARIMA")
#    else:
#        print("Yes！最近有暴发，且暴发时间为第{}天".format(retE[0][1]))
#        Detection_value[retE[0][0]]=list(filter(lambda x: type(x)==int, retE[0]))
#        recent_data.append(retE[0][1])
#    import json
#    js=json.dumps(Detection_value)
#    file = open("./pad.txt",'a')
#    file.write(js)
#    file.write("\n")
#    file.write("最近有暴发，且暴发时间为第{}天".format(recent_data))
#    file.close()
    dic=dict(zip(All_detection_name,All_detection))
#    if not os.path.exists("./Outbreak_result/History_records/"):
#        os.mkdir("./Outbreak_result/History_records/")
    pd.Series(dic).to_csv("./Outbreaks_detected_by_seven_detection_methods.csv")
    print("\n")
    print("Outbreaks detection result file saved successfully\n") 
#    return Detection_value,recent_data
