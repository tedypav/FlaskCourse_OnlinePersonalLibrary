# Online Library

The aim of this application is to provide an environment for people to store 
information about the resources (books, articles, videos, papers, etc.) they
want or need to consume, that would enable the users to easily organise and browse
through their registered materials. It is especially useful for academics, writers
and researchers.

The application has the following features:
1. Registering as a user, with the option to check and update your user information
1. Registering a resource, updating its information or deleting it altogether
1. Adding the resource as a file, which will be saved in an AWS S3 Bucket (the files can 
   also be overwritten and deleted, if necessary)
1. The user can also put tags on every resource, and later browse their resources by tag
1. Tags and all assignments to them can be deleted
1. Every person can also check general statistics for the online library database

Below you will get more information on how to use the application 🙂 Have fun!

## Table of contents


# Project walk-though

## Install

Before you start, please be sure to install all required libraries. You can find them in
the `requirements.txt` file or simply install them with the following command in 
your terminal:

`pip install -r requirements.txt`

## Run the app

To run the application, you need to open the project and run the file `main.py`
or open a command prompt window in the folder where you downloaded the application
and run the command:

`python main.py`

## Run the tests

To run the test and ensure everything is fine (for now), run the `tests` package 
or open a command prompt window in the folder where you downloaded the application
and run the command:

`pytest tests/`

## Project structure

The project consists of a few Python packages and 

## Future project development

There are still many things that need to be added to the library. Here's a list:

1. Feature: Being able to search by words in the notes of the resources.
1. Record last login time and user activity. These could later be used to enhance the personal statistics.
1. Add an endpoint for personal statistics, so users could track their resources and activity.
1. Create collections, so that users can group resources and tags together, then browse by them.
1. Feature: Being able to browse resource by status.
1. Feature: Being able to share resources you have registered with other users of the library.
1. Introduce user roles (readers, administrators).
1. Being able to delete users (this should only be an option for the administrators).
1. Feature: Being able to replicate other people's resources (those that are shared with you).
1. Feature: Being able to change your password and registered e-mail.
1. Add endpoints for bulk registering of resources, tagging, update and delete.

# REST API

The endpoint information is divided in a few sections depending on the object in
question:
1. General statistics
1. User
1. Resources
1. Tags

## General statistics

People enjoy looking at data and statistics, therefore this endpoint is mainly for 
users' pleasure. Here you can check the number of registered users, resources and other interesting 
bits of information.

`/general_stats/`

    curl --location --request GET 'http://localhost:5000/general_stats/'

    Headers: None
    Body: None

## User requests

### Register to the library

Firstly, you'll need to register to the library, so you could try all the good things 
it has to offer.

#### Request

`/register/`

    curl --location --request POST 'http://localhost:5000/register/' 

    Headers: "Content-Type": "application/json"
    Body: first_name (mandatory; a string between 1 and 30 characters)
          last_name (mandatory; a string between 1 and 30 characters)
          email (mandatory; a valid e-mail address)
          password (mandatory; needs to have at least 6 characters, at least 1 lowercase letter, 
                     at least 1 capital letter, at least 1 digit, at least 1 special symbol of the
                     following: ["$", "@", "#", "%", "^", "*", ")", ".", "(", "-", "=", "!", "&", "+"])
          phone (optional; a valid phone number of the format "+[country code][phone number]")
          company (optional; a string between 1 and 50 characters)
          job_position (optional; a string between 1 and 50 characters)

#### Response

If everything is okay (you provided all mandatory fields, a valid e-mail and a valid password),
you'll get the following response:

    Status: 201 CREATED
    Body: "message": "Welcome to our library! This token will only be valid for the next 120 minutes. After that you'll need to log in 😉"
          "token": token

If you missed any of the required fields, you'll get the following:

    Status: 400 BAD REQUEST
    Body: "message": {A dictionary of all missing requrired fields}

If there is a problem with the provided e-mail, expect to see:

    Status: 400 BAD REQUEST
    Body: "message": "email": ["Not a valid email address."]

If the password doesn't meet the requirements, you'll get details on which of the 
requirements you're missing.

If you try to register a second time with the same e-mail, you won't be able to:

    Status: 400 BAD REQUEST
    Body: "message": "There is already an account with this e-mail. Please, log in or register with another e-mail 🙂"

### Login

