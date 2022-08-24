from fix_API_testing.book_store.models.baseObj import baseObj


class CollectionOfIsbn(baseObj):
    def __init__(self, isbn: str):
        self._isbn = None

        if isbn is not None:
            if not isinstance(isbn, str):
                raise TypeError("isbn must be string")
            self._isbn = isbn

    @property
    def isbn(self) -> str:
        """Gets the isbn of this Model.  # noqa: E501
        :return: The isbn of this Model.  # noqa: E501
        :rtype: str
        """
        return self._isbn

    def __str__(self):
        return str(self.isbn)
