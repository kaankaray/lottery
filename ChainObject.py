import time
import os
import requests
import Transaction
import sqlite3
import mainWorker

# TODO: fetchTransactions is completely broken. Need to create the address first!
# TODO: fetchBalance is completely broken.


class Chain(object):
    """
    Every chain/env will have their own chains with transactions stored within.
    """
    name: str
    baseURL: str
    _apiKey: str

    def fetchTransactions(self):
        global transactions
        global balance
        balance = 0
        res = requests.get(
            f'{self.baseURL}?module=account'
            f'&action=txlist'
            f'&address={"asd"}'
            # f'&startblock=13706208'
            f'&sort=desc'
            f'&apikey={self._apiKey}'
        ).json()

        if int(res['status']) == 1:
            print(res['result'][1])
        # global transactions
        # transactions = []
        transactions.clear()
        for t in res['result']:
            if t['to'] == os.environ.get("testAddress"):
                balance += float(t['value']) / pow(10, 18)
                transactions.append(Transaction(t))

        for t in transactions:
            t.chance = t.amount / balance
            # t.printTransaction()

    def fetchBalance(self):
        res = requests.get(
            f'https://api.etherscan.io/api?module=account'
            f'&action=balance'
            f'&address={os.environ.get("testAddress")}'
            f'&tag=latest'
            f'&apikey={os.environ.get("etherscanKey")}'
        ).json()
        print(res)
        if int(res['status']) == 1:
            print(float(res['result']) / pow(10, 18))
            return float(res['result']) / pow(10, 18)
        else:
            return -1

    def __init__(self, name, baseURL):
        print('New chain instance created.')
        self.name = name
        self.baseURL = baseURL
        self._apiKey = os.getenv(f'API_{name}')

        conn = sqlite3.connect('test_database.sqlite3')
        c = conn.cursor()
        c.execute(f'''
                      CREATE TABLE IF NOT EXISTS winners_{name}
                      ([ID] INTEGER PRIMARY KEY, [lottery_date] INTEGER, [winner_address] TEXT, [private_key] TEXT)
                      ''')
        c.execute(f'INSERT INTO winners_{name} (lottery_date, winner_address, private_key) '
                  f'VALUES ({mainWorker.timeStampToDate(time.time(), "%Y%m%d")},"asd", "asds")'
        )

        c.execute(f'''SELECT * FROM winners_{name}''')
        print(c.fetchall())

        print(mainWorker.timeStampToDate(time.time(), '%Y%m%d'))