At the moment of writing this documentation, the token validity is 120 minutes (which could easily
be changed by switching the environment variables). After it has expired, you need to generate 
a new one from the login endpoint.

#### Request

`/login/`

    curl --location --request POST 'http://localhost:5000/login/'

    Headers: "Content-Type": "application/json"
    Body: email (mandatory; the e-mail you registered with)
          password (mandatory; the password you registered with)

#### Response

A successful login will look like this:

    Status: 200 OK
    Body: "message": "This token will only be valid for the next 120 minutes. After that you'll need to log in again 😉"
          "token": token

If you decided to add more fields, you'll get a bad request:

    Status: 400 BAD REQUEST
    Body: "message": {"the field nobody requested you to add": ["Unknown field."]}

If you provided a wrong password:

    Status: 400 BAD REQUEST
    Body: "message": "The provided password is incorrect. Please, try again 😔"

Don't worry, we won't lock your account, if you try logging with a wrong password too many times 😉
(although that's probably a good feature for future development)

If you mistyped your e-mail:

    Status: 400 BAD REQUEST
    Body: "message": "This e-mail hasn't been registered in the library. Please, register or check your input data 😔"

### Get your user information

After you've been registered for a while, you'll probably want to check your profile.

#### Request

`/my_user/`

    curl --location --request GET 'http://localhost:5000/my_user/'

    Headers: "Authorization": "Bearer <token>"

#### Response

If your token is valid, you'll get your user information.

    Status: 200 OK
    Body: "message": "Below you'll find your user information."
          "user": {
                     "company": "Test Co",
                     "job_position": "QA Tester",
                     "user_id": 0,
                     "first_name": "Test",
                     "last_name": "Testing",
                     "email": "test.testing@example.com",
                     "phone": "+[country code][valid phone number]"
                     }

If your token has expired or invalid, however, you'll get:

    Status: 401 UNAUTHORIZED
    Body: "message": "Sorry, your token is invalid 😒. Please, register or login again to obtain a valid token."

or

    Status: 401 UNAUTHORIZED
    Body: "message": "Sorry, your token has expired. Please, log in again."

This is applicable for all endpoints that require authorization.

### Update your user information

At some point you may want to change your information, here is how to do it.

#### Request

`/update_user/`

    curl --location --request PUT 'http://localhost:5000/update_user/'

    Headers: "Authorization": "Bearer <token>"
             "Content-Type": "application/json"
    Body: first_name (optional; a string between 1 and 30 characters)
          last_name (optional; a string between 1 and 30 characters)
          phone (optional; a valid phone number of the format "+[country code][phone number]")
          company (optional; a string between 1 and 50 characters)
          job_position (optional; a string between 1 and 50 characters)

#### Response

If you put valid information and managed to authenticate, you'll get:

    Status: 200 OK
    Body: "message": "You successfully updated your user information."

You will see a successful message, even if you don't provide any new information.

If you added an unregistered field, the API will throw an error:

    Status: 400 BAD REQUEST
    Body: "message": {"unregistered_field": ["Unknown field."]}

You'll get a similar message if you make a mistake in the fields' data type:

    Status: 400 BAD REQUEST
    Body: "message": {"job_position": ["Not a valid string."]}

## Resource requests

The main objects you'll work with in the library are the resources. They could be of many types:
books, articles, videos, magazines, etc.

### Register a new resource

When you first sign up to the library, you won't have any resources. To change that, send a request 
to the endpoint below.

#### Request

`/new_resource/`

    curl --location --request POST 'http://localhost:5000/new_resource/'
    Headers: "Authorization": "Bearer <token>"
             "Content-Type": "application/json"
    Body: title (mandatory; a string between 3 and 150 characters)
          author (mandatory; a string between 3 and 150 characters)
          link (optional; a string between 3 and 300 characters)
          notes (optional; a text field)
          rating (optional; a number between 0 and 5, with maximum 1 number after the decimal sign)

#### Response

A successful attempt's result will look like this:

    Status: 201 CREATED
    Body: "message": "You successfully created a new resource! 🙂"
          "resource": {
                        resource_id: 0,
                        "created_datetime": "YYYY-MM-DDTHH:MM:SS.SSSS",
                        "author": "Test Author, Test Author 2",
                        "status": "To Read",
                        "title": "My First Resource"
                      }

If a field is missing, the response is:

    Status: 400 BAD REQUEST
    Body: "message": {"title": ["Missing data for required field."]}

### Upload resource file

Sometimes it's possible that you have the resource itself - maybe you bought a paper or e-book and 
would like to save it somewhere. The Online Library can help here, too.

#### Request

`/upload_file/<resource_id>/`

    curl --location --request POST 'http://localhost:5000/upload_file/<resource_id>/'
    Headers: "Authorization": "Bearer <token>"
    Form: file=<path to uploaded file>

The specific thing about this endpoint is that the file needs to be provided through "form-data".

#### Response

If you managed to upload the file, you'll receive the following response:

    Status: 201 CREATED
    Body: "message": "You successfully uploaded the file in the following location: <link to S3 bucket>"

If you don't provide a file:

    Status: 400 BAD REQUEST
    Body: "message": "You probably forgot to attach the file 🙂 Please, provide it in the form-data section, with key = file."

If you upload a file to a resource with an existing file, the first one will be overwritten 
and deleted. Only the latest uploaded file will stay in the S3 Bucket.

### Tag a resource

A key functionality of the library is the opportunity to tag resource, so later you could find 
them more easily. There isn't a specific endpoint for tag creation, we'll create the tags for you on 
the go. If you list duplicate tags for a given resource, we'll also deduplicate them for you (nobody 
likes messy resource information). Currently, we don't format the tags, though. This means that 
tagging is case-sensitive, so be careful with the tagging.

