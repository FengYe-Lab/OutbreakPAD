


import matplotlib.pylab as plt
plt.style.use('ggplot')

def GRNN_Model(X, Y):
    scaler = preprocessing.MinMaxScaler()
    arima_values = scaler.fit_transform(X)
    origin_values = scaler.fit_transform(Y.reshape((-1, 1)))

    x_train, x_test, y_train, y_test = train_test_split(arima_values, origin_values, train_size=0.7, random_state=0)

    list = []
    for x in np.linspace(0.01, 0.2, 40):
        SmoRMSE = {"smoothing_factor": "", "rmse": ""}
        nn = algorithms.GRNN(std=x, verbose=False)
        nn.train(x_train, y_train)
        y_pred = nn.predict(x_test)
        #     print(x)
        RMSE = np.sqrt(mean_squared_error(y_pred, y_test))
        SmoRMSE["smoothing_factor"] = x
        SmoRMSE["rmse"] = RMSE
        list.append(SmoRMSE)
        SmoRMSE = pd.DataFrame(list)
    plt.plot(SmoRMSE.iloc[:, 1], SmoRMSE.iloc[:, 0])
    plt.xlabel('smoothing factor')
    plt.ylabel('RMSE')
    plt.show()
    a = SmoRMSE.ix[SmoRMSE["rmse"].idxmin()]
    print(a)
    best_smoothing_factor = a[1:2].values
    nw = algorithms.GRNN(std=0.02, verbose=False)
    nw.train(x_train, y_train)
    # y_Predict = nw.predict(x_test)
    GRNN_Predict = nw.predict(arima_values)
    origin_values_inverse = scaler.inverse_transform(origin_values)
    GRNN_Predict_inverse = scaler.inverse_transform(GRNN_Predict)
    print("QRIGIN:GRNN RMSE= %.4f" % np.sqrt(
        sum((GRNN_Predict_inverse - origin_values_inverse) ** 2) / GRNN_Predict_inverse.size))
    #     print( "QRIGIN:ARIMA RMSE= %.4f"%np.sqrt(mean_squared_error(origin_values_inverse,Y)))
    plt.plot(origin_values_inverse, "b", label="ORIGIN")
    #     plt.plot(Y,"g",label="ARIMA")
    plt.plot(GRNN_Predict_inverse, "r", label="ARIMA-GRNN")
    plt.legend(loc="best")
    #     ORIGIN_ARIMA_RMSE=np.sqrt(mean_squared_error(origin_values_inverse,log_recover.values))
    # plt.text(0.5, 1, "QRIGIN:ARIMA RMSE= %.4f"%ORIGIN_ARIMA_RMSE)
    # plt.text(0.5, 1, "QRIGIN:ARIMA-GRNN RMSE= %.4f" % np.sqrt(sum((GRNN_Predict_inverse - origin_values_inverse) ** 2) / GRNN_Predict_inverse.size))

    plt.title("GRNN Models for Predict")
    plt.show()
    return GRNN_Predict_inverse