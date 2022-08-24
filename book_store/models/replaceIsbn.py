from fix_API_testing.book_store.models.baseObj import baseObj


class ReplaceIsbn(baseObj):
    def __init__(self, userId: str, isbn: str):
        self._userId = None
        self._isbn = None

        if userId is not None:
            if not isinstance(userId, str):
                raise TypeError("user id must be string")
            self._userId = userId

        if isbn is not None:
            if not isinstance(isbn, str):
                raise TypeError("isbn must be string")
            self._isbn = isbn

    @property
    def isbn(self):
        """Gets the isbn of this Model.  # noqa: E501
        :return: The isbn of this Model.  # noqa: E501
        :rtype: str
        """
        return self._isbn
