from .api_urls import *
from .response import DoppleResponse
from .message import DoppleMessage
from .dopple_request_error import DoppleRequestError

import requests
import json

class DoppleChat:
    def __init__(self, chat_id, dopple_id, email, request_helper) -> None:
        self.chat_id = chat_id
        self.dopple_id = dopple_id
        self.email = email

        self.request_helper = request_helper
    
    def get_chat_history(self, limit = 50, skip = 0) -> list:
        req = self.request_helper.post(ml_url + "/get_paginated_chat_history", {"folder": "", "username":self.email,"dopple_id":self.dopple_id, "chat_id":self.chat_id,"limit":limit,"skip":skip})

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
        req = self.request_helper.post(ml_url + "/clear_chat_history", {"folder": "", "username":self.email,"dopple_id":self.dopple_id, "chat_id":self.chat_id})
    
    def send_message(self, message, reroll = False) -> DoppleResponse:
        req = self.request_helper.post_nobearer(api_url + "/messages/send" + ("?action=reroll" if reroll else ""), {"streamMode":"none","chatId":self.chat_id,"folder":"","username":self.email,"id":self.dopple_id,"userQuery":message})
        
        req_response = json.loads(req.text)
        return DoppleResponse(message=req_response["response"], timestamp=req_response["timestamp"])

    def edit_last_user_message(self, new_message) -> str:
        req = self.request_helper.post_nobearer(api_url + "/messages/send?action=edit", {"streamMode":"none","chatId":self.chat_id,"folder":"","username":self.email,"id":self.dopple_id,"userQuery":new_message})
        
        req_response = json.loads(req.text)
        return req_response["response"]

    def edit_last_bot_message(self, new_message) -> None:
        req = self.request_helper.post(ml_url + "/edit_last_ai_response", {"chat_id":self.chat_id,"folder":"","username":self.email,"dopple_id":self.dopple_id,"new_ai_response":new_message})
    
    def delete_last_user_message(self) -> None:
        req = self.request_helper.post(ml_url + "/delete_last_user_message", {"folder": "", "username":self.email,"dopple_id":self.dopple_id, "chat_id":self.chat_id})
    
    def delete_last_ai_response(self) -> None:
        req = self.request_helper.post(ml_url + "/delete_last_ai_response", {"folder": "", "username":self.email,"dopple_id":self.dopple_id, "chat_id":self.chat_id})
    
    def delete_chat(self) -> None:
        req = self.request_helper.post(ml_url + "/delete_chat", {"folder": "", "username":self.email,"dopple_id":self.dopple_id, "chat_id":self.chat_id})
