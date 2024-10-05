class DoppleRequestError(Exception):
    def __init__(self, code : int) -> None:
        self.code : int = code
    
    def __str__(self) -> str:
        return(repr(self.code))
