import  numpy as np
import pandas as pd
def Pettitt_change_point_detection(inputdata):
    inputdata1 = np.array(inputdata)
    n         = inputdata1.shape[0]
    k = range(n)
    inputdataT = pd.Series(inputdata1)
    r = inputdataT.rank()
    Uk = [2*np.sum(r[0:x])-x*(n + 1) for x in k]
    Uka = list(np.abs(Uk))
    U = np.max(Uka)
    K = Uka.index(U)
    pvalue         = 2 * np.exp((-6 * (U**2))/(n**3 + n**2))
    if pvalue <= 0.05:
        change_point_desc = '显著'
    else:
        change_point_desc = '不显著'
    #Pettitt_result = {'突变点位置':K,'突变程度':change_point_desc
    return K
