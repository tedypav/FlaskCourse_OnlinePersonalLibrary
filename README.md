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

Below you will get more information on how to use the application :) Have fun!

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

