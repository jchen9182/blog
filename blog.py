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
    c.execute("CREATE TABLE blogdata(user TEXT,blogid INT, title TEXT,content BLOB);")

#-----------------------------------------------------------------
#FLASK APP

app = Flask(__name__)
app.secret_key = os.urandom(32)
passcheck = "Type in your password"

@app.route("/", methods=['GET', 'POST'])
def Login():
    if("username" in session and "password" in session):
        #user = session['username']
        #pas = session['password']
        c.execute()
    return render_template("LoginPage.html")

@app.route("/Main")
def Main():
	return render_template("MainPage.html")

@app.route("/Register", methods=['GET', 'POST'])
def Register():
    return render_template("RegisterPage.html")

@app.route("/Registered", methods= ['GET', 'POST'])
def Registered():
    with sqlite3.connect("DB_FILE") as db:
        c = db.cursor()
        if (request.args["password"] == request.args["repeat"]):
            if type(c.fetchone()) is none:
                c.execute("CREATE TABLE userdata (user TEXT, pass TEXT);")
            c.execute('INSERT INTO userdata VALUES (?, ?)',(request.args["username"], request.args["password"]))
            return redirect("/")
            
        return redirect("/Register")



@app.route("/Profile")
def Profile():
	return render_template("ProfilePage.html")

@app.route("/CreateBlog")
def CreateBlog():
	return render_template("CreateBlogPage.html")

@app.route("/MyBlogs")
def MyBlogs():
	return render_template("MyBlogsPage.html")

db.commit()
db.close()

if __name__ == "__main__":
	app.debug = True
	app.run()
