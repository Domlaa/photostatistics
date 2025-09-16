class DataAnalyzer:

    def get_conn(self):
        raise NotImplementedError

    # 总的拍摄张数
    def total_shot(self, time_range) -> int:
        raise NotImplementedError

    # 10mm一组，最喜欢用的焦段
    def focal_seq_10(self, time_range) -> {}:
        raise NotImplementedError

    # 使用频率前十的焦段
    def focal_top10(self, time_range) -> {}:
        raise NotImplementedError

    # 类似 github 的提交日期统计图
    def shot_calendar(self, time_range) -> {}:
        raise NotImplementedError

    # 镜头使用比例 饼图
    def lens_use_rate(self, time_range) -> {}:
        raise NotImplementedError

    # ISO 饼图
    def iso_use_rate(self, time_range) -> {}:
        raise NotImplementedError

    # shutter 饼图
    def shutter_use_rate(self, time_range) -> {}:
        raise NotImplementedError

    # aperture 饼图
    def aperture_use_rate(self, time_range) -> {}:
        raise NotImplementedError

    # 拍照时间段统计
    def shot_hour(self, time_range) -> {}:
        raise NotImplementedError

    # 每月拍照次数统计
    def monthly_shot_times(self, time_range) -> {}:
        raise NotImplementedError