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

from helper import *

config = load_config()
algorand_token = config.get('client_credentials').get('token')
algorand_test_ip_address = config.get('client_credentials').get('address')

def make_transaction(private_key, sender_address, receiver_address, amount_to_send):
    """
    A function to make a transaction between two accounts
    """
    # connect with a client given the token and address of the network
    algod_client = algod.AlgodClient(algorand_token, algorand_test_ip_address)

    # print basic sender info
    print("\nSender address: {}".format(sender_address))
    account_info = algod_client.account_info(sender_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = 1000
    # amount = 100000
    amount = amount_to_send
    note = "Initial transaction example".encode()

    # print basic receiver info
    print("\nReceiver address: {}".format(receiver_address))
    account_info = algod_client.account_info(receiver_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    unsigned_txn = transaction.PaymentTxn(sender_address, params, receiver_address, amount, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    # submit transaction
    tx_id = algod_client.send_transaction(signed_txn)
    print("Signed transaction with tx_id: {}".format(tx_id))

    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    except Exception as err:
        print("A damn error occurred: {}".format(err))
        return 

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(
        account_info.get('amount')))
    print("Amount transferred: {} microAlgos".format(amount))
    print("Fee: {} microAlgos".format(params.fee))

    account_info = algod_client.account_info(sender_address)
    print("Final Account balance: {} microAlgos".format(
        account_info.get('amount')) + "\n")
    return True

def get_balance(account_address: str) -> int:
    """
    A function that tells the accounts balance given an account address
    """
    # create a client to interact with
    client = algod.AlgodClient(algorand_token, algorand_test_ip_address)
    account_info = client.account_info(account_address)
    print(json.dumps(account_info, indent=4))

    account_balance = account_info.get('amount')
    print('Account balance: {} microAlgos'.format(account_balance))
    return account_balance

def get_records(account_address):
    """
    A function to get all account related records
    """
    print(account_address)
    return 1