#### Request

`/tag_resource/`

    curl --location --request POST 'http://localhost:5000/tag_resource/'
    Headers: "Authorization": "Bearer <token>"
             "Content-Type": "application/json"
    Body: resource_id (mandatory; the ID of the resource you'd like to tag; you can check it from the
                      "Get all your resources" endpoint)
          tag (mandatory; a list of strings each of maximum length 50 characters; there is no limit 
              as to how many tags you use)

#### Response

If all is correct, you'll get the following:

    Status: 201 CREATED
    Body: "message": "You successfully tagged the resource 🙂"
          "resource": {"tags": [<list of tags>]}

If you provide a tag that exceeds 50 characters in length:

    Status: 400 BAD REQUEST
    Body: "message": "The tag <tag> is too long, please shorten it to up to 50 characters 🙂"

On the other hand, if you forget to give a tag whatsoever:

    Status: 400 BAD REQUEST
    Body: "message": "You haven't provided any tags 🙂"

And if you provide an empty string, it also doesn't count:

    Status: 400 BAD REQUEST
    Body: "message": "You provided an empty string for tag... That's not cool..."


### Get all your resources

To get all of the available information about your resources, check out the next endpoint.

#### Request

`/my_resources/`

    curl --location --request GET 'http://localhost:5000/my_resources/'
    Headers: "Authorization": "Bearer <token>"

#### Response

If everything is okay with your token, you'll get it right away:

    Status: 200 OK
    Body: "message": "Below is a list of all resources you have previously registered 🙂"
          "resources": [<resource information>]

### Get resources by tag

An important feature is being able to easily find all the resources you previously registered 
and tagged in a certain way. This will probably be very handy whenever you're writing about a topic 
you've already researched before, so this time you can get your resources and notes straightaway.

#### Request

`/my_resources_with_tag/<tag>/`

    curl --location --request GET 'http://localhost/my_resources_with_tag/<tag>/'
    Headers: "Authorization": "Bearer <token>"

#### Response

If you entered a valid tag, you'll get the list:

    Status: 200 OK
    Body: "message": "Below are all resources you tagged as <tag>"
          "resources": [<resource information>]

If you entered a tag you haven't used before, you'd get the following response:

    Status: 400 BAD REQUEST
    Body: "message": "You haven't used this tag before 😒"

### Update a resource

There are many reasons why you'd like to update your resource - you mistyped the title, want to add
notes, want to change the link... All of these are possible with the next endpoint.

#### Request

`/update_resource/`

    curl --location --request PUT 'http://localhost:5000/update_resource/'
    Headers: "Authorization": "Bearer <token>"
             "Content-Type": "application/json"
    Body: resource_id (mandatory; the ID of the resource to be updated)
          title (optional; a string between 3 and 150 characters)
          author (optional; a string between 3 and 150 characters)
          link (optional; a string between 3 and 300 characters)
          notes (optional; a text field)
          rating (optional; a number between 0 and 5, with maximum 1 number after the decimal sign)


#### Response

