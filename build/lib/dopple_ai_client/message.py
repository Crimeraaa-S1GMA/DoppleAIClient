class DoppleMessage:
    def __init__(self, content, type) -> None:
        self.content = content
        self.type = type
        self.timestamp = 0.0
        self.edited = False
        self.nsfw = False
        self.emotion_image_url = ""
        self.example = False
        self.rerolled_responses = []
    
    def from_msg(self, msg):
        self.content = msg["message"]["data"]["content"]
        self.type = msg["message"]["type"]
        self.timestamp = msg["timestamp"]
        if "edited" in msg["message"]["data"]:
            self.edited = msg["message"]["data"]["edited"]
        self.nsfw = msg["message"]["data"]["additional_kwargs"]["nsfw"]
        self.emotion_image_url = msg["message"]["data"]["additional_kwargs"]["dopple_emotion_image_url"]
        self.example = msg["message"]["data"]["example"]

        if "rerolled_responses" in msg["message"]["data"]:
            for response in msg["message"]["data"]["rerolled_responses"]:
                self.rerolled_responses.append(response)
