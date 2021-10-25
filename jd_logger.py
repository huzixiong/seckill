import logging
import logging.handlers
import os

'''
日志模块
'''
# LOG_FILENAME = 'jd_seckill.log'
LOG_FILENAME = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log', 'jd_seckill.log')
logger = logging.getLogger()


def set_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(process)d-%(threadName)s - '
                                  '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.handlers.TimedRotatingFileHandler(
        LOG_FILENAME, when="D", interval=1, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


set_logger()
