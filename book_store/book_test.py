import pytest
from loginView import LoginView
from registerView import RegisterView
from addListOfBooks import AddListBooks
from book import Book
from stringObject import StringObject
from replaceIsbn import ReplaceIsbn
from collectionOfIsbn import CollectionOfIsbn
import book_api
import datetime
import logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
mylogger = logging.getLogger()


@pytest.fixture()
def My_Details() -> RegisterView:
    register_view = RegisterView("omermazor12345", "Omer123!")
    return register_view


@pytest.fixture()
def My_User() -> LoginView:
    login_view = LoginView("omermazor12345", "Omer123!")
    return login_view


@pytest.fixture()
def My_Id() -> str:
    return open("id.txt", "r").read()


@pytest.fixture()
def My_Token() -> str:
    return open("token.txt", "r").read()


@pytest.fixture()
def Urls() -> dict:
    """
    :return: dict of all the useful urls keys:
    accountApi = https://bookstore.toolsqa.com,
    bookStoreApi = https://bookstore.toolsqa.com
    bookStoreApiToken = https://bookstore.toolsqa.com with Bearer token
    accountApiToken = https://bookstore.toolsqa.com with Bearer token
    """
    userID = open("id.txt", "r")
    token = open("token.txt", "r")
    userIDR = userID.read()
    tokenR = token.read()
    accountApi = book_api.AccountApi("https://bookstore.toolsqa.com")
    bookStoreApi = book_api.BookStoreApi("https://bookstore.toolsqa.com")
    bookStoreApiToken = book_api.BookStoreApi("https://bookstore.toolsqa.com", tokenR)
    accountApiToken = book_api.AccountApi("https://bookstore.toolsqa.com", tokenR)
    return {
          "accountApi": accountApi,
          "bookStoreApi": bookStoreApi,
          "accountApiToken": accountApiToken,
          "bookStoreApiToken": bookStoreApiToken
          }


@pytest.fixture()
def My_Book() -> Book:
    book = Book("0-7475-3269-9", "Harry Potter", "Harry Potter and the Philosopher's Stone",
                "J. K. Rowling", datetime.datetime(1997, 6, 26),	"Bloomsbury", 223, "Fantasy",
                "https://www.wizardingworld.com/")
    return book


@pytest.fixture()
def My_Data(My_Id) -> tuple:
    """
    create a data for add books by AddListOfBooks (first return value),
    delete book by StringObject (second return value),
    replace isbn of book with new by ReplaceIsbn (third return value)
    :param My_Id:
    :return: tuple(add_list_of_books, string_object, replace_isbn)
    """
    bookStoreApi = book_api.BookStoreApi("https://bookstore.toolsqa.com")
    res_get = bookStoreApi.get_all_store_books()
    userId = My_Id
    collectionOfIsbns = [CollectionOfIsbn(res_get.json()["books"][0]["isbn"])]
    add_list_of_books = AddListBooks(userId, collectionOfIsbns)
    string_object = StringObject(collectionOfIsbns[0].isbn, My_Id)
    replace_isbn = ReplaceIsbn(userId, res_get.json()["books"][1]["isbn"])
    return add_list_of_books, string_object, replace_isbn


def test_post_user(My_Details, My_User, Urls):
    mylogger.info("test for create new user")
    res_post_user = Urls["accountApi"].post_user(My_Details)
    assert res_post_user.status_code == 201
    assert res_post_user.json()["username"] == My_Details.userName
    mylogger.info(f"Success!!! {res_post_user.json()}")
    userID = open("id.txt", "w")
    token = open("token.txt", "w")
    userID.seek(0)
    token.seek(0)
    userID.write(res_post_user.json()["userID"])
    res_post_token = Urls["accountApi"].post_generate_token(My_User)
    token.write(res_post_token.json()["token"])


def test_post_authorized(My_User, Urls):
    mylogger.info("test for user authorization")
    res_post = Urls["accountApiToken"].post_authorized(My_User)
    assert res_post.status_code == 200
    mylogger.info(f"Success!!! {res_post.json()}")
    assert res_post.json() is True


def test_post_generate_token(My_User, Urls):
    mylogger.info("test for generate new token")
    res_post = Urls["accountApi"].post_generate_token(My_User)
    assert res_post.status_code == 200
    mylogger.info(f"Success!!! {res_post.json()['token']}")
    token = open("token.txt", "w")
    token.seek(0)
    token.write(res_post.json()["token"])


def test_get_user_by_id(My_Id, Urls):
    mylogger.info("test for get user by id")
    res_get = Urls["accountApiToken"].get_user_by_id(My_Id)
    assert res_get.status_code == 200
    mylogger.info(f"Success! {res_get.json()['userId']}")


