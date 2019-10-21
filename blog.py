# Team Joe
# 
# SoftDev1 pd09
# P#00 Da Art of Storytellin'
# 2019-10-28

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def startingPage():
	return render_template("StartingPage.html")

if __name__ == "__main__":
	app.debug = True
	app.run()
