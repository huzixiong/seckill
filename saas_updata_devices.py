# import os
from os import remove, system
from os.path import abspath, join, dirname, exists

import requests
from openpyxl import load_workbook


class LoginSaas2:
    def __init__(self):
        self.url_login = "https://saas2.ukelink.net/saas/index/ajax_login"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
        self.session = self._init_session()
        self.login_session = self._init_login_session()
        self.excel_path = abspath("./template.xlsx")

    def _init_session(self):
        session = requests.session()
        return session

    def _init_login_session(self):
        session = self.session
        from_data = {"userCode": "qianjunxia",
                     "password": "e10adc3949ba59abbe56e057f20f883e"
                     }
        headers = {'User-Agent': self.user_agent,
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept': 'application/json, text/plain, */*',
                   'Connection': 'keep-alive'}
        login_session = session.post(url=self.url_login, headers=headers, data=from_data)
        return session

    def download_template_excel(self, imei):
        url_download = "https://saas2.ukelink.net/htemp/resources/bss/import_cert_template_en.xlsx"
        headers = {'Host': 'saas2.ukelink.net',
                   'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   'Referer': 'https://saas2.ukelink.net/saas/bssManager/certImport?v=17835.835044942196&hidePanle=true'}
        session = self.login_session
        r = session.get(url=url_download, headers=headers, params={'v': '263'})
        # print(r.status_code)
        with open(r"./template.xlsx", "wb") as f:
            f.write(r.content)
        path_excel = join(dirname(abspath(__file__)), 'template.xlsx')
        if not exists(path_excel):
            raise ("没有找到excel文件")
        wb = load_workbook(path_excel)
        sheet = wb.worksheets[0]
        sheet["A3"] = imei
        wb.save(path_excel)

    def updata_security_LCE(self):
        "上次安全证书excel返回上传临时连接"
        url_excel_file = "https://saas2.ukelink.net/attachment/index/uploadDoc?fname=imgFile"
        url_updata_lce = "https://saas2.ukelink.net/attachment/importConfig/handleProcess"
        # url_temp_url = None
        headers_url = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            # 'Content-Type': 'multipart/form-data',
            'Accept - Language': 'zh - CN',
            'Accept': '*/*'}
        headers_temp = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept - Language': 'zh - CN',
            'Accept': '*/*'
        }
        files = {
            "imgFile": ("import_targetTypeIMEI_template_zh-CN.xlsx", open(
                r"./template.xlsx",
                "rb"), "application/excel"),
            "id": "WU_FILE_1",
            "name": "import_targetTypeIMEI_template_zh-CN.xlsx",
            "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "lastModifiedDate": "Wed Jun 23 2021 11:29:11 GMT+0800 (中国标准时间)"
        }
        session = self.login_session
        rsp = session.post(url=url_excel_file, headers=headers_url, files=files)
        url_temp_url = rsp.json()['data'].get('url')
        # print(url_temp_url)
        from_data_temp = {'url': '/bss/terminal/importImeiCaInfo',
                          'key': 'list',
                          'title[A]': 'imei',
                          'streamNo': 'web_saas1626229426112727279',
                          'partnerCode': 'UKSAS',
                          'loginCustomerId': '59409a6556a5956b828b8d5e',
                          'path': url_temp_url,
                          # 'access_token': 'TGT-4931-lpGGA9Z7YSsrEK9TW7eKE7SWG7ZbVpflaM1cMRlipeDloQhPXP',
                          'p': '1',
                          'currentPage': '1'}
        rsp_temp = session.post(url=url_updata_lce, headers=headers_temp, data=from_data_temp)
        print(rsp_temp.json().get('data').get('list')[0])

    def dele_excel(self):
        if exists(self.excel_path):
            remove(self.excel_path)

    def enter_imei_to_saas2(self,imei):
        url = "https://saas2.ukelink.net/bss/terminal/Add"
        headers = {'Host': 'saas2.ukelink.net',
                   'Connection': 'keep-alive',
                   'Accept-Language': 'zh-CN',
                   'Content-Type': 'text/plain;charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                   'Origin': 'https://saas2.ukelink.net',
                   'Referer': 'https://saas2.ukelink.net/saas/resourceManager/terminal?v=51231.99410528367&hidePanle=true'}

        params = {'code': 'autoupload',
                  'description': '',
                  'hardVersion': '1.1.1',
                  'imei': imei,
                  'loginCustomerId': '59409a6556a5956b828b8d5e',
                  'mgmtUrl': '',
                  'mvnoId': '570e05e256a5951a9d725f0b',
                  'name': 'autoupload',
                  'orgId': '57a855e756a59570858edabd',
                  'ownerType': '0',
                  'partnerCode': 'UKSAS',
                  'password': '',
                  'seedIccid': '',
                  'softVersion': '1.1.1',
                  'ssid': '',
                  'state': 'NORMAL',
                  'streamNo': 'web_saas1626680320536279525',
                  'targetMarket': '1',
                  'type': 'E1',
                  'wifiPassword': ''}
        sessions = self.login_session
        r = sessions.post(headers=headers, url=url, params=params)
        print(r.json())

    def register_account(self,imei):
        url = "https://saas2.ukelink.net/bss/customerTerminal/TerminalUserRegister"
        headers = {
            'Host': 'saas2.ukelink.net',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }
        params={
            "registerType": "EMAIL",
            "countryCode": "86",
            "phone": "123456",
            "email": imei + "@auto.com",
            "username": imei + "@auto.com",
            "password": "123456",
            "lastname": "auto",
            "firstname": "auto",
            "imei": imei,
            "identificationType": "IDENTITY",
            "identification": "123456",
            "registerCountry": "CN",
            "orgId": "57a855e756a59570858edabd",
            "currencyType": "EUR",
            "payType": "FREETEST",
            "customerLevel": "VIP",
            "mvnoId": "570e05e256a5951a9d725f0b",
            "streamNo": "web_saas1628565088112543880",
            "partnerCode": "UKSAS",
            "loginCustomerId": "5a6ef2b6a1fbd87379e764d5"
        }
        session = self.login_session
        r = session.post(url=url,headers=headers,params=params)
        print(r.json())



if __name__ == "__main__":
    login = LoginSaas2()
    input_imei = input("请输入要导入证书设备的imei：").strip()
    if len(input_imei) != 15:
        print("imei不合法")
        system("pause")
    else:
        login.download_template_excel(input_imei)
        login.updata_security_LCE()
        login.dele_excel()
        system("pause")
