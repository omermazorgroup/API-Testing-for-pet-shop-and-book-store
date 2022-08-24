import requests


class BaseApi:
    def __init__(self, url: str, token: str):
        self._base_url = url
        self.session = requests.session()
        self._token = token
        self._headers = {
            'accept': 'application/json',
            'authorization': 'Basic b21lcm1hem9yMTI6T21lcjEyMyE==true',
            'Authorization': f'Bearer {self._token}'
        }
        self.session.headers.update(self._headers)

