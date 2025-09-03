import os
from collections import Counter
import sys
from datetime import datetime
from typing import List
from pyecharts import options as opts

from pyecharts.charts import Calendar, Bar, Line, Pie

from datetime import datetime

from db_bootstrap import init_local_db

os.makedirs('./data/摄影统计/', exist_ok=True)


def get_weekday(timestamp):
    # 将时间戳转换为日期时间对象
    dt_object = datetime.fromtimestamp(timestamp)

    # 获取星期几，0代表星期一，1代表星期二，以此类推
    weekday = dt_object.weekday()
    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    return weekdays[weekday]



def sender(time_range):
    focal_seq_data = []
    focal_seq_10_data = []
    aperture_seq_data = []
    try:
        msg_data = msg_db.get_messages(wxid, time_range)
    except Exception as e:
        print(f"fail Exception: {e}")

    print(f"find photo size: {len(msg_data)}, time_range: {time_range}")


    # for name, count in owls_champion.items():
    #     print(f"熬夜天数 {name}: {count}")

    # 发言次数 字典 (key=remark, value=count)
    # reverse=True 降序排序，即集合大的在前。
    top_chat_count = sorted(chat_count.items(), key=lambda item: item[1], reverse=True)
    print(f"排序发言次数: {top_chat_count[:10]}")
    chat_count = dict(top_chat_count[:10])

    # 发言天数 字典 (key=remark, value=set | bitmap)
    top_chat_day_count = sorted(chat_day_count.items(), key=lambda item: len(item[1]), reverse=True)
    # print(f"排序发言天数: {top_chat_day_count[:10]}")
    chat_day_count = dict(top_chat_day_count[:10])

    # key=id, value=count
    top_owls_champion = sorted(owls_champion.items(), key=lambda item: item[1], reverse=False)
    owls_champion = dict(top_owls_champion[:10])

    if not data:
        return {
            'chart_data_focal-seq-10': None,
            'chart_data_aperture': None,
        }
    p1 = (
        Pie()
        .add(
            "",
            data,
            center=["40%", "50%"],
        )
        .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            toolbox_opts=opts.ToolboxOpts(),
            title_opts=opts.TitleOpts(title="消息类型占比"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", pos_top="20%", orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        # .render("./data/聊天统计/types_pie.html")
    )
    p2 = (
        Pie()
        .add(
            "",
            [[my_name, send_num], [ta_name, receive_num]],
            center=["40%", "50%"],
        )
        .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            toolbox_opts=opts.ToolboxOpts(),
            title_opts=opts.TitleOpts(title="双方消息占比"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", pos_top="20%", orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}\n{d}%"))
        # .render("./data/聊天统计/pie_scroll_legend.html")
    )
    p3 = (
        Pie()  # 创建一个 `Pie` 对象，表示饼图。
        .add(
            "",
            [[key, value] for key, value in weekday_count.items()],  # 数据项为 weekday_count 字典的键值对，转换成 [(key, value)] 的格式。
            radius=["40%", "75%"],  # 饼图的半径，设置为一个环形图。内圈半径为 40%，外圈半径为 75%。
        )
        .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),  # 配置数据缩放功能（通常用于其他类型的图表，饼图默认无法使用）。
            toolbox_opts=opts.ToolboxOpts(),  # 工具箱选项，提供工具（如保存图片、数据视图等）。
            title_opts=opts.TitleOpts(title="星期分布图"),  # 设置图表标题为“星期分布图”。
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),  # 配置图例，设置为垂直布局，位置在图表左上角。
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(formatter="{b}: {c}\n{d}%")  # 配置饼图的标签格式：显示名称({b})、值({c}) 和百分比({d})。
        )
        # .render("./data/聊天统计/pie_weekdays.html")  # （注释掉的代码）将图表渲染为 HTML 文件，保存到指定路径。
    )
    chat_bar = (
        Bar()
        .add_xaxis(list(chat_count.keys()))  # 从字典的键中获取 x 轴数据（姓名）
        .add_yaxis("发言次数", list(chat_count.values()))  # 从字典的值中获取 y 轴数据
        .reversal_axis()  # 转换坐标轴，使其变为水平条形图
        .set_global_opts(
            title_opts=opts.TitleOpts(title="活跃度统计"),
            xaxis_opts=opts.AxisOpts(name="发言次数", type_="value"),
            yaxis_opts=opts.AxisOpts(name="群员"),
        )
    )
    chat_day_bar = (
        Bar()
        .add_xaxis(list(chat_day_count.keys()))  # 从字典的键中获取 x 轴数据（姓名）
        .add_yaxis("发言天数", [len(dates) for dates in chat_day_count.values()])  # 从字典的值中获取 y 轴数据（得分）
        .reversal_axis()  # 转换坐标轴，使其变为水平条形图
        .set_global_opts(
            title_opts=opts.TitleOpts(title="活跃天数统计"),
            xaxis_opts=opts.AxisOpts(name="天数", type_="value"),
            yaxis_opts=opts.AxisOpts(name="群员"),
        )
    )
    night_owls_bar = (
        Bar()
        .add_xaxis(list(owls_champion.keys()))  # 从字典的键中获取 x 轴数据（姓名）
        .add_yaxis("熬夜冠军", list(owls_champion.values()))  # 从字典的值中获取 y 轴数据（得分）
        .reversal_axis()  # 转换坐标轴，使其变为水平条形图
        .set_global_opts(
            title_opts=opts.TitleOpts(title="熬夜冠军统计"),
            xaxis_opts=opts.AxisOpts(name="次数", type_="value"),
            yaxis_opts=opts.AxisOpts(name="群员"),
        )
    )
    # 将图表的配置项（options）导出为带引号的JSON字符串
    return {
        # 焦段范围使用频率 柱状图
        'chart_data_focal_seq_10': p2.dump_options_with_quotes(),
        # 光圈使用频率 饼图
        'chart_data_aperture': p1.dump_options_with_quotes(),
    }


def get_format_date(timestamp, format_str='%Y-%m-%d') -> str:
    # 将时间戳转换为 datetime 对象
    dt_object = datetime.fromtimestamp(timestamp)
    # 格式化为字符串
    # formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return dt_object.strftime(format_str)



if __name__ == '__main__':
    from web_ui.web import get_contact

    init_local_db()

    # data = month_count(wxid, time_range=None)
    # data['chart'].render("./data/聊天统计/month_count.html")
    # data = calendar_chart(wxid, time_range=None)
    # data['chart'].render("./data/聊天统计/calendar_chart.html")
    # time_range = ['2024-01-01 00:00:00','2024-12-31 00:00:00']
    time_range = None
    # data = sender(wxid, time_range=time_range, my_name=Me().name, ta_name=contact.remark)
    # print(data)
