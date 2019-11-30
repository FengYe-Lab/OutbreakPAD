
from .pyspc import *
import matplotlib.pylab  as plt
def EWMA(ts):
#    print("EWMA:")
    chart2 = spc(ts) + ewma()+ rules()
#    print(chart2)
    return chart2
