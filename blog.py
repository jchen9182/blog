# Team Joe
#
# SoftDev1 pd09
# P#00 Da Art of Storytellin'
# 2019-10-28

from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os

#-----------------------------------------------------------------
#DATABASE SETUP
DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='userdata' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE userdata (user TEXT, pass TEXT);")
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='blogdata' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE blogdata(blogid INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, title TEXT,content BLOB);")

#-----------------------------------------------------------------
#FLASK APP

app = Flask(__name__)
app.secret_key = os.urandom(32)
#some helpful global variables
message = ""
loggedin = False
lastRoute = "/"
editID = -1

def rend_temp(template, mess):
    global message
    if (mess != ""):
        message = ""
        return render_template(template, m = mess)
    return render_template(template)

@app.route("/", methods=['GET', 'POST'])
def Login():
    global lastRoute
    global loggedin
    loggedin = False
    lastRoute = "/"
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT * FROM userdata")
        valid = c.fetchall()
        if("username" in session and "password" in session):
            if (session["username"], session["password"]) in valid:
                loggedin = True
                return redirect("/Main")
                #check if the credentials are in our userdatabase, if so they log in
    return rend_temp("LoginPage.html", message)

##check if the user entered a valid combo of username and passwor
@app.route("/loginHelper", methods=['GET', 'POST'])
def helper():
    global message
    global loggedin
    if (len(request.args) == 0): return redirect(lastRoute)
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT * FROM userdata")
        valid = c.fetchall()
        if (request.args["username"], request.args["password"]) in valid:
            session["username"] = request.args["username"]
            session["password"] = request.args["password"]
            loggedin = True
            return redirect("/Main")
        # if (session["username"], session["password"]) in valid:
        #     return redirect("/Main")
        message = "Username or password incorrect."
        return redirect("/")


@app.route("/Main")
def Main():
    global lastRoute
    if (not loggedin): return redirect(lastRoute)
    lastRoute = "/Main"
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT * FROM blogdata")
        allblogs = c.fetchall()
        url = {}
        #looking at all the blogs
        for entry in allblogs:
            url[entry[0]] = "http://127.0.0.1:5000/Blog?id=" + str(entry[0])
        return render_template("MainPage.html", smth = allblogs, u = url)

@app.route("/Register", methods=['GET', 'POST'])
def Register():
    global lastRoute
    lastRoute = "/Register"
    return rend_temp("RegisterPage.html", message)

@app.route("/Blog")
def Blog():
    global lastRoute
    global editID
    if (not loggedin): return redirect(lastRoute)
    lastRoute = "/Blog?id=" + request.args["id"]
    #creates new url for each individual blog
    editID = int(request.args["id"])
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT * FROM blogdata WHERE blogid = (?)", (request.args["id"],))
        blog = c.fetchone()
        #rendering the blog
        return render_template("BlogPage.html", b = blog, u = session["username"])

##Below is a checker
##If you register, it checs the following
@app.route("/registerHelper", methods= ['GET', 'POST'])
def Registered():
    global message
    #this is the message to make sure it tells you whats wrtong
    if (len(request.args) == 0): return redirect(lastRoute)
    #makes sure your password is actually there
    with sqlite3.connect(DB_FILE) as db:
    #initialize the SLIQTE database
        if (len(request.args["username"]) > 0):
            c = db.cursor()
            #makses sure that there actually is a database there
            if (len(request.args["password"]) == 0):
                message = "Password is empty."
                return redirect("/Register")
            if (request.args["password"] == request.args["repeat"]):
                #makes sure the passwrds are the same
                c.execute('SELECT * FROM userdata WHERE user = (?)', (request.args["username"],))
                if (len(c.fetchall()) > 0) :
                    #if theres already an account with that username, makes u redo
                    message = "Username already exists."
                    return redirect("/Register")
                c.execute('INSERT INTO userdata VALUES (?, ?)',(request.args["username"], request.args["password"]))
                message = "Account Created!"
                #Yay!
                return redirect("/")
            else:
                message = "Passwords do not match."
                return redirect("/Register")
        message = "Username not filled out."
        return redirect("/Register")


