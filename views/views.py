from flask import request, redirect, flash, send_from_directory, render_template
from app import *


@app.route("/", methods=["POST", "GET"])
def login():
    if flask.request.method == 'GET':
        return render_template('index.html')
    else:
        pass
            

@app.route("/signup", methods=["POST", "GET"])
def index():
    if flask.request.method == 'GET':
        return render_template('signup.html')
    if flask.request.method == 'POST':   
        pass


@app.route("/login", methods=["POST", "GET"])
def index():
    if flask.request.method == 'GET':
        return render_template('login.html')
    if flask.request.method == 'POST':
        pass