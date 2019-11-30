from .pyspc import *
import matplotlib.pylab  as plt
# plt.style.use('ggplot')
def CUSUM(ts):
    chart1 = spc(ts)+cusum()+rules()
    return chart1
