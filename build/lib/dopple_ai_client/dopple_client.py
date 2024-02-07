from .api_urls import *

from .chat import DoppleChat
from .bot import DoppleBot
from .user_data import UserData

from .dopple_request import DoppleRequest
from .dopple_request_error import DoppleRequestError

import requests
import json

from bs4 import BeautifulSoup

class DoppleClient:
    def __init__(self, dopple_token : str, user_id : str) -> None:
        self.dopple_token = dopple_token
        self.user_id = user_id

        self.request_helper = DoppleRequest(dopple_token=self.dopple_token, user_agent=user_agent)
        
        user_data = self.get_user_data()
        self.email = user_data.email

    def get_user_data(self) -> dict:
        req = self.request_helper.get("https://be.dopple.ai/api/users/" + self.user_id)

        req_json = json.loads(req.text)

        return UserData(
            email=req_json["email"],
            avatar_url=req_json["pictures"][req_json["picture"]],
            join_date=req_json["createdAt"]
        )
    
    def get_dopple_info(self, dopple_id : str) -> DoppleBot:
        req = self.request_helper.get(site_url + "/profile/" + dopple_id)

        bot = None

        soup = BeautifulSoup(req.text, features="html.parser")

        scripts = soup.find_all("script")

        try:
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
                        banner_video_url=content_json["banner_video_url"],
                        message_count=content_json["message_count"],
                        creator_username=content_json["creator_username"],
                        category=content_json["category"],
                        subcategory=content_json["subcategory"],
                        internal=content_json["made_internally"],
                    )
                    return bot
        except:
            return None
        
        return bot

    def get_bots_chatted_with(self) -> list:
        req = self.request_helper.post(ml_url + "/get_user_chats", json={"username":self.email})

        req_response = json.loads(req.text)

        return list(req_response["relations"].keys())
    
    def search_dopples(self, query : str) -> list:
        req = self.request_helper.post(ml_url + "/search_dopples", {"search_term":query})

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
                banner_video_url=result["banner_video_url"],
                message_count=result["message_count"],
                creator_username=result["creator_username"],
                category=result["category"],
                subcategory=result["subcategory"],
                internal=result["made_internally"],
            ))

        return results
    
    def load_chat_from_id(self, dopple_id : str) -> DoppleChat:
        req = self.request_helper.post(ml_url + "/get_chat_id", {"username":self.email,"dopple_id":dopple_id})

        chat_id = json.loads(req.text)["chat_id"]

        return DoppleChat(chat_id=chat_id, dopple_id=dopple_id, email=self.email, request_helper=self.request_helper)
    
    def load_chat_from_bot(self, dopple_bot : DoppleBot) -> DoppleChat:
        req = self.request_helper.post(ml_url + "/get_chat_id", {"username":self.email,"dopple_id":dopple_bot.dopple_id})

        chat_id = json.loads(req.text)["chat_id"]

        return DoppleChat(chat_id=chat_id, dopple_id=dopple_bot.dopple_id, email=self.email, request_helper=self.request_helper)
