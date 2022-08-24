import requests
from fix_API_testing.book_store.api.base_api import BaseApi


class AccountApi(BaseApi):
    def __init__(self, url: str, token: str):
        super().__init__(url, token)
        self._url = self._base_url

    def post_authorized(self, login_view_model):
        login_view_model_data = login_view_model.to_json()
        res = self.session.post(url=f"{self._url}/Account/v1/Authorized", data=login_view_model_data)
        return res

    def post_generate_token(self, login_view_model):
        login_view_model_data = login_view_model.to_json()
        res = self.session.post(url=f"{self._url}/Account/v1/GenerateToken", data=login_view_model_data)
        return res

    def post_user(self, register_view_model):
        register_view_model_data = register_view_model.to_json()
        res = self.session.post(url=f"{self._url}/Account/v1/User", data=register_view_model_data)
        return res

    def delete_user_by_id(self, user_id: str):
        res = self.session.delete(url=f"{self._url}/Account/v1/User/{user_id}")
        return res

    def get_user_by_id(self, user_id: str):
        res = self.session.get(url=f"{self._url}/Account/v1/User/{user_id}")
        return res
