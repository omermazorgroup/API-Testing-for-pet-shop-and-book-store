import pytest
import logging
from pet import Pet
from category import Category
from tags import Tags
from order import Order
from user import User
import pet_api
import datetime
import json

# these urls are of the local server, the default is https://petstore3.swagger.io/api/v3
petApi = pet_api.PetApi("http://localhost:8080/api/v3")
orderApi = pet_api.OrderApi("http://localhost:8080/api/v3/store")
userApi = pet_api.UserApi("http://localhost:8080/api/v3/user")
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
mylogger = logging.getLogger()

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


def test_put_pet(My_Pet):
    mylogger.info("test for update a pet")
    re =petApi.post_new_pet(My_Pet)
    My_Pet.name = "Omer"
    res_put = petApi.put_pet(My_Pet)
    res_get = petApi.get_pet_by_id(My_Pet.id)
    assert res_put.status_code == 200
    assert My_Pet.name == res_get.json()["name"]
    mylogger.info(f"Success! {res_get.json()['name']}")

def test_post_new_pet(My_Pet):
    mylogger.info("test for create a new pet")
    res_delete = petApi.delete_pet_by_id(My_Pet.id)
    res_post = petApi.post_new_pet(My_Pet)
    assert res_post.status_code == 200
    res_get = petApi.get_pet_by_id(My_Pet.id)
    assert res_get.status_code == 200
    assert res_get.json() == res_post.json()
    mylogger.info(f"Success! {res_post.json()}")

def test_get_pet_by_id(My_Pet):
    mylogger.info("test for get a  pet by id")
    petApi.post_new_pet(My_Pet)
    res_get = petApi.get_pet_by_id(My_Pet.id)
    assert res_get.status_code == 200
    assert res_get.json()["id"] == My_Pet.id
    mylogger.info(f"Success! {res_get.json()['id']}")


def test_get_pets_by_status(My_Pet):
    mylogger.info("test for get a  pet by status")
    res_get = petApi.get_pets_by_status(My_Pet.status)
    assert res_get.status_code == 200
    statusArray = []
    for pet in res_get.json():
        statusArray.append(pet["status"])
    assert My_Pet.status in statusArray
    mylogger.info(f"Success! {My_Pet.status}")


def test_get_pet_by_tags(My_Pet):
    mylogger.info("test for get a pets by tags")
    tags = []
    for tag in My_Pet.tags:
        tags.append(tag.name)
    res_get = petApi.get_pet_by_tags(tags)
    assert res_get.status_code == 200
    tagsNames = []
    for pet in res_get.json():
        for tag in pet["tags"]:
            if isinstance(tag, dict):
                tagsNames.append(tag["name"])
    assert My_Pet.tags[0].name in tagsNames
    mylogger.info(f"Success! {My_Pet.tags[0].name}")


def test_post_pet_by_id_and_update(My_Pet):
    mylogger.info("test for update a pet by name and status")
    petApi.post_new_pet(My_Pet)
    pet_before = [My_Pet.name, My_Pet.status]
    My_Pet.name = "dany"
    My_Pet.status = "sold"
    pet_after = [My_Pet.name, My_Pet.status]
    res_post = petApi.post_pet_by_id_and_update(My_Pet.id, My_Pet.name, My_Pet.status)
    assert res_post.status_code == 200
    assert res_post.json()["name"] != pet_before[0] and res_post.json()["status"] != pet_before[1]
    assert res_post.json()["name"] == pet_after[0] and res_post.json()["status"] == pet_after[1]
    mylogger.info(f"Success! {res_post.json()['name'], res_post.json()['status']}")

def test_delete_pet_by_id(My_Pet):
    mylogger.info("test for delete a pet by id")
    res_post = petApi.post_new_pet(My_Pet)
    assert res_post.status_code == 200
    res_delete = petApi.delete_pet_by_id(My_Pet.id)
    assert res_delete.status_code == 200
    res_get = petApi.get_pet_by_id(My_Pet.id)
    assert res_get.status_code == 404
    mylogger.info("Deleted Success!")

