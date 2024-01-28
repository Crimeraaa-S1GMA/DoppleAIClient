from .api_urls import *

from .chat import DoppleChat
from .bot import DoppleBot

import requests
import json

from bs4 import BeautifulSoup

class DoppleClient:
    def __init__(self, dopple_token : str, username : str) -> None:
        self.dopple_token = dopple_token
        self.username = username
    
    def get_dopple_info(self, dopple_id : str) -> DoppleBot:
        req = requests.get(site_url + "/profile/" + dopple_id, headers={
            "Accept": "application/json",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.dopple_token),
            "Content-Type": "application/json",
            "User-Agent": user_agent
        })

        bot = None

        soup = BeautifulSoup(req.text, features="html.parser")

        scripts = soup.find_all("script")

        for script in scripts:
            content = str(script.decode_contents())
            if dopple_id in content and "id" in content and "tagline" in content and "bio" in content and "greeting" in content: # check for the actual thing
                content = "{" + content.split("{", maxsplit=1)[1]
                content = content.split("\\n\"])", maxsplit=1)[0]
                content = content.replace("\\\"", "\"")
                content = content.replace("\\\\\"", "\\\"")
                content_json = json.loads(content)
                bot = DoppleBot(
                    dopple_id=content_json["id"],
                    display_name=content_json["display_name"],
                    tagline=content_json["tagline"],
                    bio=content_json["bio"],
                    greeting=content_json["greeting"],
                    avatar_url=content_json["avatar_url"],
                    banner_url=content_json["banner_url"],
                    banner_video_url=content_json["banner_video_url"]
                )
                return bot
        
        return bot

    def get_bots_chatted_with(self) -> list:
        req = requests.post(ml_url + "/get_user_chats", headers={
            "Accept": "application/json",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.dopple_token),
            "Content-Type": "application/json",
            "User-Agent": user_agent
        }, json={"username":self.username})

        req_response = json.loads(req.text)

        return list(req_response["relations"].keys())
    
    def search_dopples(self, query : str) -> list:
        req = requests.post(ml_url + "/search_dopples", headers={
            "Accept": "application/json",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.dopple_token),
            "Content-Type": "application/json",
            "User-Agent": user_agent
        }, json={"search_term":query})

        req_response = json.loads(req.text)

        results = []

        for result in req_response["search_results"]:
            results.append(DoppleBot(
                dopple_id=result["id"],
                display_name=result["display_name"],
                tagline=result["tagline"],
                bio=result["bio"],
                greeting=result["greeting"],
                avatar_url=result["avatar_url"],
                banner_url=result["banner_url"],
                banner_video_url=result["banner_video_url"]
            ))

        return results
    
    def load_chat(self, dopple_id : str) -> DoppleChat:
        req = requests.post(ml_url + "/get_chat_id", headers={
            "Accept": "application/json",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.dopple_token),
            "Content-Type": "application/json",
            "User-Agent": user_agent
        }, json={"username":self.username,"dopple_id":dopple_id})

        chat_id = json.loads(req.text)["chat_id"]

        return DoppleChat(chat_id=chat_id, dopple_id=dopple_id, username=self.username, token=self.dopple_token)
    
    def load_chat(self, dopple_bot : DoppleBot) -> DoppleChat:
        req = requests.post(ml_url + "/get_chat_id", headers={
            "Accept": "application/json",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.dopple_token),
            "Content-Type": "application/json",
            "User-Agent": user_agent
        }, json={"username":self.username,"dopple_id":dopple_bot.dopple_id})

        chat_id = json.loads(req.text)["chat_id"]

        return DoppleChat(chat_id=chat_id, dopple_id=dopple_bot.dopple_id, username=self.username, token=self.dopple_token)
