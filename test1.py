import json
import os
import subprocess
import time

import requests
from openpyxl import load_workbook

from getDeviceConnect import get_device_connect

User_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
headers = {'User-Agent': User_agent,
           'Accept-Encoding': 'gzip, deflate',
           'Accept': 'application/json, text/plain, */*',
           'Connection': 'keep-alive'}
url_login = "https://saas2.ukelink.net/saas/index/ajax_login"
from_data = {"userCode": "qianjunxia",
             "password": "e10adc3949ba59abbe56e057f20f883e"
             }

url_online = "https://saas2.ukelink.net/manage/config/query"
from_online_data = {"lid": "onlineTerminal--onlineTerminalLans"}

url_home = "https://saas2.ukelink.net/saas/index/home"
url_imei = "https://saas2.ukelink.net/bss/terminal/Add"


def sessions():
    session = requests.session()
    session.headers = User_agent
    return session


def saas_login(url=url_login):
    session = sessions()
    res = session.post(url=url_login, headers=headers, data=from_data)
    return session


def saas_online(url=url_online):
    session = sessions()
    res_online = session.post(url=url_online, headers=headers, data=from_online_data)
    print(res_online.text)


def saas_home(url=url_home):
    session = sessions()
    rsp = session.get(url=url_home, headers=headers)
    with open(r"C:\Users\huzixiong\Desktop\uaflogs\home.html", "w", encoding="utf-8") as f:
        f.write(rsp.text)


def add_imei(url=url_imei):
    from_imei_data = {"code": "111111123654987",
                      "description": "autoupload",
                      "hardVersion": "1.1.1",
                      "imei": "111111123654988",
                      "loginCustomerId": "59409a6556a5956b828b8d5e",
                      "mgmtUrl": "",
                      "mvnoId": "603624976a3bfd0001b7ad67",
                      "name": "111111123654987",
                      "orgId": "603625ad0aea6e23b424e49c",
                      "ownerType": 0,
                      "partnerCode": "UKSAS",
                      "password": "",
                      "seedIccid": "",
                      "softVersion": "1.1.1",
                      "ssid": "",
                      "state": "NORMAL",
                      "streamNo": "web_saas1624349688269372308",
                      "targetMarket": 1,
                      "type": "G2",
                      "wifiPassword": ""
                      }
    session = sessions()
    res = session.post(url=url_login, headers=headers, data=from_data)
    print(res.text)
    rep = session.post(url=url_imei, headers=headers, data=from_imei_data)
    print(rep.json())


def find_imei_usernam_id(imei):
    url_find_uername = "https://saas2.ukelink.net/bss/customerTerminal/QueryCustListByUsernameRequest"
    from_username_data = {"loginCustomerId": "59409a6556a5956b828b8d5e",
                          "partnerCode": "UKSAS",
                          "streamNo": "web_saas1624412082538673722",
                          "username": "huzixiong_001@test.com"}

    url_find_imei = "https://saas2.ukelink.net/bss/terminal/Query"
    from_imei_data = {"imei": imei,
                      "loginCustomerId": "59409a6556a5956b828b8d5e",
                      "partnerCode": "UKSAS",
                      "streamNo": "web_saas1624414611492753570"}
    session = sessions()
    session.post(url=url_login, headers=headers, data=from_data)
    rsp_username = session.post(url=url_find_uername, headers=headers, data=from_username_data)
    rsp_imei = session.get(url_find_imei, headers=headers, params=from_imei_data)
    # print(res.json())
    # print(rsp_username.json())
    # print(rsp_imei.json())
    user_name_id = rsp_username.json()["data"][0]["id"]
    imei_id = rsp_imei.json()["data"]["dataList"][0].get("id")
    # print(user_name_id,imei_id)
    return (user_name_id, imei_id, session)


def active_terminal():
    imei = input("请输入imei：")
    user_name_id, imei_id, session = find_imei_usernam_id(imei)
    url_active = "https://saas2.ukelink.net/bss/terminal/Activate"
    from_active_data = {"customerId": user_name_id,
                        "flag": 0,
                        "loginCustomerId": "59409a6556a5956b828b8d5e",
                        "partnerCode": "UKSAS",
                        "streamNo": "web_saas1624415954453828740",
                        "terminalId": imei_id}
    rsp_active = session.post(url=url_active, headers=headers, data=from_active_data)
    print("设备账号绑定imei：", rsp_active.json().get("resultDesc"))


