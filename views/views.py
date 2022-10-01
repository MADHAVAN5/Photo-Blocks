from flask import Flask, request, redirect, flash, send_from_directory, render_template
from app import *
import flask

@app.route("/", methods=["POST", "GET"])
def index():
    if flask.request.method == 'GET':
        return render_template('land.html')
    else:
        pass
            

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if flask.request.method == 'GET':
        return render_template('signup.html')
    if flask.request.method == 'POST':   
        pass


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')
    if flask.request.method == 'POST':
        pass