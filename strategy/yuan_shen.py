# -*- encoding: UTF-8 -*-
import logging
import pandas as pd

# 新的股票分析策略
def check(code_name, data):
    # 确保数据有足够的行数
    if len(data) < 5:
        logging.debug("{0}:样本小于5天...\n".format(code_name))
        return False

    # 获取最近几天的数据
    current = data.iloc[-1]
    three_days_ago = data.iloc[-4]
    four_days_ago = data.iloc[-5]
    previous_day = data.iloc[-2]

    # 当前收盘价与3个交易日前和4个交易日前收盘价的比值
    ratio = current['收盘'] / three_days_ago['收盘']
    
    # 检查条件
    if ratio >= 1.1 and current['收盘'] == current['最高']:
        if current['成交量'] > previous_day['成交量'] and current['收盘'] < current['开盘']:
            if current['收盘'] < previous_day['收盘']:
                if current['成交量'] <= data.iloc[-3:-1]['成交量'].max():
                    return True

    return False

# 示例使用
# 假设我们有一个DataFrame 'df' 包含股票数据
# df = pd.read_csv('your_stock_data.csv')  # 读取数据
# result = new_check('股票代码', df)
# print(result)