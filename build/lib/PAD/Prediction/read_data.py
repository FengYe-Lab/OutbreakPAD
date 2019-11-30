import pandas as pd
def read_data(file,start_date="1/1/2014"):
    ts=pd.read_csv(file)
    ts_number=ts.iloc[:,1]
    ts_number=ts_number.values
    ts_time=pd.date_range(start_date,periods=len(ts_number),freq="D")
    ts=pd.Series(ts_number,index=ts_time)
    return ts