def test_upload_image_by_id(My_Pet):
    mylogger.info("test for upload a image to an pet by a id")
    mylogger.error("this test getting error!!!")
    files = {'upload_file': open('slide-1.jpg', 'rb')}
    res_post = petApi.upload_image_by_id(My_Pet.id, files)
    mylogger.info(res_post.json())
    assert res_post.status_code == 200
    mylogger.info(f"Success {res_post.json()['message']}")


def test_get_store_inventory():
    mylogger.info("test for get a store to inventory")
    res_get = orderApi.get_store_inventory()
    assert res_get.status_code == 200
    assert type(res_get.json()) == dict
    mylogger.info(f"Success {res_get.json()}")


def test_post_order(My_Order):
    mylogger.info("test for create a new order")
    orderApi.delete_order(My_Order.id)
    res_post = orderApi.post_order(My_Order)
    assert res_post.status_code == 200
    res_get = orderApi.get_order(My_Order.id)
    mylogger.info(res_get.json())
    assert res_get.status_code == 200
    assert res_get.json() == res_post.json()
    mylogger.info(f"Success {res_get.json()}")


def test_get_order(My_Order):
    mylogger.info("test for get a order")
    orderApi.post_order(My_Order)
    res_get = orderApi.get_order(My_Order.id)
    assert res_get.status_code == 200
    assert res_get.json()["id"] == My_Order.id
    mylogger.info(f"Success {res_get.json()['id']}")


def test_delete_order(My_Order):
    mylogger.info("test for delete a order")
    res_post = orderApi.post_order(My_Order)
    assert res_post.status_code == 200
    res_delete = orderApi.delete_order(My_Order.id)
    assert res_delete.status_code == 200
    res_get = orderApi.get_order(My_Order.id)
    assert res_get.status_code == 404
    mylogger.info("Deleted Success!")


def test_post_user(My_User):
    mylogger.info("test for create a new user")
    userApi.delete_username(My_User.username)
    res_post = userApi.post_user(My_User)
    assert res_post.status_code == 200
    res_get = userApi.get_username(My_User.username)
    assert res_get.status_code == 200
    assert res_get.json() == res_post.json()
    mylogger.info(f"Success! {res_get.json()}")


def test_post_users(My_Users):
    mylogger.info("test for create a list of new users")
    mylogger.info("test post users")
    mylogger.error("this test getting error!!!")
    users = [user.to_json() for user in My_Users]
    users_json = json.dumps(users)
    res_post = userApi.post_users_list(users_json)
    assert res_post.status_code == 200


def test_get_login(My_User):
    mylogger.info("test for get login request")
    res_get = pet_api.UserApi().get_login(My_User.username, My_User.password)
    assert res_get.status_code == 200
    mylogger.info(f"Success!{res_get.content}")


def test_get_logout():
    mylogger.info("test for get logout request")
    res_get = pet_api.UserApi().get_logout()
    assert res_get.status_code == 200
    mylogger.info(f"Success!{res_get.content}")


def test_get_username(My_User):
    mylogger.info("test for get user by username")
    mylogger.error("this test getting error!!!")
    res_post = userApi.post_user(My_User)
    assert res_post.status_code == 200
    res_get = userApi.get_username(My_User.username)
    assert res_get.status_code == 200
    assert res_get.json()["username"] == My_User.username
    mylogger.info(f"Success!{res_get.json()['username']}")


def test_put_username(My_User):
    mylogger.info("test for update a username of user")
    res_post = userApi.post_user(My_User)
    assert res_post.status_code == 200
    first_username = My_User.username
    My_User.username = "omermazor2"
    res_put = userApi.put_username(first_username, My_User)
    assert res_put.status_code == 200  # REQUEST PROBLEM: RETURN 500!!!
    assert res_put.json()["username"] == My_User.username  # REQUEST PROBLEM: RETURN 500!!!
    mylogger.info(f"Success!{res_put.json()['username']}")


def test_delete_username(My_User):
    mylogger.info("test for delete a user by username")
    res_post = userApi.post_user(My_User)
    assert res_post.status_code == 200
    res_delete = userApi.delete_username(My_User.username)
    assert res_delete.status_code == 200
    res_get = userApi.get_username(My_User.username)
    assert res_get.status_code == 404
    mylogger.info("Deleted Success!")
