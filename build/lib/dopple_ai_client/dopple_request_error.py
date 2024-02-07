class DoppleRequestError(Exception):
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return(repr(self.value))
