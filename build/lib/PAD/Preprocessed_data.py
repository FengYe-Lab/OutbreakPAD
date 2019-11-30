import matplotlib.pylab  as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import calendar
from datetime import datetime
import seaborn as sn
def Preprocessed_data(file):
    with PdfPages('Preprocessed_data.pdf') as pdf:
        plt.figure()
        data = pd.read_csv(file)
        data['time'] = pd.date_range("1/1/2014", periods=len(data["count"]), freq="D")
        data['time'] = data['time'].astype('datetime64[ns]')
        data["weekday"] = pd.to_datetime(data['time']).dt.weekday
        data['month'] = pd.to_datetime(data['time']).dt.month
        # data['season'] = pd.to_datetime(data['time']).dt.season
        data['weekday'] = data.time.apply(
            lambda dateString: calendar.day_name[datetime.strptime(str(dateString), '%Y-%m-%d %H:%M:%S').weekday()])
        data["month_name"] = data.time.apply(
            lambda dateString: calendar.month_name[datetime.strptime(str(dateString), '%Y-%m-%d %H:%M:%S').month])
        data['month'] = pd.to_datetime(data['time']).dt.month
        data['year'] = pd.to_datetime(data['time']).dt.year

        # Get seasons
        spring = range(3, 5)
        summer = range(6, 8)
        fall = range(9, 11)
        # winter = everything else

        month = data['month'].values
        season = []

        for _ in range(len(month)):  # _变量是无用变量
            if month[_] == 3 or month[_] == 4 or month[_] == 5:
                season.append(2)  # spring
            elif month[_] == 6 or month[_] == 7 or month[_] == 8:
                season.append(3)  # summer
            elif month[_] == 9 or month[_] == 10 or month[_] == 11:
                season.append(4)  # fall
            else:
                season.append(1)  # winter
        data["season"] = season
        data["season"] = data.season.map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})

        fig, axes = plt.subplots(nrows=2, ncols=2)
        sn.boxplot(data=data, y='count', x='year', orient='v', ax=axes[0][0])
        sn.boxplot(data=data, y='count', x='season', orient='v', ax=axes[0][1])
        sn.boxplot(data=data, y='count', x='month', orient='v', ax=axes[1][0])
        sn.boxplot(data=data, y='count', x='weekday', orient='v', ax=axes[1][1])
        #     # plt.show()
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

        axes[0][0].set(xlabel='year', ylabel='Number of count', title='Number of count')
        axes[0][1].set(xlabel='season', ylabel='Number of count', title='Number in different seasons')
        axes[1][0].set(xlabel='month', ylabel='Number of count', title='Number at different months in a year')
        axes[1][1].set(xlabel='weekday', ylabel='Number of count', title='Number on weekdays')
        monthAggregated = pd.DataFrame(data.groupby("month")["count"].mean()).reset_index()
        # print(monthAggregated)
        monthSorted = monthAggregated.sort_values(by="count", ascending=False)
        # print(monthSorted)
        plt.rc('text', usetex=True)
        plt.figure()
        fig, axes = plt.subplots()
        #     fig.set_size_inches(12, 20)
        # sortOrder = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
        #                  "11", "12"]
        sortOrder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        sn.barplot(data=monthSorted, x="month", y="count", order=sortOrder)
        axes.set(xlabel="month", ylabel="Average number of count",
                 title=" Number of count in different months")
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()
        weekAggregated = pd.DataFrame(data.groupby("weekday")["count"].mean()).reset_index()
        # print(weekAggregated)
        weekSorted = weekAggregated.sort_values(by="count", ascending=False)
        # print(weekSorted)
        plt.rc('text', usetex=True)
        plt.figure(figsize=(8, 6))
        fig, axes = plt.subplots()
        #     fig.set_size_inches(12, 20)
        # sortOrder = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
        #                  "11", "12"]
        sortOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        sn.barplot(data=weekSorted, x="weekday", y="count", order=sortOrder)
        axes.set(xlabel="weekday", ylabel="Average number of count",
                 title="Number of count in different weeks")
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()
        # 一年内不同月的Number of SKPS
        plt.rc('text', usetex=True)
        plt.figure()
        monthAggregated = pd.DataFrame(data.groupby(["month_name", "year"])["count"].mean()).reset_index()
        # print(monthAggregated)
        fig1, ax1 = plt.subplots()
        fig1.set_size_inches(19, 8)
        hueOrder = [2014, 2015, 2016, 2017, 2018]
        sn.pointplot(x=monthAggregated["month_name"], y=monthAggregated["count"], hue=monthAggregated["year"],
                     hue_order=hueOrder,
                     data=monthAggregated)
        ax1.set(xlabel="Time", ylabel="Number", title="Number of count at different months of the year")

        pdf.savefig(figsize=(8, 6))
        plt.close()
        # 一年内不同周的Number of SKPS
        weekAggregated = pd.DataFrame(data.groupby(["weekday", "year"])["count"].mean()).reset_index()
        #     print(weekAggregated)
        fig1, ax1 = plt.subplots()
        fig1.set_size_inches(19, 8)
        hueOrder = [2014, 2015, 2016, 2017, 2018]
        # hueOrder = ["Friday","Monday","Saturday","Sunday","Thursday","Wednesday","Tuesday"]
        sn.pointplot(x=weekAggregated["weekday"], y=weekAggregated["count"], hue=weekAggregated["year"],
                     hue_order=hueOrder,
                     data=weekAggregated)
        ax1.set(xlabel="Time", ylabel="Number", title="Number of count at different weeks of the year")
        #     plt.savefig("result2.png")
        #     plt.show()

        pdf.savefig()
        plt.close()