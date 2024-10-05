import urllib.parse
from .api_urls import *

from .chat import DoppleChat
from .bot import DoppleBot
from .user_data import UserData
from .profile import DoppleProfile

from .dopple_request import DoppleRequest
from .dopple_request_error import DoppleRequestError

import requests
import json

class DoppleClient:
    def __init__(self, **kwargs) -> None:
        self.req : DoppleRequest = DoppleRequest(dopple_token="", user_agent=user_agent)
        self.user_id : str = ""

        if "token" in kwargs.keys() and "id" in kwargs.keys():
            self.req.dopple_token = kwargs["token"]
            self.user_id = kwargs["id"]
        elif "email" in kwargs.keys() and "password" in kwargs.keys():
            req = self.req.post_nobearer(be_url + "api/users/login/", {"email" : kwargs["email"], "password" : kwargs["password"]})

            req_json = json.loads(req.text)

            self.req.dopple_token = req_json["accessToken"]
            self.user_id = req_json["data"]["id"]
        else:
            print("Please provide the init function with either token and id values, or the email (can take username or email as input) and password values.")
        
        self.user_data : UserData = self.get_user_data()
    
    def get_login_values(self) -> dict:
        return {
            "token" : self.req.dopple_token,
            "user_id" : self.user_id,
        }

    def get_user_data(self) -> dict:
        response : requests.Response = self.req.get(be_url + "api/users/" + self.user_id)

        req_json = json.loads(response.text)

        return UserData(
            email=req_json["email"],
            avatar_url=req_json["pictures"][req_json["picture"]],
            join_date=req_json["createdAt"],
        )

    ## Gets various info such as server-side settings (line-break, model, away messages), remaining trials of dopple+ features and dopple+ subscription info
    def get_user_details(self) -> dict:
        response : requests.Response = self.req.get(ml_url + f"get_user_details?username={self.user_data.email}")

        req_json = json.loads(response.text)

        return req_json

    def get_creator_profile(self, creator_user_id : str) -> DoppleProfile:
        response : requests.Response = self.req.get(ml_v2_url + f"get_public_user_created_dopples?creator_id={creator_user_id}&sort_by=message_count") # message_count / creation_time
        # &skip=0&limit=9 - just in case
        
        req_json = json.loads(response.text)

        return DoppleProfile(creator_user_id, req_json["creator_username"], req_json["num_subscribers"], req_json["num_dopples"], req_json["num_messages"], req_json["user_created_dopples"])
    
    def block_creator(self, creator_user_id : str) -> None:
        self.req.get(ml_url + f"block_creator?username={self.user_data.email}&user_to_block={creator_user_id}")
    
    def subscribe_creator(self, creator_user_id : str) -> None:
        self.req.post(ml_url + "subscribe_to_creator", {
            "subscriber_username" : self.user_data.email,
            "creator_username" : creator_user_id,
        })
    
    def unsubscribe_creator(self, creator_user_id : str) -> None:
        self.req.post(ml_url + "unsubscribe_from_creator", {
            "subscriber_username" : self.user_data.email,
            "creator_username" : creator_user_id,
        })
    
    def report_creator(self, creator_user_id : str, reason : str) -> None:
        self.req.post(ml_url + "unsubscribe_from_creator", {
            "reporter_username" : self.user_data.email,
            "username" : creator_user_id,
            "reason" : reason,
        })
    
    def get_dopple_info(self, dopple_id : str) -> DoppleBot:
        response : requests.Response = self.req.post(ml_url + "get_dopple_info", {"dopple_id" : dopple_id})

        req_json : dict = json.loads(response.text)

        return DoppleBot(req_json)
    
    def report_dopple(self, dopple_id : str, reason : str) -> None:
        self.req.post(ml_url + "report_dopple", {
            "username" : self.user_data.email,
            "dopple_id" : dopple_id,
            "reason" : reason,
        })

    def get_user_chat_dopple_ids(self) -> list:
        response : requests.Response = self.req.post(ml_url + "get_user_chats", json={"username":self.user_data.email})

        req_response : requests.Response = json.loads(response.text)

        return list(req_response["relations"].keys())

    def get_user_active_chats(self) -> list:
        response : requests.Response = self.req.post(ml_url + "get_user_chats", json={"username":self.user_data.email})

        req_response : requests.Response = json.loads(response.text)

        results = []

        for chat in req_response["active_chats"]:
            results.append(DoppleChat(chat_id=chat["chat_id"], dopple_id=chat["id"], email=self.user_data.email, folder="", req=self.req))

        return results

    def get_user_saved_chats(self) -> list:
        response : requests.Response = self.req.post(ml_url + "get_user_chats", json={"username":self.user_data.email})

        req_response : requests.Response = json.loads(response.text)

        results = []

        for chat in req_response["saved_chats"]:
            results.append(DoppleChat(chat_id=chat["chat_id"], dopple_id=chat["id"], email=self.user_data.email, folder="saved_chats", req=self.req))

        return results
    
    def search_dopples(self, query : str) -> list:
        response : requests.Response = self.req.post(ml_url + "search_dopples", {"search_term":query})

        req_response : requests.Response = json.loads(response.text)

        results = []

        for result in req_response["search_results"]:
            results.append(DoppleBot(result))

        return results
    
    def load_chat_from_dopple_id(self, dopple_id : str) -> DoppleChat:
        response : requests.Response = self.req.post(ml_url + "get_chat_id", {"username":self.user_data.email,"dopple_id":dopple_id})

        chat_id = json.loads(response.text)["chat_id"]

        return DoppleChat(chat_id=chat_id, dopple_id=dopple_id, email=self.user_data.email, folder="", req=self.req)
    
    def load_chat_from_dopple_object(self, dopple_object : DoppleBot) -> DoppleChat:
        response : requests.Response = self.req.post(ml_url + "get_chat_id", {"username":self.user_data.email,"dopple_id":dopple_object.dopple_id})

        chat_id = json.loads(response.text)["chat_id"]

        return DoppleChat(chat_id=chat_id, dopple_id=dopple_object.dopple_id, email=self.user_data.email, folder="", req=self.req)
    
    def create_persona(self, name : str, info : str) -> None:
        self.req.post(ml_url + "upsert_persona", json={"username":self.user_data.email, "old_persona_name" : "", "persona_name" : name, "persona_info" : info})
    
    def edit_persona(self, old_name : str, new_name : str, new_info : str) -> None:
        self.req.post(ml_url + "upsert_persona", json={"username":self.user_data.email, "old_persona_name" : old_name, "persona_name" : new_name, "persona_info" : new_info})
    
    def set_default_persona(self, name : str) -> None:
        self.req.post(ml_url + "set_default_persona", json={"username":self.user_data.email, "persona_name" : name})
    
    def delete_persona(self, name : str) -> None:
        self.req.delete(ml_url + f"delete_persona?username={self.user_data.email}&persona_id={name}")

    def set_line_break_mode(self, value : bool) -> None:
        self.req.post(ml_url + "set_line_break_mode", json={"username":self.user_data.email, "line_break_mode" : value})

    def set_premium_model_mode(self, value : bool) -> None:
        self.req.post(ml_url + "save_model_setting", json={"username":self.user_data.email, "use_premium_model" : value})
