import requests
from fix_API_testing.book_store.api.base_api import BaseApi


class BookStoreApi(BaseApi):
    def __init__(self, url: str, token: str):
        super().__init__(url, token)
        self._url = self._base_url

    def get_all_store_books(self):
        res = self.session.get(url=f"{self._url}/BookStore/v1/Books")
        return res

    def post_books(self, list_of_books):
        list_of_books_data = list_of_books.to_json()
        res = self.session.post(url=f"{self._url}/BookStore/v1/Books", data=list_of_books_data)
        return res

    def delete_books_by_userid(self, user_id: str):
        res = self.session.delete(url=f"{self._url}/BookStore/v1/Books?UserId={user_id}")
        return res

    def get_by_isbn(self, isbn: str):
        res = self.session.get(url=f"{self._url}/BookStore/v1/Book?ISBN={isbn}")
        return res

    def delete_books_by_string_object(self, string_object):
        string_object_data = string_object.to_json()
        res = self.session.delete(url=f"{self._url}/BookStore/v1/Book", data=string_object_data)
        return res

    def put_isbn(self, new_isbn: str, replace_isbn):
        replace_isbn_data = replace_isbn.to_json()
        res = self.session.put(url=f"{self._url}/BookStore/v1/Books/{new_isbn}", data=replace_isbn_data)
        return res



