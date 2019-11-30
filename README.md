# PAD
PAD(Prediction And Detection) is a Python 3 library. This library enables you to predict outbreaks of hospital-acquired infections.

# Download and install
##  in linux
  ```bash
  git clone https://github.com/zmmei/PAD.git  
  cd PAD    
  python setup install  
  ```  
# Function

# Simple Demo
  ```python
  import PAD  
  import pandas as pd  
  ts_number=[3,1]*30+[2,3]*79+[30,26]*6  
  ts_time=pd.date_range("1/1/2014",periods=230,freq="D")  
  ts=pd.Series(ts_number,index=ts_time)  
  PAD.PAD(ts,p=2,d=0,q=1,a="ARIMA",pvalue_cusum_k=1.5)  
  ```

