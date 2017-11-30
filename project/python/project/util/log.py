import logging
import sys
import time
import os

class Log():

    def getLogger(self):
        pathFile = sys.path[0] + "\\log\\"
        log_file = pathFile + 'test-' + str(time.strftime("%Y%m%d")) + '.log'
        if not os.path.exists(pathFile):
            os.makedirs(pathFile)
        # 获取logger实例，如果参数为空则返回root logger
        logger = logging.getLogger("test")

        # 指定logger输出格式
        formatter = logging.Formatter('%(asctime)s - %(filename)s -%(levelname)s: %(message)s')

        # 文件日志
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter  # 也可以直接给formatter赋值

        # 为logger添加的日志处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # 指定日志的最低输出级别，默认为WARN级别
        logger.setLevel(logging.INFO)
        return logger
