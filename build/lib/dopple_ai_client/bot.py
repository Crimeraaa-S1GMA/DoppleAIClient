class DoppleBot:
    def __init__(self, dopple_id, display_name, tagline, **metadata) -> None:
        self.dopple_id = dopple_id
        self.display_name = display_name
        self.tagline = tagline

        self.bio = metadata["bio"]
        self.greeting = metadata["greeting"]
        self.avatar_url = metadata["avatar_url"]
        self.banner_url = metadata["banner_url"]
        self.banner_video_url = metadata["banner_video_url"]
        self.message_count = metadata["message_count"]
        self.creator_username = metadata["creator_username"]
        self.category = metadata["category"]
        self.subcategory = metadata["subcategory"]
        self.internal = metadata["internal"]
