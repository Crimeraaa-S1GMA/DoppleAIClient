import requests

from .dopple_request_error import DoppleRequestError

class DoppleRequest:
    def __init__(self, dopple_token, user_agent) -> None:
        self.dopple_token = dopple_token
        self.user_agent = user_agent
    
    def get(self, url):
        req = requests.get(url=url, headers={
            "Accept": "*/*",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.dopple_token),
            "Content-Type": "application/json",
            "User-Agent": self.user_agent
        })

        if req.status_code != 200:
            raise(DoppleRequestError(req.status_code))

        return req
    
    def post(self, url, json):
        req = requests.post(url=url, headers={
            "Accept": "*/*",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.dopple_token),
            "Content-Type": "application/json",
            "User-Agent": self.user_agent
        }, json=json)

        if req.status_code != 200:
            raise(DoppleRequestError(req.status_code))

        return req
    
    def get_nobearer(self, url):
        req = requests.get(url=url, headers={
            "Accept": "*/*",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent
        }, cookies={
            "accessToken" : self.dopple_token
        })

        if req.status_code != 200:
            raise(DoppleRequestError(req.status_code))

        return req
    
    def post_nobearer(self, url, json):
        req = requests.post(url=url, headers={
            "Accept": "*/*",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent
        }, json=json, cookies={
            "accessToken" : self.dopple_token
        })

        if req.status_code != 200:
            raise(DoppleRequestError(req.status_code))

        return req
