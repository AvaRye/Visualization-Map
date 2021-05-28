import pandas as pd
import numpy as np
from interval import Interval
import os

'''
原始一个月中的每天数据文件
 -> 根据经纬度划分为省
 -> 汇总成省对应的日平均数据一个文件
 -> 存储进月为单位的文件夹
'''

# calculate the province that the location belongs
province_range = [{"name": "广东", "lon": Interval(109.664816, 117.303484), "lat": Interval(20.223273, 25.519951)},
                  {"name": "江苏", "lon": Interval(116.355183, 121.927472), "lat": Interval(30.76028, 35.127197)},
                  {"name": "山东", "lon": Interval(114.810126, 122.705605), "lat": Interval(34.377357, 38.399928)},
                  {"name": "浙江", "lon": Interval(118.022574, 122.834203), "lat": Interval(26.643625, 31.182556)},
                  {"name": "河南", "lon": Interval(110.35571, 116.644831), "lat": Interval(31.3844, 36.366508)},
                  {"name": "河北", "lon": Interval(113.454863, 119.84879), "lat": Interval(36.048718, 42.615453)},
                  {"name": "辽宁", "lon": Interval(118.839668, 125.785614), "lat": Interval(38.72154, 43.488548)},
                  {"name": "四川", "lon": Interval(97.347493, 108.54257), "lat": Interval(26.048207, 34.315239)},
                  {"name": "湖北", "lon": Interval(108.362545, 116.132865), "lat": Interval(29.032769, 33.272876)},
                  {"name": "湖南", "lon": Interval(108.786106, 114.256514), "lat": Interval(24.643089, 30.1287)},
                  {"name": "福建", "lon": Interval(115.84634, 120.722095), "lat": Interval(23.500683, 28.317231)},
                  {"name": "上海", "lon": Interval(120.852326, 122.118227), "lat": Interval(30.691701, 31.874634)},
                  {"name": "北京", "lon": Interval(115.416827, 117.508251), "lat": Interval(39.442078, 41.058964)},
                  {"name": "安徽", "lon": Interval(114.878463, 119.645188), "lat": Interval(29.395191, 34.65234)},
                  {"name": "内蒙古", "lon": Interval(97.17172, 126.065581), "lat": Interval(37.406647, 53.333779)},
                  {"name": "陕西", "lon": Interval(105.488313, 111.241907), "lat": Interval(31.706862, 39.582532)},
                  {"name": "黑龙江", "lon": Interval(121.183134, 135.088511), "lat": Interval(43.422993, 53.560901)},
                  {"name": "广西", "lon": Interval(104.446538, 112.05675), "lat": Interval(20.902306, 26.388528)},
                  {"name": "天津", "lon": Interval(116.702073, 118.059209), "lat": Interval(38.554824, 40.251765)},
                  {"name": "江西", "lon": Interval(89.551219, 124.57284), "lat": Interval(8.972204, 40.256391)},
                  {"name": "吉林", "lon": Interval(121.638964, 131.309886), "lat": Interval(40.864207, 46.302152)},
                  {"name": "重庆", "lon": Interval(105.289838, 110.195637), "lat": Interval(28.164706, 32.204171)},
                  {"name": "山西", "lon": Interval(110.230241, 114.56294), "lat": Interval(34.583784, 40.744953)},
                  {"name": "云南", "lon": Interval(97.527278, 106.196958), "lat": Interval(21.142312, 29.225286)},
                  {"name": "新疆", "lon": Interval(73.501142, 96.384783), "lat": Interval(34.336146, 49.183097)},
                  {"name": "贵州", "lon": Interval(103.599417, 109.556069), "lat": Interval(24.620914, 29.224344)},
                  {"name": "甘肃", "lon": Interval(92.337827, 108.709007), "lat": Interval(32.596328, 42.794532)},
                  {"name": "海南", "lon": Interval(108.614575, 117.842823), "lat": Interval(8.30204, 20.16146)},
                  {"name": "宁夏", "lon": Interval(104.284332, 107.661713), "lat": Interval(35.238497, 39.387783)},
                  {"name": "青海", "lon": Interval(89.401764, 103.068897), "lat": Interval(31.600668, 39.212599)},
                  {"name": "香港", "lon": Interval(113.815684, 114.499703), "lat": Interval(22.134935, 22.566546)},
                  {"name": "澳门", "lon": Interval(113.528164, 113.598861), "lat": Interval(22.109142, 22.217034)},
                  {"name": "台湾", "lon": Interval(119.314417, 123.701571), "lat": Interval(21.896939, 25.938831)},
                  {"name": "西藏", "lon": Interval(78.386053, 99.115351), "lat": Interval(26.853453, 36.484529)}]

dict_province = {"广东": [], "江苏": [], "山东": [], "浙江": [], "河南": [], "河北": [], "辽宁": [], "四川": [], "湖北": [], "湖南": [],
                 "福建": [], "上海": [], "北京": [], "安徽": [], "内蒙古": [], "陕西": [], "黑龙江": [], "广西": [], "天津": [], "江西": [],
                 "吉林": [], "重庆": [], "山西": [], "云南": [], "新疆": [], "贵州": [], "甘肃": [], "海南": [], "宁夏": [], "青海": [],
                 "西藏": [], "香港": [], "澳门": [], "台湾": []}

title = ["PM2.5(微克每立方米)", "PM10(微克每立方米)", "SO2(微克每立方米)", "NO2(微克每立方米)",
         "CO(毫克每立方米)", "O3(微克每立方米)", "U(m/s)", "V(m/s)",
         "TEMP(K)", "RH(%)", "PSFC(Pa)", "lat", "lon"]
TITLE = title[0]


def read_data(year, month, day_of_month):
    # 创建存储文件夹
    year = str(year)
    month = str(month).rjust(2, '0')
    os.makedirs(year + month, exist_ok=True)

    for day in range(1, day_of_month + 1):
        print(day)
        file = "/Users/ava/0/Visualization/vis/data/" + year + month + "/CN-Reanalysis-daily-" \
               + year + month + str(day).rjust(2, '0') + "00.csv"
        # read data
        data = pd.read_csv(file, sep=",")
        # get part of data
        data2 = data[[TITLE, " lat", " lon"]]  # 坑啊带个空格orz

        # 整理数据
        for i in data2.index:
            s = data2.iloc[i]
            for province in province_range:
                if s[" lat"] in province["lat"] and s[" lon"] in province["lon"]:
                    dict_province[province["name"]].append(s[TITLE])

        # 求均值
        for key in dict_province.keys():
            if dict_province[key]:
                dict_province[key] = np.mean(dict_province[key])
            else:
                dict_province[key] = 0

        file_name = "/Users/ava/PycharmProjects/vis/" + year + month + "/" + file[-14:]
        # to csv
        header = [["name", "value"]]
        list_pro = [[k, v] for k, v in dict_province.items()]
        pd.DataFrame(data=list_pro, columns=header).to_csv(file_name, mode="w")
        # reset dict
        for key in dict_province.keys():
            dict_province[key] = []
        print(file_name + " done")
    return


# 数据选项
y = 2016
day_of_month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# 循环读取处理
for mon in range(1, 2):
    read_data(y, mon, day_of_month_list[mon - 1])
