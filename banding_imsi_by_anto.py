import requests


class LoginSaas2():
    def __init__(self):
        self.user_agent = self.get_user_agent()
        self.headers = self.get_headers()
        self.url_login = "https://saas2.ukelink.net/saas/index/ajax_login"
        self.session = self.get_session()

    def get_user_agent(self):
        return "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"

    def get_headers(self):
        return {'User-Agent': self.user_agent,
                'Accept-Encoding': 'gzip, deflate',
                'Accept': 'application/json, text/plain, */*',
                'Connection': 'keep-alive'}

    def get_session(self):
        from_data = {"userCode": "qianjunxia",
                     "password": "e10adc3949ba59abbe56e057f20f883e"
                     }
        session = requests.session()
        res = session.post(url=self.url_login, headers=self.headers, data=from_data)
        print(res.json())
        return session


class DoTask(LoginSaas2):

    def __init__(self):
        self.url_username_find = "https://saas2.ukelink.net/bss/customerTerminal/QueryCustListByUsernameRequest"
        super().__init__()

    def find_username_orgid_mvnoid(self):
        params = {'loginCustomerId': '59409a6556a5956b828b8d5e',
                  'partnerCode': 'UKSAS',
                  'streamNo': 'web_saas162919280812123636',
                  'username': 'huzixiong_001@test.com'}
        res = self.session.post(headers=self.headers, url=self.url_username_find, data=params)
        print(res.json()["data"][0])


if __name__ == "__main__":
    # LoginSaas2()
    DoTask().find_username_orgid_mvnoid()
