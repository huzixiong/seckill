import requests


class SaasSession:
    """
    session 相关操作
    """

    def __init__(self):
        self.cookies_dir_path = "./cookies/"
        self.user_agents = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
        self.session = self._init_session()

    def _init_session(self):
        session = requests.session()
        session.headers = self.user_agents
        return session

    def _get_headers(self):
        return {
            "User_Agent": self.user_agents,
            "Accept": "application/json, text/plain, */*;"
                      "gzip, deflate, br;"
                      "zh-CN,zh;q=0.9;",
            "referer": "https://saas2.ukelink.net/saas/index/login",
            "Connection": "keep-alive"
        }

    def get_user_agent(self):
        return self.user_agents

    def get_session(self):
        return self.session

    def get_cookies(self):
        return self.get_session().cookies

    def upload_cookies(self, cookies):
        return self.session.cookies.update(cookies)


test = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Connection': 'keep-alive'}

"https://saas2.ukelink.net/saas/alarmManager/onlineTerminal?v=1651.560404069219&hidePanle=true#onlineTerminal"
