import os
import platform

from jd_logger import logger
from timer import Timer


def seckill_stop():
    """判断时间，当超过抢购时间后，自动停止程序"""
    timer = Timer()
    system = platform.system()
    if timer.local_time_greater_than_buy_time(2):  # 设置超出抢购时间时长
        if system == "Windows":
            # os.system("taskkill /F /IM python.exe")  # 旧版
            os.system("taskkill /F /IM py.exe")  # 3.7.3
        else:
            # Mac | Linux
            os.system("ps -ef | grep python | grep -v grep | cut -c 6-11 | xargs kill -15")


logger.info("seckill exec stop!")
seckill_stop()
