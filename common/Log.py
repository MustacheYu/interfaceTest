# encoding=utf-8
import os
import readConfig as readConfig
import logging
from datetime import datetime
import threading
import json


# noinspection PyGlobalUndefined
class Log:
    def __init__(self):
        global logPath, resultPath, proDir
        proDir = readConfig.proDir
        resultPath = os.path.join(proDir, "result")
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        # defined handler
        handler = logging.FileHandler(os.path.join(logPath, "output.log"))
        handler.setLevel(logging.INFO)
        # defined formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s  %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger

    def build_case_line(self, case_name, info):
        result_info = u"\n用例名称:%s\n返回内容:%s" % (case_name, json.dumps(json.loads(info), ensure_ascii=False))
        self.logger.info(result_info)

    @staticmethod
    def get_report_path():
        report_path = os.path.join(logPath, "report.html")
        return report_path

    @staticmethod
    def get_result_path():
        return logPath


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log
