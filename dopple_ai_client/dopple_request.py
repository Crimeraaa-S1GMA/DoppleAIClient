from .dopple_request_error import DoppleRequestError

import requests

class DoppleRequest:
    def __init__(self, dopple_token : str, user_agent : str) -> None:
        self.dopple_token : str = dopple_token
        self.user_agent : str = user_agent

        self.good_status_codes : list[int] = [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
    
    def get(self, url : str):
        req = requests.get(url=url, headers={
            "Accept": "*/*",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.dopple_token),
            "Content-Type": "application/json",
            "User-Agent": self.user_agent
        })

        if req.status_code not in self.good_status_codes:
            raise(DoppleRequestError(req.status_code))

        return req
    
    def post(self, url : str, json : dict):
        req = requests.post(url=url, headers={
            "Accept": "*/*",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.dopple_token),
            "Content-Type": "application/json",
            "User-Agent": self.user_agent
        }, json=json)

        if req.status_code not in self.good_status_codes:
            raise(DoppleRequestError(req.status_code))

        return req
    
    def delete(self, url : str, json : dict):
        req = requests.delete(url=url, headers={
            "Accept": "*/*",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.dopple_token),
            "Content-Type": "application/json",
            "User-Agent": self.user_agent
        }, json=json)

        if req.status_code not in self.good_status_codes:
            raise(DoppleRequestError(req.status_code))

        return req
    
    def get_nobearer(self, url : str, json : dict):
        req = requests.get(url=url, headers={
            "Accept": "*/*",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent
        }, cookies={
            "accessToken" : self.dopple_token
        }, json=json)

        if req.status_code not in self.good_status_codes:
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

        if req.status_code not in self.good_status_codes:
            raise(DoppleRequestError(req.status_code))

        return req
