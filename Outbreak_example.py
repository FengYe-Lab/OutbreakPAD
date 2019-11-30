import OutbreakPAD
data=OutbreakPAD.read_data("/home/zoushengmei/OutbreakPAD.1.0/data/example.csv")
OutbreakPAD.PAD(data,p=2,d=0,q=1,a="ARIMA",pvalue_cusum_k=1.5) 
