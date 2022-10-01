# ---------------------------------------------------------- #
from flask import Flask, request, redirect, flash, send_from_directory, render_template, jsonify, url_for
from app import *
import flask
import json
import sqlite3

from utils.uploadCheck import *

conn = sqlite3.connect('database/database.db', check_same_thread=False)
c = conn.cursor()

@app.route('/upload', methods=['GET'])
def UplaodGet():
    return render_template('upload.html')

#Upload Post
@app.route('/upload', methods=['POST'])
def UplaodPost():
    formData = request.form
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER']+'tmp/', file.filename))

        org = Image.open(os.path.join(app.config['UPLOAD_FOLDER']+'tmp/', file.filename))
        org.save(os.path.join(app.config['UPLOAD_FOLDER']+'tmp/'+ file.filename.split('.')[0] + '.png'))

        import ipfsApi
        api = ipfsApi.Client('127.0.0.1', 5002)
        res = api.add(os.path.join(app.config['UPLOAD_FOLDER']+'tmp/'+ file.filename.split('.')[0] + '.png'))
        org.save(os.path.join(app.config['UPLOAD_FOLDER'] + res['Hash'] + '.png'))

        conn.execute("INSERT INTO photoColl(owner,hash) VALUES (?, ?)", (formData['wallet_id'], os.path.join(app.config['UPLOAD_FOLDER'] + res['Hash'] + '.png')))
        conn.commit()
        erase_dir()
        
        return redirect('/dashboard')

    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)
# ---------------------------------------------------------- #