If you try to update a resource which you haven't registered before, you won't succeed:

    Status: 403 FORBIDDEN
    Body: "message": "You need to be the owner of this resource to change or delete it 😒"

If you try to update a non-existent resource, this will also be a problem:

    Status: 400 BAD REQUEST
    Body: "message": "Don't try to trick us, this resource doesn't exist! 😉"

But if you provide correct information, you'll be rewarded with:

    Status: 200 OK
    Body: "message": "You successfully updated resource with ID = <resource_id>."

### Change resource status

As you consume the resources, you might want to change their status, so they wouldn't all stay in the
 "To Read" section. The next three endpoints behave in the same way and could be put in one group. 
The failure messages are the same for all of them, so they are only mentioned in the "Dropped" status
 update.

#### Request

To change the resource's status to "Dropped":

`/resource_status/<resource_id>/dropped/`

    curl --location --request PUT 'http://localhost:5000/resource_status/<resource_id>/dropped/'
    Headers: "Authorization": "Bearer <token>"

#### Response

Success looks like this:

    Status: 200 OK
    Body: "message": "You successfully changed this resource's status to Dropped"

If the resource doesn't exist, you'll get:

    Status: 400 BAD REQUEST
    Body: "message": "Don't try to trick us, this resource doesn't exist! 😉"

If you try to change another user's resource, you won't succeed:

    Status: 403 FORBIDDEN
    Body: "message": "You need to be the owner of this resource to change or delete it 😒"

#### Request

To change the resource's status to "Read":

`/resource_status/<resource_id>/read/`

    curl --location --request PUT 'http://localhost:5000/resource_status/<resource_id>/read/'
    Headers: "Authorization": "Bearer <token>"

#### Response

Success looks like this:

    Status: 200 OK
    Body: "message": "You successfully changed this resource's status to Read"

#### Request

To change the resource's status to "To Read":

`/resource_status/<resource_id>/to_read/`

    curl --location --request PUT 'http://localhost:5000/resource_status/<resource_id>/to_read/'
    Headers: "Authorization": "Bearer <token>"


#### Response

Success looks like this:

    Status: 200 OK
    Body: "message": "You successfully changed this resource's status to To Read"


### Delete a resource

Naturally, you might also just want to delete a given resource.

#### Request

`/delete_resource/<resource_id>/`

    curl --location --request DELETE 'http://localhost:5000/delete_resource/<resource_id>/'
    Headers: "Authorization": "Bearer <token>"

#### Response

The failed attempts will get the same responses as with the resource updates. The successful attemps 
go like this:

    Status: 200 OK
    Body: "message": "You successfully deleted resource with ID = <resource_id>."

Along with the resource, all of its tag assignments will be deleted. But your tags will stay intact - 
no tags are deleted through this endpoint.

### Delete a resource file

Something else you might want is to delete your resource file.

#### Request

`/delete_file/<resource_id>/`

    curl --location --request DELETE 'http://localhost:5000/delete_file/<resource_id>/'
    Headers: "Authorization": "Bearer <token>"

#### Response

The failed attempts will get the same responses as with the resource updates. The successful attemps 
go like this:

    Status: 200 OK
    Body: "message": "The file is now gone forever 😒"

## Tag requests

This section has only two endpoints for tag management.

### Get all your tags

This is the endpoint you can use to get all your tags, as it's easy to lose track when you're tagging 
all kinds of responses.

#### Request

`/my_tags/`

    curl --location --request GET 'http://localhost:5000/my_tags/'
    Headers: "Authorization": "Bearer <token>"

#### Response

If everything is okay with your token, you'll get:

    Status: 200 OK
    Body: "message": "Below is a list of all tags you have previously used 🙂"
          "tags": [<tag information>]

### Delete a tag

With the way tags are created, it's really easy for you to make a mistake and mistype a tag, or simply 
not need one anymore. In these cases you probably want to delete both the tag and all assignments to 
it. 

#### Request

`/delete_tag/<tag>/`

    curl --location --request DELETE 'http://localhost:5000/delete_tag/<tag>/'
    Headers: "Authorization": "Bearer <token>"

#### Response

If you try to delete a tag you haven't used before, you'll get the same response as in the "Get 
resources by tag" endpoint. If you provide the correct information, you'll receive:

    Status: 200 OK
    Body: "message": "You successfully deleted the tag <tag> and all assignments associated to it."

Along with the tag, all assignments to it to existing resources will also be deleted.
