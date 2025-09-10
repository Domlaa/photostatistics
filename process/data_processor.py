class DataProcessor:

    # 总的拍摄张数
    def total_shot(self) -> int:
        raise NotImplementedError

    # 10mm一组，最喜欢用的焦段
    def focal_seq_10(self) -> {}:
        raise NotImplementedError

    # 类似 github 的提交日期统计图
    def shot_calendar(self, time_range) -> {}:
        raise NotImplementedError
