import os
from functools import wraps
from json import dumps as dp
from logger import logger
from pickle import load
from time import strftime, time, localtime

import requests
from colorama import init


class SaasSession(object):
    def __init__(self):
        self.cookies_file_path = "./cookies/"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"

        self.session = self._init_session()

    def _init_session(self):
        session = requests.session()
        session.headers = self.user_agent
        return session

    def get_headers(self):
        return {
            "User-Agent": self.user_agent,
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

    def get_user_agent(self):
        return self.user_agent

    def get_session(self):
        return self.session

    def get_cookies(self):
        return self.get_session().cookies

    def set_cookies(self, cookies):
        self.session.cookies.update(cookies)

    def load_cookies_from_local(self):
        try:
            cookies_file = ""
            if not os.path.exists(self.cookies_file_path):
                return False
            for name in os.listdir(self.cookies_file_path):
                if name.endswith(".cookies"):
                    cookies_file = "{}{}".format(self.cookies_file_path, name)
                    break
            if cookies_file == "":
                return False
            with open(cookies_file, 'rb') as f:
                local_cookies = load(f)
            self.set_cookies(local_cookies)
        except Exception as e:
            logger.error(e)


class SaasLogin(SaasSession):
    def __init__(self):
        super().__init__()
        self.cookies_name = "Local_cookes"

    def login(self):
        url_login = "https://saas2.ukelink.net/saas/index/ajax_login"
        from_data = {"userCode": "qianjunxia",
                     "password": "e10adc3949ba59abbe56e057f20f883e"
                     }
        rsp = self.session.post(url_login, data=from_data)
        logger.info(rsp)
        logger.info(self.session.cookies)


class Configuration(SaasLogin):
    def __init__(self):
        super().__init__()

    def check_login(func):
        @wraps(func)
        def inn_func(self, *args, **kwargs):
            self.login()
            return func(self, *args, **kwargs)
        return inn_func

    @check_login
    def updata_cfg_excel_commite(self, imei, file, oem_type):
        # 上次需要excel格式的定制文件方法
        ObjectURL, fileMd5 = self.updata_cfg_file(file)
        url_cfg_excel_file = "https://saas2.ukelink.net/bss/terminalfunction/AddTerminalFunction"
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': '*/*'}
        payload = {
            "funType": oem_type,
            "targetType": "IMEI",
            "file": "",
            "status": "",
            "funDesc": oem_type,
            "resUrl": ObjectURL,
            "md5": fileMd5,
            "version": strftime('%Y%m%d%H%M%S', localtime(time())),
            "dataList": [
                {
                    "IMEI": imei
                }
            ],
            "streamNo": "web_saas1624601601057149194",
            "partnerCode": "UKSAS",
            "loginCustomerId": "59409a6556a5956b828b8d5e"
        }
        jdata = dp(payload)
        # print(self.session.cookies)
        # r = self.saas_session.get_session().post(url=url_cfg_excel_file, headers=headers, data=jdata)
        r = self.session.post(url=url_cfg_excel_file, headers=headers, data=jdata)
        # print("打印：",self.saas_session.get_cookies())
        # print(r.request.headers)
        # print(r.text)
        print("{}{}!".format("上传配置文件", r.json().get("resultDesc")))

    @check_login
    def updata_cfg_imsi_commit(self, imsi, file, oem_type):
        ObjectURL, fileMd5 = self.updata_cfg_file(file)
        url_cfg_excel_file = "https://saas2.ukelink.net/bss/terminalfunction/AddTerminalFunction"
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': '*/*'}
        payload = {
            "funType": oem_type,
            "targetType": "IMSI",
            "tagCode": imsi,
            "status": "1",
            "funDesc": oem_type,
            "resUrl": ObjectURL,
            "file": "",
            "md5": fileMd5,
            "version": strftime('%Y%m%d%H%M%S', localtime(time())),
            "streamNo": "web_saas1626509579244759400",
            "partnerCode": "UKSAS",
            "loginCustomerId": "59409a6556a5956b828b8d5e"
        }
        jdata = dp(payload)
        # print(self.session.cookies)
        # r = self.saas_session.get_session().post(url=url_cfg_excel_file, headers=headers, data=jdata)
        r = self.session.post(url=url_cfg_excel_file, headers=headers, data=jdata)
        # print("打印：",self.saas_session.get_cookies())
        # print(r.request.headers)
        # print(r.text)
        print("{}{}!".format("上传配置文件", r.json().get("resultDesc")))

    def updata_cfg_file(self, file_Local_cfg):

        url_cfg_file = "https://saas2.ukelink.net/attachment/aws/uploadTerminalConfig?fname=configFile"
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Accept': '*/*', }
        files = {
            "configFile": ("T350_993_V01.cfg", open(
                file_Local_cfg, "rb"), "application/octet-stream"),
            "id": "WU_FILE_1",
            "name": "T350_993_V01.cfg",
            "type": "application/octet-stream",
            "lastModifiedDate": "Wed Jun 23 2021 11:29:11 GMT+0800 (中国标准时间)",
            "size": "1004"
        }
        # r = self.saas_session.get_session().post(url=url_cfg_file, headers=headers, files=files)
        r = self.session.post(url=url_cfg_file, headers=headers, files=files)
        return (r.json().get('ObjectURL'), r.json().get('fileMd5'))

    def action(self):
        self.type = ""
        while True:
            print("#########################################")
            print(
                "\n【1】设备定制文件（rom定制文件）\n【2】MIFIKV定制文件（云卡定制文件）\n【3】流量防护黑名单（云卡流量防护文件）\n【4】Uservice扩展配置\n【5】物理种子卡fplmn文件\n【6】物理种子卡资费文件（fee）\n")
            # print(
            # "*******1.设备定制文件（rom定制文件）,2.MIFIKV定制文件（云卡定制文件）,3.流量防护黑名单（云卡流量防护文件）,4.Uservice扩展配置,5.物理种子卡fplmn文件,6.物理种子卡资费文件（fee）*******")
            print("#########################################")
            input_number = input("请选择功能类型（123456）：")
            print()
            if input_number != "1" and input_number != "2" and input_number != "3" and input_number != "4" and input_number != "5" and input_number != "6":
                # print("输入错误，请选择对应功能类型（数字）！")
                print('\033[1;35m 输入错误，请选择对应功能类型（如：1）！\033[0m')
                continue
            if input_number == "1":
                self.type = "OEMCFG"
            elif input_number == "2":
                self.type = "OEMCFG_MIFI"
            elif input_number == "3":
                self.type = "BW"
            elif input_number == "4":
                self.type = "EXPAND_CFG"
            elif input_number == "5":
                self.type = "ROAM"
            elif input_number == "6":
                self.type = "ROAMFEE"
            if input_number == "5" or input_number == "6":
                input_imei = input("请输入设备imsi：")
            else:
                input_imei = input("请输入设备imei：")
            if len(input_imei.strip()) != 15:
                print('\033[1;35m 输入的imei错误，请检查imei是否15位！\033[0m')
                # print("输入的imei错误，请检查imei是否15位！")
                continue
            elif isinstance(input_imei, int):
                print('\033[1;35m 输入的imei错误，请检查是否是纯数字！\033[0m')
                # print("输入的imei错误，请检查是否是纯数字！")
                continue
            input_file_paht = input("请输入配置文件路径（直接把文件拖入即可）：")
            try:
                if os.path.splitext(input_file_paht)[1] != ".cfg":
                    print('\033[1;35m 注意：配置文件要以cfg结尾！拖入的文件不能有空格，如果有空格请去除空格后再拖入！\033[0m')
                    # print("注意：配置文件要以cfg结尾！拖入的文件不能有空格，如果有空格请去除空格后再拖入！")
                    continue
            except Exception as e:
                print(e)
            print("正在上传配置文件.....")
            if self.type == "ROAM" or self.type == "ROAMFEE":
                self.updata_cfg_imsi_commit(input_imei, input_file_paht, self.type)
            else:
                self.updata_cfg_excel_commite(input_imei, input_file_paht, self.type)
            os.system("pause")


if __name__ == "__main__":
    init(autoreset=True)
    test = Configuration()
    test.action()
