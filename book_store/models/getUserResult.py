from fix_API_testing.book_store.models.baseObj import baseObj
from fix_API_testing.book_store.models.book import Book


class GetUserResult(baseObj):
    def __init__(self, userId: str, username: str, books: [Book]):
        if not isinstance(userId, str):
            raise TypeError("userId must be a string!")
        self._userId = userId
        if not isinstance(username, str):
            raise TypeError("username must be a string!")
        self._username = username
        if not isinstance(books, list):
            raise TypeError("books must be a list!")
        self._books = books

    @property
    def userId(self) -> str:
        return self._userId

    @property
    def username(self) -> str:
        return self._username

    @property
    def books(self) -> [str]:
        return self._books