def updata_excel_file():
    url_excel_file = "https://saas2.ukelink.net/attachment/index/uploadDoc"
    headers_url = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        # 'Content-Type': 'multipart/form-data',
        'Accept': '*/*', }
    files = {
        "imgFile": ("import_targetTypeIMEI_template_zh-CN.xlsx", open(
            r"C:\Users\huzixiong\Desktop\临时\jd_seckill-modify\jd_seckill-modify\import_targetTypeIMEI_template_zh-CN.xlsx",
            "rb"), "application/excel"),
        "id": "WU_FILE_1",
        "name": "import_targetTypeIMEI_template_zh-CN.xlsx",
        "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "lastModifiedDate": "Wed Jun 23 2021 11:29:11 GMT+0800 (中国标准时间)"
    }
    params = {
        'fname': 'imgFile'
    }
    session = sessions()
    rsp = session.post(url=url_excel_file, headers=headers_url, files=files, params=params)
    print(rsp.json())


def updata_security_LCE():
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
    session = saas_login()
    rsp = session.post(url=url_excel_file, headers=headers_url, files=files)
    url_temp_url = rsp.json()['data'].get('url')
    print(url_temp_url)
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
    print(rsp_temp.text)

    # os.remove(r"C:\Users\huzixiong\Desktop\临时\jd_seckill-modify\jd_seckill-modify\template.xlsx")
    # print(rsp_temp.json().get('data').get('list')[0]['服务器错误信息'])


def updata_cfg_file():
    url_cfg_file = "https://saas2.ukelink.net/attachment/aws/uploadTerminalConfig?fname=configFile"
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        # 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary33HBkKD5WLef8dpJ',
        'Accept': '*/*', }
    # 'Cookie': 'PHPSESSID=dh2a5db4lplud8hsgfvsbf27lo; access_token=TGT-1839-nba5AuvliSKlhrWe1Oe9qCOEOFobygO9udAJvKo9LbR17agYn6; loginCustomerId=59409a6556a5956b828b8d5e; language=zh-CN'}
    files = {
        "configFile": ("T350_993_V01.cfg", open(
            r"C:\Users\huzixiong\Desktop\T350_993_V01.cfg", "rb"), "application/octet-stream"),
        "id": "WU_FILE_1",
        "name": "T350_993_V01.cfg",
        "type": "application/octet-stream",
        "lastModifiedDate": "Wed Jun 23 2021 11:29:11 GMT+0800 (中国标准时间)",
        "size": "1004"
    }
    session = saas_login()
    t = session.cookies.items()
    print(t)
    r = session.post(url=url_cfg_file, headers=headers, files=files)
    print(r.json().get('ObjectURL'), r.json().get('fileMd5'))


def updata_cfg_excel_commite():
    url_cfg_excel_file = "https://saas2.ukelink.net/bss/terminalfunction/AddTerminalFunction"
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*'}
    payload = {
        "funType": "OEMCFG_MIFI",
        "targetType": "IMEI",
        "file": "",
        "status": "",
        "funDesc": "AutoUpload",
        "resUrl": "https://s3-us-west-2.amazonaws.com/ukl-devtest-saastest-181113/12922b3ad3bebfad5f44a193e68ed268.cfg",
        "md5": "9472cc6bd2372f874caf927bd69d9851",
        "version": "20210625110833",
        "dataList": [
            {
                "IMEI": "869680025355719"
            }
        ],
        "streamNo": "web_saas1624601601057149194",
        "partnerCode": "UKSAS",
        "loginCustomerId": "59409a6556a5956b828b8d5e"
    }
    jdata = json.dumps(payload)
    session = saas_login()
    print(session.cookies)
    r = session.post(url=url_cfg_excel_file, headers=headers, data=jdata)
    # print(r.request.headers)
    print(r.text)


def download_template_excel(imei):
    url_download = "https://saas2.ukelink.net/htemp/resources/bss/import_cert_template_en.xlsx"
    headers = {'Host': 'saas2.ukelink.net',
               'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Referer': 'https://saas2.ukelink.net/saas/bssManager/certImport?v=17835.835044942196&hidePanle=true'}
    session = saas_login()
    r = session.get(url=url_download, headers=headers, params={'v': '263'})
    print(r.status_code)
    with open(r"./template.xlsx", "wb") as f:
        f.write(r.content)
    path_excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.xlsx')
    if not os.path.exists(path_excel):
        raise ("没有找到excel文件")
    wb = load_workbook(path_excel)
    sheet = wb.worksheets[0]
    sheet["A3"] = imei
    wb.save(path_excel)
    # os.remove(r'./template.xlsx')


