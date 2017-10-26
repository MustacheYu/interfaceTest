# encoding=utf-8
import requests
import json
import readConfig as readConfig

localReadConfig = readConfig.ReadConfig()


# noinspection PyGlobalUndefined
class ConfigHttp:
    def __init__(self):
        global host, timeout
        host = localReadConfig.get_http("baseurl")
        timeout = localReadConfig.get_http("timeout")
        self.url = None
        self.cookies = None
        self.headers = {}
        self.params = {}
        self.data = {}
        self.files = {}

    def set_url(self, url):
        self.url = host + url

    def set_headers(self, header):
        self.headers = eval(header)

    def set_cookies(self, cookies):
        self.cookies = eval(cookies)

    def set_params(self, param):
        self.params = param

    def set_data(self, data):
        self.data = data

    def set_files(self, files):
        self.files = files

    def api_method(self, method):
        if method == "get":
            try:
                response = requests.get(self.url,
                                        headers=self.headers,
                                        params=self.params,
                                        cookies=self.cookies,
                                        timeout=float(timeout))
                return response
            except requests.ConnectTimeout:
                return None
        elif method == "post_json":
            try:
                response = requests.post(self.url,
                                         headers=self.headers,
                                         json=json.loads(self.data),
                                         cookies=self.cookies,
                                         files=self.files,
                                         timeout=float(timeout))
                return response
            except requests.ConnectTimeout:
                return None
        elif method == "post_dict":
            try:
                response = requests.post(self.url,
                                         headers=self.headers,
                                         data=json.loads(self.data),
                                         cookies=self.cookies,
                                         files=self.files,
                                         timeout=float(timeout))
                return response
            except requests.ConnectTimeout:
                return None
        else:
            print u'暂不支持其他'
