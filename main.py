# -*- encoding: UTF-8 -*-

import utils
import logging
import work_flow
import settings
import schedule
import time
import datetime
from pathlib import Path


def job():
    if utils.is_weekday():
        work_flow.prepare()

# 创建一个日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 如果有已有的处理器，先移除它们
if logger.hasHandlers():
    logger.handlers.clear()

# Add a StreamHandler to output to the console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

log_file_handler = logging.FileHandler('console_output.log', mode='a')
log_file_handler.setLevel(logging.INFO)
log_file_handler.setFormatter(formatter)
logging.getLogger().addHandler(log_file_handler)

if settings.config['cron']:
    EXEC_TIME = "15:15"
    schedule.every().day.at(EXEC_TIME).do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    work_flow.prepare()
