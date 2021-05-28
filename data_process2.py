import pandas as pd
import numpy as np
from interval import Interval

'''
读取每个月的省对应的文件夹
 -> 算出月平均数据
 -> 存进同级文件夹
'''

# year_month = "/201601"
# day_of_month = 31
day_of_month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def process(year_month, day_of_month):
    values = []
    means = []

    for day in range(1, day_of_month + 1):
        file = "/Users/ava/PycharmProjects/vis" + year_month + year_month + str(day).rjust(2, '0') + "00.csv"
        # read data
        data = pd.read_csv(file, sep=",")
        values.append(list(data["value"]))
    # print(values)

    zip_value = list(map(list, zip(*values)))
    # print(zip_value)
    for line in zip_value:
        means.append(np.mean(line))
    print(means)
    file_name = "/Users/ava/PycharmProjects/vis" + year_month + year_month + "_average.csv"
    # to csv
    header = [["name", "value"]]
    list_pro = []
    for i in data["name"].index:
        list_pro.append([data["name"][i], means[i]])
    pd.DataFrame(data=list_pro, columns=header).to_csv(file_name, mode="w")


# 数据选项
y = "/2013"
for mon in range(4, 13):
    y_m = y + str(mon).rjust(2, '0')
    process(y_m, day_of_month_list[mon - 1])
