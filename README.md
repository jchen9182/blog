# Joe's Blog by Team Joe

Roles
----------------------------------

#### Flask App Creator (Jude and Jason)
- Person will create a Python flask application that will have each of the routes we need (mentioned above)
- Person will make sure that the pages that require you to be logged in cannot be accessed by just typing the extension into the URL if you have not logged in
- Person will make sure to flash messages when appropriate to do so (i.e. flashing a login error when submitting a wrong username or password on the login page)
#### HTML/Jinja Template Creator (Calvin)
- Person will create the HTML templates for each of the routes
- Person will use forms when appropriate (i.e. login page => username and password inputs, submit button)
- Person will use Jinja to take in and display variables when necessary (i.e. for the blog post template, use Jinja to display a blog post pulled from the database table)
- Person will pay attention to aesthetic details
#### Database Creator (Derek)
- Person will write a Python application to create appropriate databases and tables, making sure to only add them if they don’t already exist
- Person will facilitate adding to, editing contents in, and potentially removing from tables 

How to Run
----------------------------------
**1)** Install Python3 and Flask if you have not done so already.
  - All your Flask-related needs:
  ```console
    $ pip3 install flask
  ```
**2)** Clone the reopsitory and cd into it:
```console
  $ git clone git@github.com:CalfinChoo/blog.git
  ...
  $ cd blog
```
**3)** Run the following command:
```console
  $ python app.py
```
**4)** View the webpage in your browser at URL: http://127.0.0.1:5000/

**5)** Voilà! If working properly, you should be able to navigate around the blog website!
<br>(**Hint:** Start by registering for an account!)

Libraries/Modules Involved
----------------------------------
```
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
```
- **Flask:** provides us with the web frame to locally host our blog
- **render_template:** allows us to call and display HTML templates for our web pages, as well as insert variables such as database entries into the templates using Jinja
- **request:** allows our functions to receive information/arguments from HTML forms that we can then store (e.g. login credentials, blog posts, etc.)
- **redirect:** provides us with the ability to redirect the user from one route to another when necessary (e.g. if user attempts to bypass the login page by just changing the URL)
- **url_for:** pairs with redirect; used on the function of the route we want to redirect the page to
- **sqlite3:** enables us to control our database with commands in our code
