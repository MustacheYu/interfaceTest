# encoding=utf-8
import os
import readConfig as readConfig
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
import json

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir


def show_return_msg(response):
    url = response.url
    msg = response.text
    print(u"\n请求地址：" + url)
    # 可以显示中文
    print(u"\n请求返回值：" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))


# ****************************** read interfaceURL xml ********************************
def get_url_from_xml(name):
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)

    url = '/' + '/'.join(url_list)
    return url


# ****************************** read testCase excel ********************************
def get_xls(xls_name, sheet_name):
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file
    data = open_workbook(xlsPath)
    # get sheet by name
    sheet = data.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls
