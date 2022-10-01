# ---------------------------------------------------------- #
from flask import Flask, request, redirect, flash, send_from_directory, render_template, jsonify, url_for
from app import *
import flask
import json
import sqlite3
from utils.service.blockchain_utils.credentials import get_client, get_account_credentials
from utils.service.network_interaction.nft_service import NFTService
#from utils.service.repository.marketplace_repository import NFTMarketplace
#from utils.service.repository.nft_repository import NFTRepository
#from utils.service.repository.marketplace_repository import NFTMarketplaceRepository
import time
import algosdk

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

        imgPath = "/static/uploads/" + res['Hash'] + '.png'
        imgPath = imgPath.replace("\\", "/")
        conn.execute("INSERT INTO photoColl(owner,hash) VALUES (?, ?)", (formData['wallet_id'], imgPath))
        conn.commit()
        erase_dir()
        
        return redirect('/dashboard')

    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)
# ---------------------------------------------------------- #

@app.route('/minting/<unique_hash_link>', methods=['GET'])
def MintGet(unique_hash_link):
    return render_template('minting.html', img_location='/static/uploads/'+unique_hash_link+'.png')

@app.route('/minting', methods=['POST'])
def MintPost():
    formData = request.form

    client = get_client()
    current_trans = NFTService(nft_creator_pk='mGEs+qL0wLeBLc5ms+AMm2uqXiU4jzMadUBMTn+FQlnE9uwS9OAaS1P8fQz5hqea9txeH4rfGAB4e2cpQEzDuA==', nft_creator_address='YT3OYEXU4ANEWU74PUGPTBVHTL3NYXQ7RLPRQADYPNTSSQCMYO4BHMP62Y',
        client=client, unit_name=formData["unit_name"], asset_name=formData["asset_name"], nft_url=formData["nft_location"])
    current_trans.create_nft()

    conn.execute("UPDATE photoColl SET mint = ? WHERE hash = ?", (1, formData["nft_location"]))
    conn.commit()

    return redirect('/dashboard')

