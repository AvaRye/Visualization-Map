import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# 经纬度数据在每一行中的位置
latIndex = 11
lonIndex = 12
# PM2.5数据所在位置
PM2_5 = 0
PM10 = 1

# 城市的经纬度范围
latMin = 29.79
latMax = 30.03
lonMin = 121.41
lonMax = 121.72

# 存储每年1月的5、10、15、20、25、30日0时的数据用作绘制柱状图
PM2_5_max = []
PM2_5_all_year = []


def PM2_5_get_data(filePath):
    dataCsv = pd.read_csv(filePath, encoding='UTF-8')
    data = dataCsv.values
    data_PM2_5 = []
    for latlon in data:
        if latlon[latIndex] > latMin and latlon[latIndex] < latMax and latlon[lonIndex] > lonMin and latlon[lonIndex] < lonMax:
            data_PM2_5.append(latlon[PM2_5])

    # 取平均值以代表城市该时段的PM2.5值
    sum = 0
    for i in data_PM2_5:
        sum += i
    avg = round((sum / len(data_PM2_5)), 2)

    PM2_5_all_year.append(avg)


def PM2_5_append_max_data():
    # 分别用每五天的时间中的最大值来代表这五天的pm2.5数值
    PM2_5_max.append(max(PM2_5_all_year[0:4*24]))
    PM2_5_max.append(max(PM2_5_all_year[4*24:9*24]))
    PM2_5_max.append(max(PM2_5_all_year[9*24:14*24]))
    PM2_5_max.append(max(PM2_5_all_year[14*24:19*24]))
    PM2_5_max.append(max(PM2_5_all_year[19*24:24*24]))
    PM2_5_max.append(max(PM2_5_all_year[24*24:30*24]))


def add_to_list(year):
    PM2_5_all_year.clear()
    dirName = os.path.join("G:\\vscodepy\\air\\", year)
    fileList = os.listdir(dirName)
    for file in fileList:
        filePath = os.path.join(dirName, file)
        PM2_5_get_data(filePath)
    PM2_5_append_max_data()


years = ['2013', '2014', '2015', '2016', '2017', '2018']
for year in years:
    add_to_list(year)
# print(PM2_5_max)

index = np.arange(0, len(PM2_5_max))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.bar(index[:], PM2_5_max[:], width = 0.4, color="lightblue")
# plt.bar(np.arange(0,31), np.arange(5,36), width=0.5,color='lightblue')
plt.title('2013-2018年1月份宁波市PM2.5（每5日）最大值柱形图')  # 标题 根据经纬度更改标题中的城市名
plt.xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34],
           ['13年5日', '15日', '25日', '14年5日', '15日', '25日', '15年5日', '15日', '25日', '16年5日', '15日', '25日', '17年5日', '15日', '25日', '18年5日', '15日', '25日'])
plt.xlabel('日期(1月)')  # x轴名称
plt.ylabel('PM2.5(微克每立方米)')  # y轴名称
# plt.grid(True)  # 显示网格
plt.show()
