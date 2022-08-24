from fix_API_testing.book_store.models.baseObj import baseObj
from fix_API_testing.book_store.models.collectionOfIsbn import CollectionOfIsbn


class AddListBooks(baseObj):
    def __init__(self, userId: str, collectionOfIsbns: list):
        self._collectionOfIsbns = None
        if userId is not None:
            if not isinstance(userId, str):
                raise TypeError("user id must be string")
            self._userId = userId

        if collectionOfIsbns is not None:
            if not isinstance(collectionOfIsbns, list):
                raise TypeError("collectionOfIsbns must be list")
            for isnb in collectionOfIsbns:
                if not isinstance(isnb, CollectionOfIsbn):
                    raise TypeError("one or more values inside collectionOfIsbns is not instance of CollectionOfIsbn!")
            self._collectionOfIsbns = collectionOfIsbns



