from baseObj import baseObj


class StringObject(baseObj):
    def __init__(self, isbn:str, userId:str):
        self._isbn = None
        self._userId = None

        if isbn is not None:
            if not isinstance(isbn, str):
                raise TypeError("isbn must be string")
            self._isbn = isbn

        if userId is not None:
            if not isinstance(userId, str):
                raise TypeError(" userId must be string")
            self._userId = userId


