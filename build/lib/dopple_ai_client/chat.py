from .api_urls import *
from .response import DoppleResponse
from .message import DoppleMessage

import requests
import json

class DoppleChat:
    def __init__(self, chat_id, dopple_id, username, token) -> None:
        self.chat_id = chat_id
        self.dopple_id = dopple_id
        self.username = username
        self.token = token
    
    def get_chat_history(self, limit = 50, skip = 0) -> list:
        req = requests.post(ml_url + "/get_paginated_chat_history", headers={
            "Accept": "application/json",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.token),
            "Content-Type": "application/json",
            "User-Agent": user_agent
        }, json={"folder": "", "username":self.username,"dopple_id":self.dopple_id, "chat_id":self.chat_id,"limit":limit,"skip":skip})
        req_response = json.loads(req.text)

        messages = []

        for msg in req_response["paginated_chat_history"]:
            messages.append(DoppleMessage(
                content=msg["message"]["data"]["content"],
                type=msg["message"]["type"],
                timestamp=msg["timestamp"],
                nsfw=msg["message"]["data"]["additional_kwargs"]["nsfw"],
                emotion_image_url=msg["message"]["data"]["additional_kwargs"]["dopple_emotion_image_url"],
                example=msg["message"]["data"]["example"],
            ))
        return messages
    
    def clear_chat_history(self) -> None:
        req = requests.post(ml_url + "/clear_chat_history", headers={
            "Accept": "application/json",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.token),
            "Content-Type": "application/json",
            "User-Agent": user_agent
        }, json={"folder": "", "username":self.username,"dopple_id":self.dopple_id, "chat_id":self.chat_id})
    
    def send_message(self, message, reroll = False) -> DoppleResponse:
        req = requests.post(api_url + "/messages/send" + ("?action=reroll" if reroll else ""), headers={
            "Accept": "*/*",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Content-Type": "application/json",
            "User-Agent": user_agent
        }, json={"streamMode":"none","chatId":self.chat_id,"folder":"","username":self.username,"id":self.dopple_id,"userQuery":message}, cookies={
            "accessToken" : self.token
        })
        req_response = json.loads(req.text)
        return DoppleResponse(message=req_response["response"], timestamp=req_response["timestamp"])

    def edit_message(self, new_message) -> str:
        req = requests.post(api_url + "/messages/send?action=edit", headers={
            "Accept": "*/*",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Content-Type": "application/json",
            "User-Agent": user_agent
        }, json={"streamMode":"none","chatId":self.chat_id,"folder":"","username":self.username,"id":self.dopple_id,"userQuery":new_message}, cookies={
            "accessToken" : self.token
        })
        req_response = json.loads(req.text)
        return req_response["response"]
    
    def delete_last_user_message(self) -> None:
        req = requests.post(ml_url + "/delete_last_user_message", headers={
            "Accept": "application/json",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.token),
            "Content-Type": "application/json",
            "User-Agent": user_agent
        }, json={"folder": "", "username":self.username,"dopple_id":self.dopple_id, "chat_id":self.chat_id})
    
    def delete_chat(self) -> None:
        req = requests.post(ml_url + "/delete_chat", headers={
            "Accept": "application/json",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "Authorization": "Bearer {0}".format(self.token),
            "Content-Type": "application/json",
            "User-Agent": user_agent
        }, json={"folder": "", "username":self.username,"dopple_id":self.dopple_id, "chat_id":self.chat_id})
