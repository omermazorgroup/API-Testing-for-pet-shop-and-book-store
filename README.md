# API-Testing-for-pet-shop-and-book-store 
## by Omer Mazor

#### Fixing issues:
I added two commits of changes that I performed 
for fixing the project:
* First I organized the project using folders and 
  subsequently I changed the path in importing 
  the files and models
* In bookstore branch I removed token.txt file 
  which contained the expiration date Bearer token and 
  instead I used fixture that which 
  updates new token with every api request
* I rename the test files so that 
  they start with the word "test"
* The user can choose the url 
* Maximum use of objects
* The url addresses of the api are 
  parameters received from the command line


# Introdaction
In this project I created a tests for two Swagger API:
 - petstore: https://petstore3.swagger.io/
 - bookstore:  https://bookstore.toolsqa.com/swagger/

# Project Overview
Create fix_API_testing folder and insert the project there

## petstore
if you don't run the API on your server delete the url's parameters from the top 
of the file pet_test.py, the default url after delete will be 'https://petstore3.swagger.io/api/v3'

16 of 19 tests passed:, 
--test_upload_image_by_id fails following a constant and recurring error response (400 +)
- test_post_users fails following a constant and recurring error response (500 +)
- test_get_username fails following a constant and recurring error response (500 +) 
![scripts](https://res.cloudinary.com/dwsdrdv3w/image/upload/v1659615673/%D7%A6%D7%99%D7%9C%D7%95%D7%9D_%D7%9E%D7%A1%D7%9A_175_mflpa2.png)

## booktore

5 tests passed, 5 tests failed, 1 ignored
- test_delete_user_by_id passed but ignored becouse it may interfere with the continuation of the testing process
- test_post_user fails if tested user is exits
- test_post_books fails following error 504-Gateway Time-Out
- test_delete_books_by_string_object passed but fails due to its necessary use in post_books
- test_delete_books_by_userid passed but fails due to its necessary use in post_books
- test_put_isbn passed but fails due to its necessary use in post_books
![scripts](https://res.cloudinary.com/dwsdrdv3w/image/upload/v1659615667/%D7%A6%D7%99%D7%9C%D7%95%D7%9D_%D7%9E%D7%A1%D7%9A_174_vdq3yj.png)
