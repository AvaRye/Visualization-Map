# README

可视化大作业

## 一、数据来源

- 一部分用到的城市经纬度范围（数据来源：百度地图拾取坐标系统）：

```
北京（latMin = 39.78
latMax = 40.01
lonMin = 116.22
lonMax = 116.52）

廊坊（latMin = 39.46
latMax = 39.60
lonMin = 116.62
lonMax = 116.80）

天津（latMin = 39.04
latMax = 39.28
lonMin = 117.04
lonMax = 117.33）

唐山（latMin = 39.59
latMax = 39.81
lonMin = 118.08
lonMax = 118.31）

宁波（latMin = 29.79
latMax = 30.03
lonMin = 121.41
lonMax = 121.72）

兰州（latMin = 36.03
latMax = 36.15
lonMin = 103.65
lonMax = 103.99）
```

- 部分数据使用城市经纬度范围来自[http://horizon2020.wqdian.cn](https://link.zhihu.com/?target=http%3A//horizon2020.wqdian.cn)，该网站的省市范围数据来自于天地图行政数据接口API和高德地图的逆地理编码。

```py
province_range = [
{"name": "广东", "lon": Interval(109.664816, 117.303484), "lat": Interval(20.223273, 25.519951)},
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
```

## 二、代码说明

### 散点图、柱形图绘制

figure.py用于绘制散点图，bar.py用于绘制柱形图

- figure.py：

从每一个csv文件（2013-2018年1月每小时）中读取所有数据，通过下标获取到符合条件（条件为经纬度在给定范围内，即可看作该行数据为给定城市空气数据）的每一行的第一列数据，即PM2.5的值，存入列表PM2_5_BJ_201X中，此处201X代表年份，以此列表为y轴数据，绘制 每一年1月北京市区PM2.5指数小时变化图。

- bar.py：

读取PM2.5数据后，再从中筛选出每五日的最大值（例如*max(PM2_5_all_year[0:4×24])*表示选取前5天数据中的最大值，因为从0开始，且每天有24小时，故此处为4×24），选最大值的目的是挑选极值数据以避免单一数据过小。将每一年共36个最大值作为y轴数据，绘制 某一城市6年间1月份的PM2.5数据变化柱形图。

### 逐月数据处理

- data_process.py 

用于原始数据的处理，将原始数据按经纬度划分为省，一省之内多点数据求平均值。将每日均数据存储为一个csv文件，存储进以月为单位的文件夹里。

- data_process2.py 

读取每个月的省对应的文件夹，算出月平均数据，存进同级文件夹。（..._average.csv）

- map_2d.py 

读取多个月均值文件整理成一个总的数据列表，使用[pyecharts](https://pyecharts.org/#/)库提供的api绘制一个界面，包括一个通过颜色直观显示每月数值情况的中国地图、一个折线图展示一年中的月平均数据变化、一个玫瑰饼图和一个横向柱形图通过不同形式展示不同省市的数据排序情况。另外有时间线控制可以自动播放或暂停切换月份数据，左上角可通过调整数据上下限筛选展示数据。

这三个文件的产出是 `PM2.5_of_13vs16.html` 这个文件，对比了13年和16年的逐月总体数据。

### 逐日数据处理

- get_multi_data.py 

用于处理原始数据，根据经纬度找到某个省的数据，选取某几个月多数据求平均值。

- map_2d_day.py 

读取综合数据文件，绘制了 1月和 6月的综合数据，分别绘制中国地图图组展示逐日数据传播情况，并选取pm2.5、pm10、SO2三个有代表性的数据柱形图和气温数据折线图绘制在同一张表中，可缩放拖动，可以直观看到数据之间的关系。

这两个文件的产出是`Multi_of_2016_1vs6.html` ，对比了2016年1月和6月的逐日数据；`RH_of_2016_1vs6.html`，对比天津市2016年1月和6月空气质量于空气湿度的关系；`Temp_of_2016_1vs6.html`，对比天津市2016年1月和6月空气质量于空气温度的关系；`PSFC_of_2016_1vs6.html`，对比天津市2016年1月和6月空气质量于气压的关系。

## 三、分析

### 散点图与柱形图

从散点图可以看出，北京1月份PM2.5值每年都仅在某些天数呈现极高的数值，即重度污染天气通常占小部分，且根据y轴的变化（注意每幅散点图的y轴比例尺不同），可以看出北京的空气质量逐年变好，从柱形图能够更直观地看到这一点，可见北京地城市污染治理效果佳。

从柱形图看其他城市，廊坊和唐山虽然部分时间处于空气高度污染状态，但总体情况来看，PM2.5逐年下降，这直接影响了北京地PM2.5值，它们都是北京的邻接城市，可见，大气污染的传输模式通常是几个邻近城市之间相互循环传播。

天津市的PM2.5值逐年变化不明显，很大程度上是因为天津濒临海洋，在治理北京及周边城市大气污染物的同时，天津成了污染扩散的腹地，大量污染物涌入天津，故天津的大气污染仍比较严重。

*注意y轴比例尺不同*

兰州大气污染程度较轻，且逐年改善。

宁波一直处于空气良好的状态。

### PM2.5_of_13vs16

可以看到最直观的就是16年整体情况都比13年好了很多，13年最高数据是1月的山东164，16年是12月的天津124，其次可以看到污染的传播模式大趋势是从华北为中心开始扩散的，但是在4、5月份新疆、内蒙等地的污染有所上升，可能是从内陆传来的。

其次每年冬天12月和1月都是空气污染最严重的时候，华北地区普遍烧煤供暖而且气候干燥，拉高了全国平均值。西藏和青海的空气一直都很好，和其地理位置优越有关也和省内没有太多重工业有关。

### 逐日数据分析

可以从天津示例中看到在1月份气温越高空气污染越高，在气温低时空气污染都下降明显。可以推测在冬天华北地区空气污染普遍上升，但当气温下降明显时空气污染也会减轻许多。同时空气污染和空气湿度呈明显正相关。

夏天的6月份空气污染就和气温关系不明显了，空气湿度对污染的影响有一些延后。



---

数据处理中间的数据放到`generated_data.zip`里了

