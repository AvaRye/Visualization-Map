import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# 经纬度数据在每一行中的位置
latIndex = 11
lonIndex = 12
# PM2.5数据所在位置
PM2_5 = 0

# 北京五环内的经纬度范围
latBJMin = 39.78
latBJMax = 40.01
lonBJMin = 116.22
lonBJMax = 116.52

PM2_5_BJ_201X = []#用来存PM2.5的数据

def PM2_5_BJ(filePath):
    dataCsv = pd.read_csv(filePath, encoding='UTF-8')
    data = dataCsv.values
    # labels = list(dataCsv.columns.values)
    # ['PM2.5(微克每立方米)', ' PM10(微克每立方米)', ' SO2(微克每立方米)',
    #' NO2(微克每立方米)', ' CO(毫克每立方米)', ' O3(微克每立方米)', ' U(m/s)', ' V(m/s)',
    # ' TEMP(K)', ' RH(%)', ' PSFC(Pa)', ' lat', ' lon', ' ']
    # print(labels)

    # 截取大表中北京市区的数据存储在dataBeiJing中
    # latlon表示每行数据，即不同经纬度的数据
    dataBeiJing = []
    for latlon in data:
        if latlon[latIndex] > latBJMin and latlon[latIndex] < latBJMax and latlon[lonIndex] > lonBJMin and latlon[lonIndex] < lonBJMax:
            dataBeiJing.append(latlon[PM2_5])

    # 取平均值以代表北京该时段的PM2.5值
    sum = 0
    for i in dataBeiJing:
        sum += i
    avgBJ = round((sum / len(dataBeiJing)), 2)

    PM2_5_BJ_201X.append(avgBJ)


def draw_pm(year):
    PM2_5_BJ_201X.clear()
    dirName = os.path.join("G:\\vscodepy\\air\\", year)
    fileList = os.listdir(dirName)
    for file in fileList:
        filePath = os.path.join(dirName, file)
        PM2_5_BJ(filePath)

    index = np.arange(0, len(PM2_5_BJ_201X))
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.scatter(index[:], PM2_5_BJ_201X[:], 5, "lightblue")
    plt.title(year + '年1月北京市区PM2.5指数小时变化图')  # 标题
    plt.xticks([0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360, 384, 408, 432, 456, 480, 504, 528, 552, 576, 600, 624, 648, 672, 696, 720],
               [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31])
    plt.xlabel('日期(1月x日)')  # x轴名称
    plt.ylabel('PM2.5(微克每立方米)')  # y轴名称
    plt.grid(True)  # 显示网格
    plt.show()

years = ['2013', '2014', '2015', '2016', '2017', '2018']
for year in years:
  draw_pm(year)