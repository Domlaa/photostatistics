import os
from datetime import datetime

from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, HeatMap, Calendar, Line
from pyecharts.commons.utils import JsCode

from process.mysql_data_processor import MysqlDataProcessor

processor = MysqlDataProcessor()


def get_weekday(timestamp):
    # 将时间戳转换为日期时间对象
    dt_object = datetime.fromtimestamp(timestamp)

    # 获取星期几，0代表星期一，1代表星期二，以此类推
    weekday = dt_object.weekday()
    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    return weekdays[weekday]


def sender(time_range):
    focal_seq_10_map = processor.focal_seq_10(time_range)
    shot_calendar_data = processor.shot_calendar(time_range)
    lens_use_data = processor.lens_use_rate(time_range)
    iso_use_data = processor.iso_use_rate(time_range)
    shutter_use_data = processor.shutter_use_rate(time_range)
    aperture_use_data = processor.aperture_use_rate(time_range)
    hour_data = processor.shot_hour(time_range)
    monthly_shot_times = processor.monthly_shot_times(time_range)
    focal_top10_data = processor.focal_top10(time_range)

    total_shot = processor.total_shot(time_range)

    total_shot = processor.total_shot(time_range)
    days_with_photos = len(shot_calendar_data)
    most_active_month = max(monthly_shot_times, key=monthly_shot_times.get)
    photos_in_most_active_month = max(monthly_shot_times.values())
    favorite_time = max(hour_data, key=hour_data.get)
    # 找到 value 最大的那一项
    most_productive = max(shot_calendar_data, key=lambda x: x[1])
    most_productive_date = most_productive[0]
    photos_on_most_productive_day = most_productive[1]

    fav_focal_range_t = max(focal_top10_data.items(), key=lambda x: x[1])
    fav_focal_range = fav_focal_range_t[0]

    statistics_data = {
        'days_with_photos': days_with_photos,
        'total_photos': total_shot,
        'most_active_month': most_active_month,
        'photos_in_most_active_month': photos_in_most_active_month,
        'favorite_time': favorite_time,
        'most_productive_date': most_productive_date,
        'photos_on_most_productive_day': photos_on_most_productive_day,
        'fav_focal_range': fav_focal_range,
    }
    # statistics_data = {

    #     'most_used_focal_length': most_used_focal_length,
    #     'fav_lens': fav_lens,
    #     'photos_with_fav_lens': photos_with_fav_lens,
    #     'fav_iso': fav_iso,
    #     'fav_shutter': fav_shutter,
    #     'fav_aperture': fav_aperture,
    # }

    focal_seq_10_data_bar = (
        Bar()
        .add_xaxis(list(focal_seq_10_map.keys()))  # 从字典的键中获取 x 轴数据（姓名）
        .add_yaxis("焦段范围统计", list(focal_seq_10_map.values()))  # 从字典的值中获取 y 轴数据
        .reversal_axis()  # 转换坐标轴，使其变为水平条形图
        .set_global_opts(
            title_opts=opts.TitleOpts(title="焦段范围使用统计"),
            xaxis_opts=opts.AxisOpts(name="使用次数", type_="value"),
            yaxis_opts=opts.AxisOpts(name="焦段范围"),
        )
    )

    focal_top_10_data_bar = (
        Bar()
        .add_xaxis(list(focal_top10_data.keys()))  # 从字典的键中获取 x 轴数据（姓名）
        .add_yaxis("最常用的焦段", list(focal_top10_data.values()))  # 从字典的值中获取 y 轴数据
        .reversal_axis()  # 转换坐标轴，使其变为水平条形图
        .set_global_opts(
            title_opts=opts.TitleOpts(title="最常用的焦段统计"),
            xaxis_opts=opts.AxisOpts(name="使用次数", type_="value"),
            yaxis_opts=opts.AxisOpts(name="焦段"),
        )
    )

    # print(f"shot_calendar_data: {shot_calendar_data}")
    # 添加数据到图表
    shot_calendar = Calendar().add(
        series_name="拍摄数量",
        yaxis_data=shot_calendar_data,  # 指定数据 二维数组
        calendar_opts=opts.CalendarOpts(
            range_="2024",  # 日历图显示的年份范围
            yearlabel_opts=opts.CalendarYearLabelOpts(is_show=False),  # 不显示年份标签
        ),
    ).set_global_opts(  # 设置全局选项，包括标题和可视化映射
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            formatter="{c}张",  # b是日期，c是值
            # formatter= JsCode("""
            # function (params) {
            #     return params.value[0] + " 拍摄 " + params.value[1] + " 张";
            # }
            # """)
        ),
        title_opts=opts.TitleOpts(title="年度拍照统计"),  # 设置标题的位置和内容
        visualmap_opts=opts.VisualMapOpts(
            max_=100,  # 可视化映射的最大值
            orient="horizontal",  # 横向
            pos_bottom="40px",  # 距离底部
            pos_left="center",  # 居中,
            range_color=["#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476", "#31a354"],  # 浅绿 → 深绿
        ),
    )

    lens_pie = (
        Pie()
        .add(
            "镜头使用比例",
            lens_use_data,  # 数据源为列表，子项为（name, value）的形式
            center=["30%", "50%"],  # 圆心位置，距离画布左边 40%，上边 50%
        )
        .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            toolbox_opts=opts.ToolboxOpts(),
            title_opts=opts.TitleOpts(title="镜头使用占比"),
            tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"),  # b=名称 c=数值 d=百分比
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="60%", pos_top="20%", orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}"))  # 标签显示名称+百分比
    )

    # TODO 图例过度导致混乱
    iso_view = (
        Pie()
        .add(
            "ISO使用比例",
            iso_use_data,
            radius=["40%", "60%"],  # 内半径40%，外半径70%，形成圆环
            center=["30%", "50%"],  # 圆心位置，距离画布左边 40%，上边 50%
        )
        .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            toolbox_opts=opts.ToolboxOpts(),
            title_opts=opts.TitleOpts(title="ISO使用占比"),
            tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"),  # b=名称 c=数值 d=百分比
            legend_opts=opts.LegendOpts(type_="scroll",
                                        pos_left="60%",
                                        pos_top="20%",
                                        orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}"))  # 标签显示名称+百分比
    )

    # TODO 图例过度导致混乱
    shutter_view = (
        Pie()
        .add(
            "快门使用比例",
            shutter_use_data,
            radius=["40%", "60%"],  # 内半径40%，外半径70%，形成圆环
            center=["30%", "50%"],  # 圆心位置，距离画布左边 40%，上边 50%
        )
        .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            toolbox_opts=opts.ToolboxOpts(),
            title_opts=opts.TitleOpts(title="快门使用占比"),
            tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"),  # b=名称 c=数值 d=百分比
            legend_opts=opts.LegendOpts(type_="scroll",

                                        pos_left="60%",
                                        pos_top="20%",
                                        orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}"))  # 标签显示名称+百分比
    )

    # TODO 图例过度导致混乱
    aperture_view = (
        Pie()
        .add(
            "光圈使用比例",
            aperture_use_data,
            radius=["60%", "80%"],  # 内半径40%，外半径70%，形成圆环
            center=["30%", "50%"],  # 圆心位置，距离画布左边 40%，上边 50%
        )
        .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            toolbox_opts=opts.ToolboxOpts(),
            title_opts=opts.TitleOpts(title="光圈使用占比"),
            tooltip_opts=opts.TooltipOpts(formatter="{b}: {c} ({d}%)"),  # b=名称 c=数值 d=百分比
            legend_opts=opts.LegendOpts(type_="scroll",
                                        pos_left="60%",
                                        pos_top="10%",
                                        orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}"))  # 标签显示名称+百分比
    )

    hour_view = (
        Bar()
        .add_xaxis(list(hour_data.keys()))
        .add_yaxis('次数', list(hour_data.values()))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="拍照时间分布"),
            xaxis_opts=opts.AxisOpts(
                name="小时",
                axislabel_opts=opts.LabelOpts(interval=0)),
            yaxis_opts=opts.AxisOpts(name="次数"),
        )
    )

    monthly_shot_times_line = (
        Line()
        .add_xaxis(list(monthly_shot_times.keys()))
        .add_yaxis('拍照次数', list(monthly_shot_times.values()))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="每月拍照次数统计"),
            xaxis_opts=opts.AxisOpts(
                name="日期",
                axislabel_opts=opts.LabelOpts(interval=0)),
            yaxis_opts=opts.AxisOpts(name="次数"),
        )
    )

    # 将图表的配置项（options）导出为带引号的JSON字符串
    return {
        # 焦段范围使用频率 柱状图
        'chart_data_focal_seq_10': focal_seq_10_data_bar.dump_options_with_quotes(),
        # 拍照日期热图
        'chart_data_shot_calendar': shot_calendar.dump_options_with_quotes(),
        'chart_data_lens': lens_pie.dump_options_with_quotes(),
        'chart_data_iso': iso_view.dump_options_with_quotes(),
        'chart_data_shutter': shutter_view.dump_options_with_quotes(),
        'chart_data_aperture': aperture_view.dump_options_with_quotes(),
        'chart_data_hour': hour_view.dump_options_with_quotes(),
        'chart_data_m_shot_times': monthly_shot_times_line.dump_options_with_quotes(),
        'chart_data_focal_top10': focal_top_10_data_bar.dump_options_with_quotes(),
        'statistics_data': statistics_data
    }


def get_format_date(timestamp, format_str='%Y-%m-%d') -> str:
    # 将时间戳转换为 datetime 对象
    dt_object = datetime.fromtimestamp(timestamp)
    # 格式化为字符串
    # formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return dt_object.strftime(format_str)


if __name__ == '__main__':
    time_range = None
    data = sender(time_range=time_range)
