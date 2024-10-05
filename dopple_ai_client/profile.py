from .bot import DoppleBot

class DoppleProfile:
    def __init__(self, profile_id : str, username : str, subs : int, dopple_count : int, total_messages : int, bots : list[dict] = {}) -> None:
        self.profile_id : str = profile_id
        self.username : str = username
        self.subs : int = subs
        self.dopple_count : int = dopple_count
        self.total_messages : int = total_messages

        self.bots : list[DoppleBot] = []

        for bot in bots:
            self.bots.append(DoppleBot(bot))
    
    def __str__(self) -> str:
        return f"{self.username} (ID:{self.profile_id}, {self.dopple_count} dopples, {self.subs} subscribers and {self.total_messages} messages)"
