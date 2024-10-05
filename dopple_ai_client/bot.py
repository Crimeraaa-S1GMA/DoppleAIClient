class DoppleBot:
    def __init__(self, data : dict = {}) -> None:
        self.dopple_id : str = data["id"] if "id" in data else ""
        self.display_name : str = data["display_name"] if "display_name" in data else ""
        self.tagline : str = data["tagline"] if "tagline" in data else ""
        self.bio : str = data["bio"] if "bio" in data else ""
        self.description : str = data["description"] if "bio" in data else ""
        self.greeting : str = data["greeting"] if "bio" in data else ""
        self.avatar_url : str = data["avatar_url"] if "avatar_url" in data else ""
        self.banner_url : str = data["banner_url"] if "banner_url" in data else ""
        self.banner_video_url : str = data["banner_video_url"] if "banner_video_url" in data else ""
        self.message_count : int = data["message_count"] if "message_count" in data else 0
        self.creator_username : str = data["creator_username"] if "creator_username" in data else ""
        self.category : int = data["category"] if "category" in data else 0
        self.subcategory : int = data["subcategory"] if "subcategory" in data else 0
        self.internal : bool = data["internal"] if "internal" in data else False
        self.supports_reactions : bool = data["has_emotion_images"] if "has_emotion_images" in data else False
        self.example_conversations : list[dict] = data["shots"] if "shots" in data else []
    
    def __str__(self) -> str:
        return f"{self.display_name} (ID:{self.dopple_id})"
