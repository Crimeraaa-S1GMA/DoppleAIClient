class DoppleMessage:
    def __init__(self, content : str, type : str) -> None:
        self.content : str = content
        self.type : str = type
        self.timestamp : float = 0.0
        self.edited : bool = False
        self.nsfw : bool = False
        self.emotion_image_url : str = ""
        self.example : bool = False
        self.rerolled_responses : list[str] = []
    
    def from_msg(self, msg : dict):
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
    
    def __str__(self) -> str:
        return f"{self.content}"
