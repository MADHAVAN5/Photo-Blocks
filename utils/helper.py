from flask import Flask, request, render_template, url_for, flash, redirect
from werkzeug.exceptions import abort
import os
import sys
import sqlite3
from dotenv import load_dotenv

import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction
import algosdk
from algosdk.v2client import algod
from algosdk import account as algo_acc
import yaml
import os
from pathlib import Path
from algosdk import mnemonic
from algosdk.v2client import indexer


def get_project_root_path() -> Path:
    path = Path(os.path.dirname(__file__))
    return path.parent.parent

def load_config():
    root_path = get_project_root_path()
    config_location = os.path.join(root_path, 'config.yml')

    with open(config_location) as file:
        return yaml.full_load(file)

def get_db_connection():
    """
    A function to create a sqlite db connection
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_pk(get_mnemonic: str) -> str:
    """
    A function to convert mnemonic to private key
    """
    the_pk = mnemonic.to_private_key(get_mnemonic)
    return the_pk

def get_mnemonic(private_key: str) -> str:
    """
    A function to convert private key to mnemonic
    """
    the_mnemonic = mnemonic.from_private_key(private_key)
    return the_mnemonic

    