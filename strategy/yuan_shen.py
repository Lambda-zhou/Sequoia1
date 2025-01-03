import logging
import pandas as pd

# 股票监测策略函数
def check(code_name, data, end_date=None, threshold=60):
    # 确保数据行数足够
    if len(data) < threshold + 1:
        logging.debug("{0}: 数据样本小于{1}天...\n".format(code_name, threshold + 1))
        return False

    if end_date is not None:
        mask = (data['日期'] <= end_date)
        data = data.loc[mask]
    data = data.tail(n=threshold)

    # 获取当前交易日数据
    current_day = data.iloc[-1]
    prev_day = data.iloc[-2]
    day_before_two = data.iloc[-3]
    day_before_three = data.iloc[-4]

    # 条件1：当前收盘价相对于3个交易日前和4个交易日前的收盘价比值大于等于1.1，并且当前收盘价等于当前最高价
    ratio_3_days = current_day['收盘'] / day_before_three['收盘']
    ratio_4_days = current_day['收盘'] / day_before_two['收盘']
    if ratio_3_days < 1.1 or ratio_4_days < 1.1 or current_day['收盘'] != current_day['最高']:
        return False

    # 条件2：当前成交量大于前一日成交量，并且当前收盘价小于当前开盘价
    if current_day['成交量'] <= prev_day['成交量'] or current_day['收盘'] >= current_day['开盘']:
        return False

    # 条件3：当前收盘价小于前一日收盘价
    if current_day['收盘'] >= prev_day['收盘']:
        return False

    # 条件4：当前成交量小于前一日、前两日和前三日的成交量
    if (current_day['成交量'] >= prev_day['成交量'] or
        current_day['成交量'] >= day_before_two['成交量'] or
        current_day['成交量'] >= day_before_three['成交量']):
        return False

    # 若所有条件均满足，返回 True
    return True
