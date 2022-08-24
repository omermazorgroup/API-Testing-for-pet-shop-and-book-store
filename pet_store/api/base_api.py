import requests


class BaseApi:
    def __init__(self, url: str):
        self._url = url
        self._headers = {"accept": "application/json"}
        self._session = requests.session()
        self._session.headers.update(self._headers)
