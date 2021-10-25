# -*- coding:utf-8 -*-
import json
import time
from datetime import datetime

import requests

from jd_logger import logger


class Timer(object):
    def __init__(self, sleep_interval=0.5):
        # 这里修改为获取当天时间
        buy_time = datetime.now().replace(hour=9, minute=59, second=59, microsecond=500000)
        self.buy_time = datetime.strptime(str(buy_time), "%Y-%m-%d %H:%M:%S.%f")

        # 原作者代码，获取配置文件，配置文件需要每天改
        # self.buy_time = datetime.strptime(global_config.getRaw('config', 'buy_time'), "%Y-%m-%d %H:%M:%S.%f")

        # 开始抢购时间戳 1609811999500
        self.buy_time_ms = int(time.mktime(self.buy_time.timetuple()) * 1000.0 + self.buy_time.microsecond / 1000)
        self.sleep_interval = sleep_interval

        self.diff_time = self.local_jd_time_diff()

    @staticmethod
    def jd_time():
        """从京东服务器获取时间毫秒
        """
        url = 'https://a.jd.com//ajax/queryServerData.html'
        ret = requests.get(url).text
        js = json.loads(ret)
        return int(js["serverTime"])

    @staticmethod
    def local_time():
        """获取本地时间毫秒
        """
        return int(round(time.time() * 1000))

    def local_jd_time_diff(self):
        """计算本地与京东服务器时间差
        """
        return self.local_time() - self.jd_time()

    def local_time_greater_than_buy_time(self, minutes=30):
        """计算当前时间与抢购时间的差值，返回布尔值
        +1801500 代表时间戳往后加上半小时
        +600500  代表时间戳往后加上十分钟
        +120500  代表时间戳往后加上两分钟
        估计几分钟没有抢到基本就没戏了，允许抢购时间是半小时
        默认设置为 30 分钟，当天超过抢购时间30分钟后手动运行脚本时，
        为了防止无意义的刷接口，直接就停掉程序
        """
        if minutes == 2:
            minutes = 120500
        elif minutes == 30:
            minutes = 1801500
        else:
            minutes = 600500
        if self.local_time() >= (self.buy_time_ms + minutes):
            return True
        else:
            return False

    def start(self):
        logger.info('正在等待到达设定时间:{}，检测本地时间与京东服务器时间误差为【{}】毫秒'.format(self.buy_time, self.diff_time))
        while True:
            # 本地时间减去与京东的时间差，能够将时间误差提升到0.1秒附近
            # 具体精度依赖获取京东服务器时间的网络时间损耗
            if self.local_time() - self.diff_time >= self.buy_time_ms:
                logger.info('时间到达，开始执行……')
                break
            else:
                time.sleep(self.sleep_interval)
