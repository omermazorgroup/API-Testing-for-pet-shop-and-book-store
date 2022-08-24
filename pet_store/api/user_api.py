from fix_API_testing.pet_store.api.base_api import BaseApi


class UserApi(BaseApi):
    def __init__(self, url: str):
        super().__init__(url)
        self._url = f'{url}/user'

    def post_user(self, user):
        user_data = user.to_json()
        res = self._session.post(url=f"{self._url}", data=user_data)
        return res

    def post_users_list(self, users):
        res = self._session.post(url=f"{self._url}/createWithList", data=users)
        return res

    def get_login(self, user_name, password):
        res = self._session.get(url=f"{self._url}/login?username={user_name}&password={password}")
        return res

    def get_logout(self):
        res = self._session.get(url=f"{self._url}/logout")
        return res

    def get_username(self, user_name: str):
        res = self._session.get(url=f"{self._url}/{user_name}")
        return res

    def put_username(self, first_user_name, user):
        user_data = user.to_json()
        res = self._session.put(url=f"{self._url}/{first_user_name}", data=user_data)
        return res

    def delete_username(self, user_name: str):
        res = self._session.delete(url=f"{self._url}/{user_name}")
        return res
