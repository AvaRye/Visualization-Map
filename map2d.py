from typing import List
import pandas as pd
import numpy as np
import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie, Line, Page

'''
读取月平均数据 （或日数据）
 -> 整理成一个总的数据列表
 -> 展示到 html 界面上
'''

# total set
YEAR = 2013
MONTH_RANGE = range(1, 13)
TITLE = "PM2.5"


# 整理总的数据列表
def get_data_by_month(year):
    data_all = []

    for mon in MONTH_RANGE:
        y_m = "/" + str(year) + str(mon).rjust(2, '0')
        file = "/Users/ava/PycharmProjects/vis" + y_m + y_m + "_average.csv"
        # read data
        mon_data = pd.read_csv(file, sep=",")
        data2 = mon_data[["name", "value"]]

        data_list = []

        for i in data2.index:
            s = data2.iloc[i]
            if s["value"]:  # 去掉没有统计数据的省份
                data_list.append(
                    {
                        "name": s["name"],
                        "value": [round(s["value"], 4), s["name"]]
                    }
                )
        # 按照value做升序排序
        data_list.sort(key=lambda x: x["value"][0], reverse=True)
        data_all.append(
            {
                "time": str(mon) + "月",
                "data": data_list
            }
        )
    return data_all


month_time_list = [str(d) + "月" for d in MONTH_RANGE]
max_list = []
min_list = []


# 计算全国平均值
def get_total_num(data_all):
    total_avg = []
    for mon in MONTH_RANGE:
        li = []
        for dicts in data_all[mon - 1]["data"]:
            li.append(dicts["value"][0])
        # 顺便记一下最大最小值
        max_list.append(max(li))
        min_list.append(min(li))
        # 添加均值，保留 4 位
        total_avg.append(round(np.mean(li), 4))
    return total_avg


# 计算全部数据最大值并扩大范围
def get_max_num():
    return max(max_list) + 2


# 计算全部数据最小值
def get_min_num():
    return min(min_list)


def get_chart(time: str, year):
    # prepare all the data
    data_all = get_data_by_month(year)
    total_num = get_total_num(data_all)
    max_num = get_max_num()
    min_num = get_min_num()

    # start painting
    map_data = [
        [[x["name"], x["value"]] for x in d["data"]] for d in data_all if d["time"] == time
    ][0]
    min_data, max_data = (min_num, max_num)
    data_mark: List = []
    i = 0
    for x in month_time_list:
        if x == time:
            data_mark.append(total_num[i])
        else:
            data_mark.append("")
        i = i + 1

    map_chart = (
        Map()
            .add(
            series_name="",
            data_pair=map_data,
            zoom=1,
            center=[119.5, 34.5],
            is_map_symbol_show=False,
            itemstyle_opts={
                "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
                "emphasis": {
                    "label": {"show": Timeline},
                    "areaColor": "rgba(255,255,255, 0.5)",
                },
            },
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="" + str(time) + "全国分地区" + TITLE + "情况（单位：微克每立方米）",
                subtitle="",
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(255,255,255, 0.9)"
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=JsCode(
                    """function(params) {
                    if ('value' in params.data) {
                        return params.data.value[2] + ': ' + params.data.value[0];
                    }
                }"""
                ),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="30",
                pos_top="center",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    line_chart = (
        Line()
            .add_xaxis(month_time_list)
            .add_yaxis("", total_num)
            .add_yaxis(
            "",
            data_mark,
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title=str(year) + "年全国" + TITLE + "情况", pos_left="72%", pos_top="5%"
            )
        )
    )
    bar_x_data = [x[0] for x in map_data]
    bar_y_data = [{"name": x[0], "value": x[1][0]} for x in map_data]
    bar = (
        Bar()
            .add_xaxis(xaxis_data=bar_x_data)
            .add_yaxis(
            series_name="",
            y_axis=bar_y_data,
            label_opts=opts.LabelOpts(
                is_show=True, position="right", formatter="{b} : {c}"
            ),
        )
            .reversal_axis()
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                max_=max_num, axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="top",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    pie_data = [[x[0], x[1][0]] for x in map_data]
    pie = (
        Pie()
            .add(
            series_name="",
            data_pair=pie_data,
            radius=["15%", "35%"],
            center=["80%", "82%"],
            rosetype="radius",
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    grid_chart = (
        Grid()
            .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10", pos_right="45%", pos_top="50%", pos_bottom="5"
            ),
        )
            .add(
            line_chart,
            grid_opts=opts.GridOpts(
                pos_left="65%", pos_right="80", pos_top="10%", pos_bottom="50%"
            ),
        )
            .add(pie, grid_opts=opts.GridOpts(pos_left="45%", pos_top="60%"))
            .add(map_chart, grid_opts=opts.GridOpts())
    )

    return grid_chart


def get_time_line(year):
    timeline = Timeline(
        init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.PURPLE_PASSION)
    )
    for y in month_time_list:
        g = get_chart(time=y, year=year)
        timeline.add(g, time_point=str(y))

    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="60",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )
    return timeline


if __name__ == "__main__":
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        get_time_line(2013),
        get_time_line(2016)
    )
    page.render(TITLE + "_of_13vs16.html")
