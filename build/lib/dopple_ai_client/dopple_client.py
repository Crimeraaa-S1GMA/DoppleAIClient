import urllib.parse
from .api_urls import *

from .chat import DoppleChat
from .bot import DoppleBot
from .user_data import UserData

from .dopple_request import DoppleRequest
from .dopple_request_error import DoppleRequestError

import requests
import json

class DoppleClient:
    def __init__(self, **kwargs) -> None:
        self.request_helper = DoppleRequest(dopple_token="", user_agent=user_agent)
        self.user_id = ""

        if "token" in kwargs.keys() and "id" in kwargs.keys():
            self.request_helper.dopple_token = kwargs["token"]
            self.user_id = kwargs["id"]
        elif "email" in kwargs.keys() and "password" in kwargs.keys():
            req = self.request_helper.post_nobearer(be_url + "api/users/login/", {"email" : kwargs["email"], "password" : kwargs["password"]})

            req_json = json.loads(req.text)

            self.request_helper.dopple_token = req_json["accessToken"]
            self.user_id = req_json["data"]["id"]
        else:
            print("Please provide the init function with either token and id values, or the email (can take username or email as input) and password values.")
        
        self.user_data = self.get_user_data()
    
    def get_login_values(self) -> None:
        print(f"Dopple Token: {self.request_helper.dopple_token}")
        print(f"User ID: {self.user_id}")

    def get_user_data(self) -> dict:
        req = self.request_helper.get(be_url + "api/users/" + self.user_id)

        req_json = json.loads(req.text)

        return UserData(
            email=req_json["email"],
            avatar_url=req_json["pictures"][req_json["picture"]],
            join_date=req_json["createdAt"]
        )

    ## Gets various info such as server-side settings (line-break, model, away messages), remaining trials of dopple+ features and dopple+ subscription info
    def get_user_details(self) -> dict:
        req = self.request_helper.get(ml_url + f"get_user_details?username={self.user_data.email}")

        req_json = json.loads(req.text)

        return req_json
    
    def get_dopple_info(self, dopple_id : str) -> DoppleBot:
        req = self.request_helper.post(ml_url + "get_dopple_info", {"dopple_id" : dopple_id})

        req_json = json.loads(req.text)

        bot = DoppleBot(
            dopple_id=req_json["dopple_info"]["id"],
            display_name=req_json["dopple_info"]["display_name"],
            tagline=req_json["dopple_info"]["tagline"],
            bio=req_json["dopple_info"]["bio"],
            description=req_json["dopple_info"]["description"],
            greeting=req_json["dopple_info"]["greeting"],
            avatar_url=req_json["dopple_info"]["avatar_url"],
            banner_url=req_json["dopple_info"]["banner_url"],
            banner_video_url=req_json["dopple_info"]["banner_video_url"],
            message_count=req_json["dopple_info"]["message_count"],
            creator_username=req_json["dopple_info"]["creator_username"],
            category=req_json["dopple_info"]["category"],
            subcategory=req_json["dopple_info"]["subcategory"],
            internal=req_json["dopple_info"]["made_internally"]
        )

        return bot

    def get_user_chat_dopple_ids(self) -> list:
        req = self.request_helper.post(ml_url + "get_user_chats", json={"username":self.user_data.email})

        req_response = json.loads(req.text)

        print(req_response)

        return list(req_response["relations"].keys())

    def get_user_active_chats(self) -> list:
        req = self.request_helper.post(ml_url + "get_user_chats", json={"username":self.user_data.email})

        req_response = json.loads(req.text)

        results = []

        for chat in req_response["active_chats"]:
            results.append(DoppleChat(chat_id=chat["chat_id"], dopple_id=chat["id"], email=self.user_data.email, folder="", request_helper=self.request_helper))

        return results

    def get_user_saved_chats(self) -> list:
        req = self.request_helper.post(ml_url + "get_user_chats", json={"username":self.user_data.email})

        req_response = json.loads(req.text)

        results = []

        for chat in req_response["saved_chats"]:
            results.append(DoppleChat(chat_id=chat["chat_id"], dopple_id=chat["id"], email=self.user_data.email, folder="saved_chats", request_helper=self.request_helper))

        return results
    
    def search_dopples(self, query : str) -> list:
        req = self.request_helper.post(ml_url + "search_dopples", {"search_term":query})

        req_response = json.loads(req.text)

        results = []

        for result in req_response["search_results"]:
            results.append(DoppleBot(
                dopple_id=result["id"],
                display_name=result["display_name"],
                tagline=result["tagline"],
                bio=result["bio"],
                description=result["description"],
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
    
    def load_chat_from_dopple_id(self, dopple_id : str) -> DoppleChat:
        req = self.request_helper.post(ml_url + "get_chat_id", {"username":self.user_data.email,"dopple_id":dopple_id})

        chat_id = json.loads(req.text)["chat_id"]

        return DoppleChat(chat_id=chat_id, dopple_id=dopple_id, email=self.user_data.email, folder="", request_helper=self.request_helper)
    
    def load_chat_from_dopple_object(self, dopple_object : DoppleBot) -> DoppleChat:
        req = self.request_helper.post(ml_url + "get_chat_id", {"username":self.user_data.email,"dopple_id":dopple_object.dopple_id})

        chat_id = json.loads(req.text)["chat_id"]

        return DoppleChat(chat_id=chat_id, dopple_id=dopple_object.dopple_id, email=self.user_data.email, folder="", request_helper=self.request_helper)

    def set_line_break_mode(self, value : bool) -> None:
        req = self.request_helper.post(ml_url + "set_line_break_mode", json={"username":self.user_data.email, "line_break_mode" : value})
    
    def create_persona(self, name : str, info : str) -> None:
        req = self.request_helper.post(ml_url + "upsert_persona", json={"username":self.user_data.email, "old_persona_name" : "", "persona_name" : name, "persona_info" : info})
    
    def edit_persona(self, old_name : str, new_name : str, new_info : str) -> None:
        req = self.request_helper.post(ml_url + "upsert_persona", json={"username":self.user_data.email, "old_persona_name" : old_name, "persona_name" : new_name, "persona_info" : new_info})
    
    def set_default_persona(self, name : str) -> None:
        req = self.request_helper.post(ml_url + "set_default_persona", json={"username":self.user_data.email, "persona_name" : name})
    
    def delete_persona(self, name : str) -> None:
        req = self.request_helper.delete(ml_url + f"delete_persona?username={self.user_data.email}&persona_id={name}")
