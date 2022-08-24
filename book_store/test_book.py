import pytest
import requests
from fix_API_testing.book_store.models.loginView import LoginView
from fix_API_testing.book_store.models.registerView import RegisterView
from fix_API_testing.book_store.models.addListOfBooks import AddListBooks
from fix_API_testing.book_store.models.book import Book
from fix_API_testing.book_store.models.stringObject import StringObject
from fix_API_testing.book_store.models.replaceIsbn import ReplaceIsbn
from fix_API_testing.book_store.models.collectionOfIsbn import CollectionOfIsbn
from fix_API_testing.book_store.models.getUserResult import GetUserResult
from fix_API_testing.book_store.api.book_api import BookStoreApi
from fix_API_testing.book_store.api.account_api import AccountApi
import logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
mylogger = logging.getLogger()


@pytest.fixture()
def Register_Details() -> RegisterView:
    register_view = RegisterView("omermazor123456", "Omer123!")
    return register_view


@pytest.fixture(scope="session")
def User() -> LoginView:
    login_view = LoginView("omermazor123456", "Omer123!")
    return login_view


@pytest.fixture()
def My_Id() -> str:
    return open("id.txt", "r").read()


@pytest.fixture(scope="session")
def url(pytestconfig) -> str:
    """
    give the url from pytest options
    :param pytestconfig: pytestconfig fixture
    :return: url to integrate
    """
    return pytestconfig.getoption("url")


@pytest.fixture(scope="module")
def bearer_auth_session(url, User) -> [dict, GetUserResult]:
    """
    fixture to make authorize by the save acc data in
    constant,py file ,and after it verify by post request
    if the authorized complete success
    :param url: url to work with
    :return: header after adding bearer token
    """
    res = requests.post(f'{url}/Account/v1/GenerateToken', data=User.to_json())
    my_token = res.json()["token"]
    return my_token


@pytest.fixture(scope="module")
def account_api(url, bearer_auth_session):
    """
    A function that return the api with url and Bearer token for account requests
    :param url: The base url for sending the requests
    :param bearer_auth_session: Bearer token that send to the header
    :return: AccountApi Model
    """
    return AccountApi(url, bearer_auth_session)


@pytest.fixture(scope="module")
def book_store_api(url, bearer_auth_session):
    """
    A function that return the api with url and Bearer token for book-store requests
    :param url: The base url for sending the requests
    :param bearer_auth_session: Bearer token that send to the header
    :return: BookStore Model
    """
    return BookStoreApi(url, bearer_auth_session)


@pytest.fixture()
def My_Data(My_Id, book_store_api) -> tuple:
    """
    create a data for add books by AddListOfBooks (first return value),
    delete book by StringObject (second return value),
    replace isbn of book with new by ReplaceIsbn (third return value)
    :param My_Id:
    :return: tuple(add_list_of_books, string_object, replace_isbn)
    """
    bookStoreApi = book_store_api
    res_get = bookStoreApi.get_all_store_books()
    userId = My_Id
    collectionOfIsbns = [CollectionOfIsbn(res_get.json()["books"][0]["isbn"])]
    add_list_of_books = AddListBooks(userId, collectionOfIsbns)
    string_object = StringObject(collectionOfIsbns[0].isbn, My_Id)
    replace_isbn = ReplaceIsbn(userId, res_get.json()["books"][1]["isbn"])
    return add_list_of_books, string_object, replace_isbn


def test_post_user(account_api, Register_Details):
    mylogger.info("test for create new user")
    res_post_user = account_api.post_user(Register_Details)
    print(res_post_user.url)
    assert res_post_user.status_code == 201
    user = GetUserResult(**res_post_user.json())
    userID = open("id.txt", "w")
    userID.seek(0)
    userID.write(res_post_user.json()["userID"])
    assert res_post_user.json()["username"] == Register_Details.userName
    mylogger.info(f"Success!!! {res_post_user.json()}")


def test_post_authorized(account_api, User):
    mylogger.info("test for user authorization")
    res_post = account_api.post_authorized(User)
    assert res_post.status_code == 200
    mylogger.info(f"Success!!! {res_post.json()}")
    assert res_post.json() is True


def test_post_generate_token(account_api, User):
    mylogger.info("test for generate new token")
    res_post = account_api.post_generate_token(User)
    assert res_post.status_code == 200
    mylogger.info(f"Success!!! {res_post.json()['token']}")


def test_get_user_by_id(account_api, My_Id):
    mylogger.info("test for get user by id")
    res_get = account_api.get_user_by_id(My_Id)
    assert res_get.status_code == 200
    user = GetUserResult(**res_get.json())
    mylogger.info(f"Success! {user.userId}")


