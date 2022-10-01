from flask import Flask, request, redirect, flash, send_from_directory, render_template, jsonify, url_for
from app import *
import flask
import json
import sqlite3

conn = sqlite3.connect('database/database.db', check_same_thread=False)
c = conn.cursor()


@app.route("/", methods=["POST", "GET"])
def index():
    if flask.request.method == 'GET':
        return render_template('land.html')
    else:
        pass
    

@app.route("/dashboard", methods=["GET", 'POST'])
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    if flask.request.method == 'POST':
        data = request.data.decode("utf-8")
        data = json.loads(data)
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (data['name'], data['addr'], data['type']))
        conn.commit()
        return redirect(url_for("dashboard"))

