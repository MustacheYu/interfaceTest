# encoding=utf-8
import common
import configHttp
import readConfig as readConfig

localLogin_xls = common.get_xls("userCase.xlsx", "login")
localConfigHttp = configHttp.ConfigHttp()
localReadConfig = readConfig.ReadConfig()


# login
def login():
    # set url
    url = common.get_url_from_xml('login')
    localConfigHttp.set_url(url)
    # set header
    header = localLogin_xls[0][3]
    localConfigHttp.set_headers(str(header))
    # set param
    data = localLogin_xls[0][4]
    localConfigHttp.set_data(str(data))
    # login
    method = localLogin_xls[0][1]
    response = localConfigHttp.api_method(str(method))
    info = response.json()
    if info['error'] == 0:
        cookies = {c.name: c.value for c in response.cookies}
        localReadConfig.set_headers("TOKEN", str(cookies))
    else:
        localReadConfig.set_headers("TOKEN", 'null')