def S2C_switch_vism(imei):
    url_switch_vsim = "https://saas2.ukelink.net/oss/terminalMonitor/uploadTerminalCmd"
    headers = {'Host': 'saas2.ukelink.net',
               'Connection': 'keep-alive',
               'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/javascript, */*; q=0.01',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
               'Origin': 'https://saas2.ukelink.net',
               'Accept-Encoding': 'gzip, deflate, br'}
    payload = {
        "cmd": 131,
        "imeiList": [
            {
                "imei": imei,
                "userType": "2"
            }
        ],
        "param": 39,
        "streamNo": "web_saas1626070455990351714",
        "partnerCode": "UKSAS",
        "loginCustomerId": "59409a6556a5956b828b8d5e"
    }
    jdata = json.dumps(payload)
    session = saas_login()
    r = session.post(url=url_switch_vsim, headers=headers, data=jdata)
    # print(r.json())


def enter_imei_to_saas2(imei):
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
    sessions = saas_login()
    r = sessions.post(headers=headers, url=url, params=params)
    print(r.json())


def binding_imei_gcbu():
    headers = {'Host': 'saas2.ukelink.net',
               'Connection': 'keep-alive',
               'Accept-Language': 'zh-CN',
               'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/javascript, */*; q=0.01',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
               'Referer': 'https://saas2.ukelink.net/saas/resourceManager/orientCardManager_self?v=41338.32949862834&hidePanle=true',
               'Cookie': 'PHPSESSID=cs5e3vdu57r0i15pe88il5b4v5; access_token=TGT-6345-e5VZdsarvfDdVfvyqNLfsC9xhy2FhrBcYFQHCxHYWkIPLeetsY; language=zh-CN; loginCustomerId=5a6ef2b6a1fbd87379e764d5'}
    url_banding = "https://saas2.ukelink.net/css/vsimbinding/add"
    from_data = {
        "mvnoId": "570e05e256a5951a9d725f0b",
        "orgId": "57a855e756a59570858edabd",
        "userCode": "huzixiong_001@test.com",
        "bindingTime": str(round(time.time())) + "000",
        "totalTime": "24",
        "imsi": "460044108324783",
        "status": "1",
        "useMode": "1",
        "empty": "一键清空",
        "userMvnoId": "570e05e256a5951a9d725f0b",
        "userOrgId": "57a855e756a59570858edabd",
        "operatorName": "qianjunxia",
        "isAdmin": "1",
        "streamNo": "web_saas1626770288563662562",
        "partnerCode": "UKSAS",
        "loginCustomerId": "5a6ef2b6a1fbd87379e764d5",
        "timezone": "GMT+8:00"
    }

    session = saas_login()
    r = session.post(url=url_banding, json=from_data, headers=headers)
    print(r.text)


def pingResult():
    while True:
        time.sleep(1)
        result = subprocess.getstatusoutput("adb shell ping -c 1 www.xiaomi.com")[1].find("0%")
        if result != -1:
            print("云卡网络ping通")
            return True


def binding_imsi():
    url = 'https://saas2.ukelink.net/css/vsimbinding/available'
    params = {'isAdmin': '1',
              'loginCustomerId': '59409a6556a5956b828b8d5e',
              'mcc': '460',
              'mnc': '00',
              'mvnoId': '56a607473144373d73e1119d',
              'orgId': '56a71be2f5b95a6ed2ce98ff',
              'partnerCode': 'UKSAS',
              'status': '3',
              'streamNo': 'web_saas1628737007211985907',
              'timezone': 'GMT+8:00',
              'userCode': 'huzixiong_001@test.com',
              'userMvnoId': '570e05e256a5951a9d725f0b',
              'userOrgId': '57a855e756a59570858edabd'
              }
    headers = {'Accept-Language': 'zh-CN',
               'Time-Zone': 'GMT8',
               'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
               }
    session = saas_login()
    r = session.get(url=url,headers=headers,params=params).json()['data']
    print(r)


def main():
    i = 1
    while True:
        if get_device_connect():
            print("检测到设备")
            break
    while True:
        if pingResult():
            print("检测到设备云卡网络已经ok")
            time.sleep(10)
            S2C_switch_vism("864652031856332")
            print("发起{}换卡".format(i))
        i = i + 1


if __name__ == "__main__":
    # updata_excel_file()
    # updata_cfg_file()
    # active_terminal()
    # updata_cfg_excel_commite()
    # S2C_switch_vism("864652031856332")
    # main()
    # download_template_excel("1")
    # updata_security_LCE()
    # os.remove(os.path.abspath("./template.xlsx"))
    enter_imei_to_saas2("868868042092669")
    # binding_imei_gcbu()
    # binding_imsi()