@app.route("/Profile")
def Profile():
    if (not loggedin): return redirect(lastRoute)
    return render_template("ProfilePage.html", user = session["username"])

@app.route("/CreateBlog")
def CreateBlog():
    if (not loggedin): return redirect(lastRoute)
    #sed cbhelper
    return rend_temp("CreateBlogPage.html", message)

@app.route("/createHelper")
def cbHelper():
    global message
    if (len(request.args) == 0): return redirect(lastRoute)
    if(len(request.args["title"]) == 0):
        message = "Title field can't be empty!"
        return redirect("/CreateBlog")
    if(len(request.args["body"].rstrip()) == 0):
        message = "Body has no text!"
        return redirect("/CreateBlog")
        ##make sure the form entries are valid
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        #otherwise insert the new blog into the blog databaset
        c.execute('''INSERT INTO blogdata VALUES (?, ?, ?, ?)''', (None, session["username"], "" + request.args["title"], "" + request.args["body"]))
        return redirect("/Main")

@app.route("/MyBlogs")
def MyBlogs():
    ##this has the same algorithm as the showing all blogs section, except it makes sure the user is the profile
    global lastRoute
    if (not loggedin): return redirect(lastRoute)
    lastRoute = "/MyBlogs"
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        if (len(request.args) > 0):
            if 'delete' in request.args:
                c.execute('''DELETE FROM blogdata WHERE user = (?) AND blogid = (?)''', (session["username"], str(editID)))
        c.execute('''SELECT * FROM blogdata WHERE user = (?)''', (session["username"],))
        myBlogs = c.fetchall()
        url = {}
        for entry in myBlogs:
            url[entry[0]] = "http://127.0.0.1:5000/Blog?id=" + str(entry[0])
        return render_template("MyBlogsPage.html", mb = myBlogs, u = url)

@app.route("/EditBlog", methods = ["GET"])
def edit():
    global editID
    global lastRoute
    global message
    if (not loggedin): return redirect(lastRoute)
    lastRoute = "/EditBlog"
    if (editID < 0): return redirect(lastRoute)
    #makes sure ur actually on a blog
    with sqlite3.connect(DB_FILE) as db:
        #then it'll update the blog
        c = db.cursor()
        gang = c.execute('''SELECT * FROM blogdata WHERE user = (?) and blogid = (?)''', (session["username"], str(editID)))
        Title = ""
        Body = ""
        for theans in gang:
            Title = theans[2]
            Body = theans[3]
        #title abnd body in the fetchall
    temp = message
    if (message != ""):
        message = ""
    return render_template("EditBlog.html", title = Title, body = Body, m = temp)

@app.route("/EditHelper")
def update():
    global editID
    global message
    if (editID < 0): return redirect(lastRoute)
    if (len(request.args) == 0): return redirect(lastRoute)
    if(len(request.args["title"]) == 0):
        message = "Title field can't be empty!"
        return redirect(lastRoute)
    if(len(request.args["body"].rstrip()) == 0):
        message = "Body has no text!"
        return redirect(lastRoute)
        ##make sure the form entries are valid
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute('''DELETE FROM blogdata WHERE blogid = (?)''', str(editID))
        #print(c.fetchall())
        c.execute('''INSERT INTO blogdata VALUES (?,?,?,?)''', (str(editID), session["username"], request.args["title"], request.args["body"]))
        #print(c.fetchall())
    return redirect("/MyBlogs")

@app.route("/auth2")
def something6():
    if (len(request.args) == 0): return redirect(lastRoute)
    if 'delete' in request.args:
        with sqlite3.connect(DB_FILE) as db:
            c = db.cursor()
            c.execute('''UPDATE blogdata SET user = REPLACE(user, user, '[DELETED]') WHERE user = (?)''', (session["username"],))
            c.execute('''DELETE FROM userdata WHERE user = (?)''', (session["username"],))
    # remove username and password from session
    session.pop('username')
    session.pop('password')
    # go back to login screen
    return redirect("/")

if __name__ == "__main__":
	app.debug = True
	app.run()

db.commit()
db.close()
