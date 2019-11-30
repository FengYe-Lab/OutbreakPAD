import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.api as sm
import seaborn as sn
from sklearn.metrics import mean_squared_error
import matplotlib.pylab as plt
import seaborn as sns
def test_stationarity(timeseries,size,cutoff = 0.01):
    # 决定起伏统计 rolling(window=2).mean()
    rolmean = timeseries.rolling(window=size).mean()    # 对size个数据进行移动平均
    rol_weighted_mean = pd.DataFrame.ewm(timeseries,span=size).mean()    # 对size个数据进行加权移动平均
    rolstd = timeseries.rolling(window=size).mean()      # 偏离原始值多少
    # 画出起伏统计
    orig = plt.plot(timeseries, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    weighted_mean = plt.plot(rol_weighted_mean, color='green', label='weighted Mean')
    std = plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    # 进行df测试
    print ('Result of Dickry-Fuller test')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical value(%s)' % key] = value
    print(dfoutput)
    if dftest[1] <= cutoff:
        print("\nStrong evidence against the null hypothesis, reject the null hypothesis. Data has no unit root, hence it is stationary")
    else:
        print("\nWeak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")





def difference(ts,size):
    diff = ts.diff(size)
    diff.dropna(inplace=True)
    return diff
def testStationarity(ts):
    dftest = adfuller(ts)
    # 对上述函数求得的值进行语义描述
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    return dfoutput
# 分解decomposing

def decomposition(ts):
    decomposition = seasonal_decompose(ts,model="additive")
    trend = decomposition.trend  # 趋势
    seasonal = decomposition.seasonal  # 季节性
    residual = decomposition.resid  # 剩余的
    ts_decompose = residual
    ts_decompose.dropna(inplace=True)
#     test_stationarity(ts_decompose,size=2)
    plt.style.use('ggplot')
    plt.subplot(411)
    plt.plot(ts,label='Original',color="blue")
    plt.legend(loc=4)
    plt.subplot(412)
    plt.plot(trend,label='Trend',color="blue")
    plt.legend(loc=4)
    plt.subplot(413)
    plt.plot(seasonal,label='Seasonarity',color="blue")
    plt.legend(loc=4)
    plt.subplot(414)
    plt.plot(residual,label='Residual',color="blue")
    plt.legend(loc=4)
    plt.tight_layout()
    plt.savefig("./decomposition.png")
    plt.show()
def rol_mean_diff(ts,window):
    rol_mean = ts.rolling(window=window).mean()
    rol_mean.dropna(inplace=True)

    ts_diff_1 = rol_mean.diff(1)
    ts_diff_1.dropna(inplace=True)
    plt.plot(rol_mean,color="blue")
    plt.title("rolling mean")
    # plt.savefig("./rolling_mean.png")
    plt.show()
    plt.plot(ts_diff_1,color="blue")
    plt.title("the first difference")
    # plt.savefig("./difference.png")
    plt.show()
    print(testStationarity(ts_diff_1))
    return rol_mean,ts_diff_1
def define_params(ts_diff):
    lag_acf = acf(ts_diff, nlags=20)
    lag_pacf = pacf(ts_diff, nlags=20, method='ols')
    # q的获取:ACF图中曲线第一次穿过上置信区间.这里q取2
    plt.subplot(121)
    plt.stem(lag_acf)
    plt.axhline(y=0, linestyle='--', color='gray')
    plt.axhline(y=-1.96 / np.sqrt(len(ts_diff)), linestyle='--', color='gray')  # lowwer置信区间
    plt.axhline(y=1.96 / np.sqrt(len(ts_diff)), linestyle='--', color='gray')  # upper置信区间
    plt.title('Autocorrelation Function')
    # p的获取:PACF图中曲线第一次穿过上置信区间.这里p取2
    plt.subplot(122)
    plt.stem(lag_pacf)
    plt.axhline(y=0, linestyle='--', color='gray')
    plt.axhline(y=-1.96 / np.sqrt(len(ts_diff)), linestyle='--', color='gray')
    plt.axhline(y=1.96 / np.sqrt(len(ts_diff)), linestyle='--', color='gray')
    plt.title('Partial Autocorrelation Function')
    plt.tight_layout()
    plt.show()
def find_params(ts_rolMean_diff):
    import itertools

    p_min = 0
    q_min = 0
    p_max = 7
    q_max = 7

    # Initialize a DataFrame to store the results
    results_bic = pd.DataFrame(index=['AR{}'.format(i) for i in range(p_min,p_max+1)],
                               columns=['MA{}'.format(i) for i in range(q_min,q_max+1)])

    for p,q in itertools.product(range(p_min,p_max+1),
    #                                range(d_min,d_max+1),
                                   range(q_min,q_max+1)):
        if p==0  and q==0:
            results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = np.nan
            continue

        try:
            model = sm.tsa.ARMA(ts_rolMean_diff, order=(p, q),
                                   #enforce_stationarity=False,
                                   #enforce_invertibility=False,
                                  )
            results = model.fit()
            results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = results.bic
        except:
            continue
    results_bic = results_bic[results_bic.columns].astype(float)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax = sns.heatmap(results_bic,
                     mask=results_bic.isnull(),
                     ax=ax,
                     annot=True,
                     fmt='.2f',
                     );
    ax.set_title('BIC')
    plt.show()

def result_model(ts_rolMean_diff,p,q):
    from statsmodels.tsa.arima_model import ARMA
    model = ARMA(ts_rolMean_diff, order=(p,q))
    result_arma = model.fit(disp=-1, method='css')
    return result_arma


def recover(result_arma, rol_mean, ts):
    predict_ts = result_arma.predict()
    # 一阶差分还原
    # diff_shift_ts = ts_diff_1.shift(1)
    # diff_recover_1 = predict_ts.add(diff_shift_ts)
    # 再次一阶差分还原
    rol_shift_ts = rol_mean.shift(1)
    diff_recover = predict_ts.add(rol_shift_ts)
    # 移动平均还原
    rol_sum = ts.rolling(window=6).sum()
    rol_recover = diff_recover * 7 - rol_sum.shift(1)
    #     # 对数还原
    #     log_recover = np.exp(rol_recover)
    rol_recover.dropna(inplace=True)
    return rol_recover


def plot_data(ts, rol_recover):
    ts_actual = ts[rol_recover.index]  # 过滤没有预测的记录
    plt.figure(facecolor='white')
    ts_actual.plot(color='blue', label='Original')
    rol_recover.plot(color='red', label='Predict')

    plt.legend(loc='best')
    plt.title('RMSE: %.4f' % np.sqrt(sum((rol_recover - ts_actual) ** 2) / ts_actual.size))
    plt.show()



def p_q_Parameter(data):
    results = sm.tsa.arma_order_select_ic(data, ic=['aic', 'bic'], trend='nc', max_ar=8, max_ma=8)
    p=results.bic_min_order[0];q=results.bic_min_order[1]
    return p,q









