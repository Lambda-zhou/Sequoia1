# -*- encoding: UTF-8 -*-
import utils
import logging
import work_flow
import settings
import schedule
import time
import datetime
from pathlib import Path
import re
from collections import Counter
from collections import defaultdict


def log():
	# 创建一个日志记录器
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)

	# 如果有已有的处理器，先移除它们
	if logger.hasHandlers():
		logger.handlers.clear()

	# Add a StreamHandler to output to the console
	formatter = logging.Formatter('%(asctime)s %(message)s')

	log_file_handler = logging.FileHandler('console_output.log', mode='a')
	log_file_handler.setLevel(logging.INFO)
	log_file_handler.setFormatter(formatter)
	logging.getLogger().addHandler(log_file_handler)


def printstock(stock_number):
	# 读取文件内容
	with open('console_output.log', 'r', encoding='utf-8') as file:
		content = file.read()

	# 使用正则表达式提取股票信息
	pattern = re.compile(r"\('(\d+)', '([^']+)', ([\d.]+|nan)\)")
	matches = pattern.findall(content)

	# 统计每只股票出现的次数
	stock_counter = Counter(matches)

	# 获取出现次数最多的10只股票
	most_common_stocks = stock_counter.most_common(stock_number)
	
	# 格式化输出
	for stock in most_common_stocks:
		print(stock[0])
	
	
def printpool(stock_number):
	# 读取日志文件
	with open('console_output.log', 'r', encoding='utf-8') as file:
		data = file.read()

	# 正则表达式匹配股票信息
	pattern = re.compile(r'\(\s*\'(\d+)\',\s*\'([^\']+)\'\s*,\s*([\d\.]+|nan)\s*\)')
	matches = pattern.findall(data)

	# 统计股票出现的次数及其所在的股票池
	stock_count = defaultdict(lambda: {'count': 0, 'pools': set(), 'price': None})

	# 记录每个股票池的名称
	pool_names = re.findall(r'\"(.*?)\"', data)

	# 解析每个股票池中的股票
	for pool_name in pool_names:
		pool_data = re.search(rf'\"{pool_name}\".*?\[(.*?)\]', data, re.DOTALL)
		if pool_data:
			stocks = pattern.findall(pool_data.group(1))
			for stock in stocks:
				stock_id, stock_name, stock_price = stock
				stock_count[stock_id]['count'] += 1
				stock_count[stock_id]['pools'].add(pool_name)
				stock_count[stock_id]['price'] = stock_price

	# 找出出现次数最多的股票
	top_stocks = sorted(stock_count.items(), key=lambda x: x[1]['count'], reverse=True)[:stock_number]

	# 输出结果
	for stock_id, info in top_stocks:
		stock_name = next((name for id, name, _ in matches if id == stock_id), '未知')
		stock_price = info['price']
		pools = ', '.join(info['pools'])
		print(f"名: {stock_name}, 价格: {stock_price}, 次数: {int(info['count']/2)}, 池: {pools}")

log()
settings.init()
work_flow.prepare()
# printstock(n)
# printpool(n)
