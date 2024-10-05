class DoppleResponse:
    def __init__(self, message : str, timestamp : float, model : str, reaction_image_url : str = "") -> None:
        self.message : str = message
        self.timestamp : float = timestamp
        self.model : str = model
        self.reaction_image_url : str = reaction_image_url
