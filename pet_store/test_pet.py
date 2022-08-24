import pytest
import logging
from fix_API_testing.pet_store.models.pet import Pet
from fix_API_testing.pet_store.models.category import Category
from fix_API_testing.pet_store.models.tags import Tags
from fix_API_testing.pet_store.models.order import Order
from fix_API_testing.pet_store.models.user import User
from fix_API_testing.pet_store.api.pet_api import PetApi
from fix_API_testing.pet_store.api.order_api import OrderApi
from fix_API_testing.pet_store.api.user_api import UserApi
import datetime
import json
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
mylogger = logging.getLogger()


@pytest.fixture(scope="session")
def url(pytestconfig) -> str:
    """
    give the url from pytest options
    :param pytestconfig: pytestconfig fixture
    :return: url to integrate
    """
    return pytestconfig.getoption("url")


@pytest.fixture(scope="module")
def pet_api(url):
    """
    A function that return the api with url for pet requests
    :param url: The base url for sending the requests
    :return: PetApi Model
    """
    return PetApi(url)


@pytest.fixture(scope="module")
def order_api(url):
    """
    A function that return the api with url for order requests
    :param url: The base url for sending the requests
    :return: OrderApi Model
    """
    return OrderApi(url)


@pytest.fixture(scope="module")
def user_api(url):
    """
    A function that return the api with url for user requests
    :param url: The base url for sending the requests
    :return: UserApi Model
    """
    return UserApi(url)


@pytest.fixture()
def My_Pet() -> Pet:
    category = Category(146, "Dogs")
    photoUrls = ["https://en.wikipedia.org/wiki/Dog#/media/File:Dog_-_%E0%B4%A8%E0%B4%BE%E0%B4%AF-6.JPG"]
    tags = [Tags(3453445, "tag1")]
    shoko = Pet(20, "shoko", category, photoUrls, tags, "available")
    return shoko


@pytest.fixture()
def My_Order() -> Order:
    my_order = Order(3242, "23542", 1, datetime.datetime.now(), "placed", False)
    return my_order


@pytest.fixture()
def My_User() -> User:
    my_user = User("12232", "omermazor", "4r5345c", "omer", "mazor", "omermazor144@gmail.com", 207976903, 5)
    return my_user


@pytest.fixture()
def My_Users() -> [User]:
    my_user1 = User(12232, "itamar", "4r5345c", "itamar", "mazor", "itamar@gmail.com", 234314532, 5)
    my_user2 = User(32454, "shlomo", "4r5345c", "shlomo", "mazor", "shlomo@gmail.com", 545435243, 5)
    my_user3 = User(35732, "topaz", "4r5345c", "topaz", "ifergan", "topaz@gmail.com", 532454325, 5)
    users = [my_user1, my_user2, my_user3]
    return users


def test_put_pet(My_Pet, pet_api):
    mylogger.info("test for update a pet")
    re =pet_api.post_new_pet(My_Pet)
    My_Pet.name = "Omer"
    res_put = pet_api.put_pet(My_Pet)
    res_get = pet_api.get_pet_by_id(My_Pet.id)
    assert res_put.status_code == 200
    pet = Pet(**res_get.json())
    assert My_Pet.name == pet.name
    mylogger.info(f"Success! {res_get.json()['name']}")


def test_post_new_pet(My_Pet, pet_api):
    mylogger.info("test for create a new pet")
    res_delete = pet_api.delete_pet_by_id(My_Pet.id)
    res_post = pet_api.post_new_pet(My_Pet)
    post_pet = Pet(**res_post.json())
    assert res_post.status_code == 200
    res_get = pet_api.get_pet_by_id(My_Pet.id)
    get_pet = Pet(**res_get.json())
    assert res_get.status_code == 200
    assert post_pet == get_pet
    mylogger.info(f"Success! {res_post.json()}")


def test_get_pet_by_id(My_Pet, pet_api):
    mylogger.info("test for get a  pet by id")
    pet_api.post_new_pet(My_Pet)
    res_get = pet_api.get_pet_by_id(My_Pet.id)
    assert res_get.status_code == 200
    pet = Pet(**res_get.json())
    assert pet.id == My_Pet.id
    mylogger.info(f"Success! {res_get.json()['id']}")


def test_get_pets_by_status(My_Pet, pet_api):
    mylogger.info("test for get a  pet by status")
    res_get = pet_api.get_pets_by_status(My_Pet.status)
    assert res_get.status_code == 200
    statusArray = []
    for pet in res_get.json():
        statusArray.append(pet["status"])
    assert My_Pet.status in statusArray
    mylogger.info(f"Success! {My_Pet.status}")


def test_get_pet_by_tags(My_Pet, pet_api):
    mylogger.info("test for get a pets by tags")
    tags = []
    for tag in My_Pet.tags:
        tags.append(tag.name)
    res_get = pet_api.get_pet_by_tags(tags)
    assert res_get.status_code == 200
    tagsNames = []
    for pet in res_get.json():
        for tag in pet["tags"]:
            if isinstance(tag, dict):
                tagsNames.append(tag["name"])
    assert My_Pet.tags[0].name in tagsNames
    mylogger.info(f"Success! {My_Pet.tags[0].name}")


