# coding: utf-8
from fix_API_testing.book_store.models.baseObj import baseObj


class LoginView(baseObj):

    def __init__(self, userName: str, password: str):
        if not isinstance(userName, str):
            raise TypeError("user name must be string")
        self._userName = userName
        if not isinstance(password, str):
            raise TypeError("password must be string")
        self._password = password

