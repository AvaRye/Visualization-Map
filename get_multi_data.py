import pandas as pd
import numpy as np
from interval import Interval
import os

'''
原始一个月中的每天数据文件
 -> 根据经纬度找到某个省的数据
 -> 选取某几个月
 -> 处理多个数据求均值
'''

# calculate the province that the location belongs
title = ["PM2.5(微克每立方米)", "PM10(微克每立方米)", "SO2(微克每立方米)", "NO2(微克每立方米)",
         "CO(毫克每立方米)", "O3(微克每立方米)", "U(m/s)", "V(m/s)",
         "TEMP(K)", "RH(%)", "PSFC(Pa)", "lat", "lon"]


def read_data(year, month, day_of_month):
    # 创建存储文件夹
    year = str(year)
    month = str(month).rjust(2, '0')
    os.makedirs(year + month, exist_ok=True)

    dict_data = {}

    # 处理每天数据存进 list 里
    for day in range(1, day_of_month + 1):
        print(day)
        file = "/Users/ava/0/Visualization/vis/data/" + year + month + "/CN-Reanalysis-daily-" \
               + year + month + str(day).rjust(2, '0') + "00.csv"
        # read data
        data = pd.read_csv(file, sep=",")
        # get part of data
        # data2 = data[[TITLE, " lat", " lon"]]  # 坑啊带个空格orz

        # 整理数据
        for i in data.index:
            s = data.iloc[i]
            # for province in province_range:
            # 只挑一个天津吧
            province = {"name": "天津", "lon": Interval(116.702073, 118.059209), "lat": Interval(38.554824, 40.251765)}
            if s[" lat"] in province["lat"] and s[" lon"] in province["lon"]:
                dict_data[str(day)] = [s["PM2.5(微克每立方米)"], s[" PM10(微克每立方米)"], s[" SO2(微克每立方米)"], s[" NO2(微克每立方米)"],
                                       s[" CO(毫克每立方米)"], s[" O3(微克每立方米)"], s[" U(m/s)"], s[" V(m/s)"],
                                       s[" TEMP(K)"], s[" RH(%)"], s[" PSFC(Pa)"]]

    # print(list_dict)
    file_name = "/Users/ava/PycharmProjects/vis/" + year + month + "/" + "multi.csv"
    # to csv
    header = [["PM2.5(微克每立方米)", "PM10(微克每立方米)", "SO2(微克每立方米)", "NO2(微克每立方米)",
               "CO(毫克每立方米)", "O3(微克每立方米)", "U(m/s)", "V(m/s)",
               "TEMP(K)", "RH(%)", "PSFC(Pa)"]]
    list_pro = dict_data.values()
    pd.DataFrame(data=list_pro, columns=header).to_csv(file_name, mode="w")
    # reset dict
    dict_data = {}
    print(file_name + " done")

    return


# 数据选项
y = 2016
day_of_month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# 循环读取处理
for mon in range(4, 5):
    read_data(y, mon, day_of_month_list[mon - 1])