@pytest.mark.skip(reason="this test will delete the user and will damage the process")
def test_delete_user_by_id(Urls, My_Id):
    mylogger.info("test for delete user by id")
    res_delete = Urls["accountApiToken"].delete_user_by_id(My_Id)
    assert res_delete.status_code == 204
    mylogger.info(f"Deleted Success!")
    res_get = Urls["accountApiToken"].get_user_by_id(My_Id)
    assert res_get.status_code == 401


def test_get_all_store_books(Urls):
    mylogger.info("test for get all books in the store")
    res_get = Urls["bookStoreApi"].get_all_store_books()
    assert res_get.status_code == 200
    mylogger.info(f"Success! {res_get.json()}")


def test_post_books(My_Data, Urls, My_Id):
    mylogger.info("test for create list of books")
    mylogger.error("this test getting error 504-Gateway Time-Out everytime!!!")
    res_delete = Urls["bookStoreApiToken"].delete_books_by_userid(My_Id)
    assert res_delete.status_code == 204
    res_post = Urls["bookStoreApiToken"].post_books(My_Data[0])
    assert res_post.status_code == 504
    mylogger.error("504 Gateway Time-out")
    assert res_post.status_code == 201
    mylogger.info(f"Success! {res_post.json()}")


def test_delete_books_by_string_object(Urls, My_Id, My_Data):
    mylogger.info("test for delete books by string object (isbn, userid)")
    mylogger.error("this test getting error!!!")
    res_get = Urls["accountApiToken"].get_user_by_id(My_Id)
    assert res_get.status_code == 200
    res_post = Urls["bookStoreApiToken"].post_books(My_Data[0])  # Post Request Don't Work!!!
    assert res_post.status_code == 201  # Post Request Don't Work!!!
    res_delete = Urls["bookStoreApiToken"].delete_books_by_string_object(My_Data[1])
    res_get2 = Urls["accountApiToken"].get_user_by_id(My_Id)
    assert res_delete.status_code == 204
    mylogger.info("book deleted successfully!")
    books_before = res_get.json()["books"]  # Post Request Don't Work!!!
    books_after = res_get2.json()["books"]  # Post Request Don't Work!!!
    assert len(books_after) < len(books_before)  # Post Request Don't Work!!!


def test_delete_books_by_userid(Urls, My_Id, My_Data):
    mylogger.info("test for delete books by user id")
    mylogger.error("this test getting error!!!")
    res_get = Urls["accountApiToken"].get_user_by_id(My_Id)
    assert res_get.status_code == 200
    res_post = Urls["bookStoreApiToken"].post_books(My_Data[0])  # Request Not Work!!!
    assert res_post.status_code == 201  # Request Not Work!!!
    res_delete = Urls["bookStoreApiToken"].delete_books_by_userid(My_Id)
    assert res_delete.status_code == 204
    mylogger.info("Deleted Success!")
    res_get2 = Urls["accountApiToken"].get_user_by_id(My_Id)
    books_before = res_get.json()["books"]  # Post Request Don't Work!!!
    books_after = res_get2.json()["books"]   # Post Request Don't Work!!!
    assert len(books_after) < len(books_before)   # Post Request Don't Work!!!


def test_get_by_isbn(Urls):
    mylogger.info("test for get books by isbn")
    mylogger.error("this test getting error!!!")
    res_get = Urls["bookStoreApi"].get_all_store_books()
    assert res_get.status_code == 200
    assert res_get.json()["books"][0]["isbn"]
    res_get2 = Urls["bookStoreApi"].get_by_isbn(res_get.json()["books"][0]["isbn"])
    assert res_get2.status_code == 200
    assert res_get2.json()["isbn"] == res_get.json()["books"][0]["isbn"]
    mylogger.info(f"isbn that received is {res_get.json()['books'][0]['isbn']} "
                  f" \n and returned isbn is {res_get2.json()['isbn']}")


def test_put_isbn(Urls, My_Id, My_Data):
    mylogger.info("test for change isbn of user's book list")
    res_post = Urls["bookStoreApiToken"].post_books(My_Data[0])  # POST REQUEST DON'T WORK!!!
    assert res_post.status_code == 201  # POST REQUEST DON'T WORK!!!
    res_get = Urls["accountApiToken"].get_user_by_id(My_Id)
    assert res_get.status_code == 200
    books = res_get.json()["books"]
    res_put = Urls["bookStoreApi"].put_isbn(books[0]["isbn"], My_Data[2])
    assert res_put.status_code == 200  # CRASH: PROBLEM WITH THE REQUEST!!!
    assert res_put.json()["books"][0]["isbn"] == My_Data[2].isbn  # CRASH: PROBLEM WITH THE REQUEST!!!
    mylogger.info(f"Success! {res_put.json()}['books'][0]['isbn']")
