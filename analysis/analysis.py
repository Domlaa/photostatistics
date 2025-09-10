import os
from datetime import datetime

from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, HeatMap, Calendar
from pyecharts.commons.utils import JsCode

from process.mysql_data_processor import MysqlDataProcessor

# from db_bootstrap import init_local_db

processor = MysqlDataProcessor()

os.makedirs('./data/摄影统计/', exist_ok=True)


def get_weekday(timestamp):
    # 将时间戳转换为日期时间对象
    dt_object = datetime.fromtimestamp(timestamp)

    # 获取星期几，0代表星期一，1代表星期二，以此类推
    weekday = dt_object.weekday()
    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    return weekdays[weekday]


def total_shot():
    return processor.total_shot()


def sender(time_range):
    focal_seq_10_map = processor.focal_seq_10()
    shot_calendar_data = processor.shot_calendar(time_range)

    focal_seq_data = []
    aperture_seq_data = []

    # focal_seq_10_map = {}
    # for row in focal_seq_10_data:
    #     f_start = int(row['focal_start'])
    #     key = f"{f_start}-{f_start+9} mm"
    #     focal_seq_10_map[key] = row['usage_count']
    # print(f"焦段范围使用统计: {len(focal_seq_10_data)}, time_range: {time_range}")

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
            pos_left="center"  # 居中
        ),
    )

    # 将图表的配置项（options）导出为带引号的JSON字符串
    return {
        # 焦段范围使用频率 柱状图
        'chart_data_focal_seq_10': focal_seq_10_data_bar.dump_options_with_quotes(),
        # 拍照日期热图
        'chart_data_shot_calendar': shot_calendar.dump_options_with_quotes()
        # 光圈使用频率 饼图
        # 'chart_data_aperture': p1.dump_options_with_quotes(),
    }


def get_format_date(timestamp, format_str='%Y-%m-%d') -> str:
    # 将时间戳转换为 datetime 对象
    dt_object = datetime.fromtimestamp(timestamp)
    # 格式化为字符串
    # formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return dt_object.strftime(format_str)


if __name__ == '__main__':
    # init_local_db()

    # data = month_count(wxid, time_range=None)
    # data['chart'].render("./data/聊天统计/month_count.html")
    # data = calendar_chart(wxid, time_range=None)
    # data['chart'].render("./data/聊天统计/calendar_chart.html")
    # time_range = ['2024-01-01 00:00:00','2024-12-31 00:00:00']
    time_range = None
    data = sender(time_range=time_range)
    # print(data)