@pytest.mark.skip(reason="this test will delete the user and will damage the process")
def test_delete_user_by_id(account_api, My_Id):
    mylogger.info("test for delete user by id")
    res_delete = account_api.delete_user_by_id(My_Id)
    assert res_delete.status_code == 204
    mylogger.info(f"Deleted Success!")
    res_get = account_api.get_user_by_id(My_Id)
    assert res_get.status_code == 401


def test_get_all_store_books(book_store_api):
    mylogger.info("test for get all books in the store")
    res_get = book_store_api.get_all_store_books()
    assert res_get.status_code == 200
    books = list(res_get.json()['books'])
    for book in books:
        Book(**book)
    mylogger.info(f"Success! {books}")


def test_post_books(book_store_api, My_Data, My_Id):
    mylogger.info("test for create list of books")
    mylogger.error("this test getting error 504-Gateway Time-Out everytime!!!")
    res_delete = book_store_api.delete_books_by_userid(My_Id)
    assert res_delete.status_code == 204
    res_post = book_store_api.post_books(My_Data[0])
    assert res_post.status_code == 504
    mylogger.error("504 Gateway Time-out")
    assert res_post.status_code == 201
    collection_of_isbn = CollectionOfIsbn(**res_post.json())
    mylogger.info(f"Success! {collection_of_isbn}")


def test_delete_books_by_string_object(book_store_api, account_api, My_Id, My_Data):
    mylogger.info("test for delete books by string object (isbn, userid)")
    mylogger.error("this test getting error!!!")
    res_get = account_api.get_user_by_id(My_Id)
    assert res_get.status_code == 200
    res_post = book_store_api.post_books(My_Data[0])  # Post Request Don't Work!!!
    assert res_post.status_code == 201  # Post Request Don't Work!!!
    res_delete = book_store_api.delete_books_by_string_object(My_Data[1])
    res_get2 = account_api.get_user_by_id(My_Id)
    assert res_delete.status_code == 204
    mylogger.info("book deleted successfully!")
    books_before = res_get.json()["books"]  # Post Request Don't Work!!!
    books_after = res_get2.json()["books"]  # Post Request Don't Work!!!
    assert len(books_after) < len(books_before)  # Post Request Don't Work!!!


def test_delete_books_by_userid(book_store_api, account_api,  My_Id, My_Data):
    mylogger.info("test for delete books by user id")
    mylogger.error("this test getting error!!!")
    res_get = account_api.get_user_by_id(My_Id)
    assert res_get.status_code == 200
    res_post = book_store_api.post_books(My_Data[0])  # Request Not Work!!!
    assert res_post.status_code == 201  # Request Not Work!!!
    res_delete = book_store_api.delete_books_by_userid(My_Id)
    assert res_delete.status_code == 204
    mylogger.info("Deleted Success!")
    res_get2 = account_api.get_user_by_id(My_Id)
    books_before = res_get.json()["books"]  # Post Request Don't Work!!!
    books_after = res_get2.json()["books"]   # Post Request Don't Work!!!
    assert len(books_after) < len(books_before)   # Post Request Don't Work!!!


def test_get_by_isbn(book_store_api):
    mylogger.info("test for get books by isbn")
    res_get = book_store_api.get_all_store_books()
    assert res_get.status_code == 200
    assert res_get.json()["books"][0]["isbn"]
    res_get2 = book_store_api.get_by_isbn(res_get.json()["books"][0]["isbn"])
    assert res_get2.status_code == 200
    book = Book(**res_get2.json())
    assert book.isbn == res_get.json()["books"][0]["isbn"]
    mylogger.info(f"isbn that received is {res_get.json()['books'][0]['isbn']} "
                  f" \n and returned isbn is {res_get2.json()['isbn']}")


def test_put_isbn(book_store_api, account_api, My_Id, My_Data):
    mylogger.info("test for change isbn of user's book list")
    mylogger.error("this test getting error!!!")
    res_post = book_store_api.post_books(My_Data[0])  # POST REQUEST DON'T WORK!!!
    assert res_post.status_code == 201  # POST REQUEST DON'T WORK!!!
    res_get = book_store_api.get_user_by_id(My_Id)
    assert res_get.status_code == 200
    books = res_get.json()["books"]
    res_put = book_store_api.put_isbn(books[0]["isbn"], My_Data[2])
    assert res_put.status_code == 200  # CRASH: PROBLEM WITH THE REQUEST!!!
    assert res_put.json()["books"][0]["isbn"] == My_Data[2].isbn  # CRASH: PROBLEM WITH THE REQUEST!!!
    mylogger.info(f"Success! {res_put.json()}['books'][0]['isbn']")
