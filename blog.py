# Team Joe
#
# SoftDev1 pd09
# P#00 Da Art of Storytellin'
# 2019-10-28

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def Login():
	return render_template("LoginPage.html")

@app.route("/Main")
def Main():
	return render_template("MainPage.html")

@app.route("/Register")
def Register():
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
