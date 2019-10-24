# Team Joe
#
# SoftDev1 pd09
# P#00 Da Art of Storytellin'
# 2019-10-28

from flask import Flask, render_template, request
import sqlite3

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

@app.route("/")
def Login():
	return render_template("LoginPage.html")

@app.route("/Main")
def Main():
	return render_template("MainPage.html")

@app.route("/Register")
def Register():
    #flash("Account created")
	return render_template("RegisterPage.html")

@app.route("/Profile")
def Profile():
	return render_template("ProfilePage.html")

@app.route("/CreateBlog")
def CreateBlog():
	return render_template("CreateBlogPage.html")

@app.route("/MyBlogs")
def MyBlogs():
	return render_template("MyBlogsPage.html")

if __name__ == "__main__":
	app.debug = True
	app.run()
