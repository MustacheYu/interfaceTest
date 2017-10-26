# encoding=utf-8
import os
import unittest
import readConfig as readConfig
from common import HTMLTestRunner
from common.Log import MyLog as Log
from common import businessCommon
from common.configEmail import Email

log = Log.get_log()
logger = log.get_logger()
localReadConfig = readConfig.ReadConfig()


# noinspection PyGlobalUndefined
class AllTest:
    def __init__(self):
        global resultPath, on_off
        resultPath = log.get_report_path()
        on_off = localReadConfig.get_email("on_off")
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
        self.caseFile = os.path.join(readConfig.proDir, "testCase")
        self.caseList = []
        self.email = Email()

    def set_case_list(self):
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        fb.close()

    def set_case_suite(self):
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caseList:
            case_name = case.split("/")[-1]
            discover = unittest.defaultTestLoader.discover(self.caseFile,
                                                           pattern=case_name + '.py',
                                                           top_level_dir=None)
            suite_module.append(discover)

        if len(suite_module) > 0:

            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None

        return test_suite

    def run(self):
        fp = None
        try:
            suit = self.set_case_suite()
            if suit is not None:
                logger.info(u"********测试开始********")
                fp = open(resultPath, 'wb')
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                                       title=u'自动化测试报告',
                                                       description=u'用例执行情况:')
                runner.run(suit)
            else:
                logger.info(u"没有用例可以运行")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info(u"*********测试结束*********")
            fp.close()
            if on_off == 'on':
                self.email.send_email()
            elif on_off == 'off':
                logger.info(u"测试报告不通过电子邮件发送给开发人员")
            else:
                logger.info(u"未知错误")


if __name__ == '__main__':
    businessCommon.login()
    obj = AllTest()
    obj.run()
