class DoppleMessage:
    def __init__(self, content, type, timestamp, nsfw, emotion_image_url, example) -> None:
        self.content = content
        self.type = type
        self.timestamp = timestamp
        self.nsfw = nsfw
        self.emotion_image_url = emotion_image_url
        self.example = example
