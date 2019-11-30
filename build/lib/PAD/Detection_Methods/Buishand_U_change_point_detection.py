import numpy as np

def Buishand_U_change_point_detection(inputdata):
    inputdata1 = np.array(inputdata)
    inputdata_mean = np.mean(inputdata1)
    n  = inputdata.shape[0]
    k = range(n)
    Sk = [np.sum(inputdata1[0:x+1] - inputdata_mean) for x in k]
    sigma = np.sqrt(np.sum((inputdata1-np.mean(inputdata1))**2)/(n-1))
    U = np.sum((Sk[0:(n - 2)]/sigma)**2)/(n * (n + 1))
    Ska = np.abs(Sk)
    S = np.max(Ska)
    K = list(Ska).index(S) + 1
    Skk = (Sk/sigma)
#    b=[]
#    for i in K:
#        tmp=inputdata.index[i]
#        b.append(tmp.strftime("%Y-%m-%d"))
    #print(b)
    # plt.plot()
    return K
