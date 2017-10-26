# encoding=utf-8
import unittest
import paramunittest
from common import common
from common import Log as Log
import readConfig as readConfig
from common import configHttp as ConfigHttp

login_xls = common.get_xls("BKlist.xlsx", "bklist")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()


@paramunittest.parametrized(*login_xls)
class BKlist(unittest.TestCase):
    def setParameters(self, case_name, method, token, header, data, result, code, msg):
        self.case_name = case_name
        self.method = str(method)
        self.token = int(token)
        self.header = str(header)
        self.data = str(data)
        self.result = int(result)
        self.code = int(code)
        self.msg = msg

        self.return_json = None
        self.info = None

    def setUp(self):
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(u"用例:%s测试开始前准备" % self.case_name)

    def testBKlist(self):
        # set url
        self.url = common.get_url_from_xml('bklist')
        configHttp.set_url(self.url)
        print(u"第一步:设置url:" + self.url)
        if self.token == 0:
            pass
        else:
            cookies = localReadConfig.get_headers('token')
            configHttp.set_cookies(str(cookies))
        # set headers
        configHttp.set_headers(self.header)
        print(u"第二步:设置header(token等)")
        # set params
        configHttp.set_data(self.data)
        print(u"第三步:设置发送请求的参数")
        # test interface
        self.return_json = configHttp.api_method(self.method)
        print(u"第四步：发送请求\n请求方法:" + self.method)
        # check result
        self.checkResult()
        print(u"第五步:检查结果")

    def tearDown(self):
        self.log.build_case_line(self.case_name, self.return_json.text)
        print(u"测试结束，输出log完结\n")

    def checkResult(self):
        # self.info = self.return_json.json()
        common.show_return_msg(self.return_json)

        # if self.result == 0:
        #     info = self.info['data']
        #     username = info['UserName']
        #     self.assertEqual(self.info['error'], self.code)
        #     self.assertEqual(username, 'admin')
        # if self.result == 1:
        #     self.assertEqual(self.info['error'], self.code)
        #     self.assertEqual(self.info['data'], self.msg)
