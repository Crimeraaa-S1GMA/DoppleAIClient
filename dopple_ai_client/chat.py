from .api_urls import *
from .response import DoppleResponse
from .message import DoppleMessage
from .dopple_request_error import DoppleRequestError
from .dopple_request import DoppleRequest

import requests
import json

class DoppleChat:
    def __init__(self, chat_id : str, dopple_id : str, email : str, folder : str, req : DoppleRequest) -> None:
        self.chat_id : str = chat_id
        self.dopple_id : str = dopple_id
        self.email : str = email
        self.folder : str = folder

        self.req : DoppleRequest = req
    
    def get_chat_history(self, limit = 50, skip = 0) -> list:
        response : requests.Response = self.req.post(ml_url + "/get_paginated_chat_history", {"folder": self.folder, "username":self.email,"dopple_id":self.dopple_id, "chat_id":self.chat_id,"limit":limit,"skip":skip})

        req_response : requests.Response = json.loads(response.text)

        messages = []

        for msg in req_response["paginated_chat_history"]:
            msg_object = DoppleMessage(content=msg["message"]["data"]["content"], type=msg["message"]["type"])
            msg_object.from_msg(msg)
            messages.append(msg_object)
        return messages
    
    def clear_chat_history(self) -> None:
        self.req.post(ml_url + "/clear_chat_history", {"folder": self.folder, "username":self.email,"dopple_id":self.dopple_id, "chat_id":self.chat_id})
    
    def send_message(self, message : str, reroll = False) -> DoppleResponse:
        response : requests.Response = self.req.post_nobearer(site_url + "api/messages/send" + ("?action=reroll" if reroll else ""), {"streamMode":"none","chatId":self.chat_id,"folder":self.folder,"username":self.email,"id":self.dopple_id,"userQuery":message})
        
        req_response : requests.Response = json.loads(response.text)
        return DoppleResponse(message=req_response["response"], timestamp=req_response["timestamp"], model=req_response["model"])

    def edit_last_user_message(self, new_message : str) -> str:
        response : requests.Response = self.req.post_nobearer(site_url + "api/messages/send?action=edit", {"streamMode":"none","chatId":self.chat_id,"folder":self.folder,"username":self.email,"id":self.dopple_id,"userQuery":new_message})
        
        req_response : requests.Response = json.loads(response.text)
        return req_response["response"]

    def edit_last_bot_message(self, new_message : str) -> None:
        self.req.post(ml_url + "edit_last_ai_response", {"chat_id":self.chat_id,"folder":self.folder,"username":self.email,"dopple_id":self.dopple_id,"new_ai_response":new_message})

    def commit_response(self, response : str) -> None:
        self.req.post(ml_url + "commit_rerolled_response", {"chat_id":self.chat_id,"folder":self.folder,"username":self.email,"dopple_id":self.dopple_id,"ai_response":response})
    
    def delete_last_user_message(self) -> None:
        self.req.post(ml_url + "delete_last_user_message", {"folder": self.folder, "username":self.email,"dopple_id":self.dopple_id, "chat_id":self.chat_id})
    
    def delete_last_ai_response(self) -> None:
        self.req.post(ml_url + "delete_last_ai_response", {"folder": self.folder, "username":self.email,"dopple_id":self.dopple_id, "chat_id":self.chat_id})
    
    def delete_chat(self) -> None:
        self.req.post(ml_url + "delete_chat", {"folder": self.folder, "username":self.email,"dopple_id":self.dopple_id, "chat_id":self.chat_id})