def test_post_pet_by_id_and_update(My_Pet, pet_api):
    mylogger.info("test for update a pet by name and status")
    pet_api.post_new_pet(My_Pet)
    pet_before = Pet(**dict(My_Pet.to_json()))
    My_Pet.name = "dany"
    My_Pet.status = "sold"
    pet_after = Pet(**dict(My_Pet.to_json()))
    res_post = pet_api.post_pet_by_id_and_update(My_Pet.id, My_Pet.name, My_Pet.status)
    assert res_post.status_code == 200
    pet = Pet(**res_post.json())
    assert pet.name != pet_before.name and pet.status != pet_before.status
    assert pet.name == pet_after.name and pet.status == pet_after.status
    mylogger.info(f"Success! {res_post.json()['name'], res_post.json()['status']}")


def test_delete_pet_by_id(My_Pet, pet_api):
    mylogger.info("test for delete a pet by id")
    res_post = pet_api.post_new_pet(My_Pet)
    assert res_post.status_code == 200
    res_delete = pet_api.delete_pet_by_id(My_Pet.id)
    assert res_delete.status_code == 200
    res_get = pet_api.get_pet_by_id(My_Pet.id)
    assert res_get.status_code == 404
    mylogger.info("Deleted Success!")


def test_upload_image_by_id(My_Pet, pet_api):
    mylogger.info("test for upload a image to an pet by a id")
    mylogger.error("this test getting error!!!")
    files = {'upload_file': open('slide-1.jpg', 'rb')}
    res_post = pet_api.upload_image_by_id(My_Pet.id, files)
    mylogger.info(res_post.json())
    assert res_post.status_code == 200
    mylogger.info(f"Success {res_post.json()['message']}")


def test_get_store_inventory(order_api):
    mylogger.info("test for get a store to inventory")
    res_get = order_api.get_store_inventory()
    assert res_get.status_code == 200
    assert type(res_get.json()) == dict
    mylogger.info(f"Success {res_get.json()}")


def test_post_order(My_Order, order_api):
    mylogger.info("test for create a new order")
    order_api.delete_order(My_Order.id)
    res_post = order_api.post_order(My_Order)
    post_order = Order(**res_post.json())
    assert res_post.status_code == 200
    res_get = order_api.get_order(My_Order.id)
    get_order = Order(**res_get.json())
    mylogger.info(res_get.json())
    assert res_get.status_code == 200
    assert get_order == post_order
    mylogger.info(f"Success {res_get.json()}")


def test_get_order(My_Order, order_api):
    mylogger.info("test for get a order")
    order_api.post_order(My_Order)
    res_get = order_api.get_order(My_Order.id)
    assert res_get.status_code == 200
    order = Order(**res_get.json())
    assert order.id == My_Order.id
    mylogger.info(f"Success {order.id}")


def test_delete_order(My_Order, order_api):
    mylogger.info("test for delete a order")
    res_post = order_api.post_order(My_Order)
    assert res_post.status_code == 200
    res_delete = order_api.delete_order(My_Order.id)
    assert res_delete.status_code == 200
    res_get = order_api.get_order(My_Order.id)
    assert res_get.status_code == 404
    mylogger.info("Deleted Success!")


def test_post_user(My_User, user_api):
    mylogger.info("test for create a new user")
    user_api.delete_username(My_User.username)
    res_post = user_api.post_user(My_User)
    post_user = User(**res_post.json())
    assert res_post.status_code == 200
    res_get = user_api.get_username(My_User.username)
    get_user = User(**res_get.json())
    assert res_get.status_code == 200
    assert get_user == post_user
    mylogger.info(f"Success! {res_get.json()}")


def test_post_users(My_Users, user_api):
    mylogger.info("test for create a list of new users")
    mylogger.info("test post users")
    mylogger.error("this test getting error!!!")
    users = [user.to_json() for user in My_Users]
    users_json = json.dumps(users)
    res_post = user_api.post_users_list(users_json)
    assert res_post.status_code == 200


def test_get_login(My_User, user_api):
    mylogger.info("test for get login request")
    res_get = user_api.get_login(My_User.username, My_User.password)
    assert res_get.status_code == 200
    mylogger.info(f"Success!{res_get.content}")


def test_get_logout(user_api):
    mylogger.info("test for get logout request")
    res_get = user_api.get_logout()
    assert res_get.status_code == 200
    mylogger.info(f"Success!{res_get.content}")


def test_get_username(My_User, user_api):
    mylogger.info("test for get user by username")
    res_post = user_api.post_user(My_User)
    assert res_post.status_code == 200
    res_get = user_api.get_username(My_User.username)
    assert res_get.status_code == 200
    user = User(**res_get.json())
    assert user.username == My_User.username
    mylogger.info(f"Success!{user.username}")


def test_put_username(My_User, user_api):
    mylogger.info("test for update a username of user")
    res_post = user_api.post_user(My_User)
    assert res_post.status_code == 200
    first_username = My_User.username
    My_User.username = "omermazor2"
    res_put = user_api.put_username(first_username, My_User)
    assert res_put.status_code == 200  # REQUEST PROBLEM: RETURN 500!!!
    user = User(**res_put.json())
    assert user.username == My_User.username  # REQUEST PROBLEM: RETURN 500!!!
    mylogger.info(f"Success!{res_put.json()['username']}")


def test_delete_username(My_User, user_api):
    mylogger.info("test for delete a user by username")
    res_post = user_api.post_user(My_User)
    assert res_post.status_code == 200
    res_delete = user_api.delete_username(My_User.username)
    assert res_delete.status_code == 200
    res_get = user_api.get_username(My_User.username)
    assert res_get.status_code == 404
    mylogger.info("Deleted Success!")
