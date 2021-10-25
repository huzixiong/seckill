import re

import requests


# d = open(r"C:\Users\huzixiong\Desktop\uaflogs\qqxuanwu.sh", "w", encoding="utf-8")
# f = open(r"C:\Users\huzixiong\Desktop\uaflogs\qq炫舞.txt", "r", encoding="utf-8")


# print(fp)
# for i in fp:
#     print("{}{}{}{}".format("./ucnc ucNet TP set_chain_rule 2 add all://",i, i.strip(), ":0"), file=d)
#     print("{}{}{}{}".format("./ucnc ucNet TP set_chain_rule 2 add all://",i, i.strip(),":0"))
# j = 0
# for i in f:
#     if i == "\n":
#         continue
#     j = j+1
#     print("{}{}{}:0".format("./ucnc ucNet TP set_chain_rule 2 add all://",j,i.strip()),file=d)

# url = "https://site.ip138.com/g.x5m.qq.com/"

# list_ip = []
# def getX5m(ip_addr):
#     headers = {'Host': 'site.ip138.com',
#                'Connection': 'keep-alive',
#                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
#                'sec-ch-ua-mobile': '?0',
#                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#                'Accept': '*/*',
#                'Sec-Fetch-Site': 'same-origin',
#                'Sec-Fetch-Mode': 'cors',
#                'Sec-Fetch-Dest': 'empty',
#                'Referer': 'https://site.ip138.com/g.x5m.qq.com/',
#                'Accept-Encoding': 'gzip, deflate, br',
#                'Accept-Language': 'zh-CN,zh;q=0.9',
#                'Cookie': 'Hm_lvt_d39191a0b09bb1eb023933edaa468cd5=1625207053,1625456480; PHPSESSID=5ehcce99ehjgro9phvliaain3j; Hm_lpvt_d39191a0b09bb1eb023933edaa468cd5=1625456917',
#                'Content-Type': 'text/plain'
#                }
#     url = "https://site.ip138.com/domain/read.do"
#     param = {'domain': ip_addr,
#     'time': '1625456925681'}
#     fp = open(r"C:\Users\huzixiong\Desktop\uaflogs\ip.cfg", "a", encoding="utf-8")
#     try:
#         session = requests.session()
#         r = session.get(url, headers=headers, params=param)
#         # print(r.status_code)
#         print(r.json())
#
#         for i in r.json().get('data'):
#             fp.write(i["ip"] + "\n")
#     except Exception as e:
#         pass
#         # time.sleep(5)
#         # getX5m(ip_addr)
#     finally:
#         fp.close()
#
# def get_url():
#     f = open(r"C:\Users\huzixiong\Desktop\uaflogs\qq炫舞.txt", "r", encoding="utf-8")
#     for url_dns in f:
#         print(url_dns)
#         if url_dns == "None":
#             continue
#         getX5m(url_dns.strip())

def get_token():
    url = "https://site.ip138.com/www.xiaomi.com/"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'site.ip138.com',
        'Referer': 'https://site.ip138.com/gifshow.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    r = requests.get(url=url, headers=headers)
    print(r.status_code)
    pattern = re.compile(r".*?TOKEN = '(.*?)'", re.S)
    parse = re.search(pattern, r.text).group(1)
    print(parse)
    return parse


def write_token(arg_token):
    url = "https://site.ip138.com/domain/write.do"
    # headers = {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'Connection': 'keep-alive',
    #     'Host': 'site.ip138.com',
    #     'Referer': 'https://site.ip138.com/gifshow.com/',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_d39191a0b09bb1eb023933edaa468cd5=1625649429,1626055001; PHPSESSID=9610ued5usq8a3iqqpgr9me107; Hm_lpvt_d39191a0b09bb1eb023933edaa468cd5=1626055126',
        'Host': 'site.ip138.com',
        'Referer': 'https://site.ip138.com/www.baidu.com/',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    params = {'input': 'www.xiaomi.com',
              'token': arg_token}
    r = requests.get(url=url, headers=headers, params=params)
    print(r.status_code)
    print(r.json())


if __name__ == "__main__":
    # get_token()
    write_token(get_token())
