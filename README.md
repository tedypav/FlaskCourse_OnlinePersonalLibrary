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
- [Online Library](#online-library)
- [Project walk-though](#project-walk-though)
  * [Install](#install)
  * [Run the app](#run-the-app)
  * [Run the tests](#run-the-tests)
- [REST API](#rest-api)
  * [General statistics](#general-statistics)
  * [User requests](#user-requests)
    + [Register to the library](#register-to-the-library)
      - [Request](#request)
      - [Response](#response)
    + [Login](#login)

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

# REST API

The endpoint information is divided in a few sections depending on the object in
question:
1. General statistics
1. User
1. Resources
1. Tags

## General statistics

People enjoy looking at data and statistics, therefore this endpoint is mainly for 
users' pleasure.

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
          phone (optional; a valid phone number)
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

    curl --location --request GET 'http://localhost:5000/my_user'

    Headers: "Authorization": "Bearer token"