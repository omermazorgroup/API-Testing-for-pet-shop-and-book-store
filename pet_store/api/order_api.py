from fix_API_testing.pet_store.api.base_api import BaseApi
from fix_API_testing.pet_store.models.pet import Pet


class OrderApi(BaseApi):
    def __init__(self, url: str):
        super().__init__(url)
        self._url = f'{self._url}/store'

    def get_store_inventory(self):
        res = self._session.get(url=f"{self._url}/inventory")
        return res

    def post_order(self, order):
        order_data = order.to_json()
        res = self._session.post(url=f"{self._url}/order", data=order_data)
        return res

    def get_order(self, id: int) -> [Pet]:
        res = self._session.get(url=f"{self._url}/order/{id}")
        return res

    def delete_order(self, id: int) -> [Pet]:
        res = self._session.delete(url=f"{self._url}/order/{id}")
        return res
