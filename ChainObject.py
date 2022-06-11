import main
import os
import requests
import Transaction
import sqlite3
import mainWorker
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.rpc import rpc_gas_price_strategy


class Chain(object):
    """
    Every chain/env will have their own chains with transactions stored within.
    """
    name: str
    baseURL: str
    _apiKey: str
    transactions = []
    balance = 0

    def sendTransaction(self, winnerAddress):
        w3 = Web3(HTTPProvider(f'https://rinkeby.infura.io/v3/{os.getenv("infuraProjectID")}'))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

        balance = w3.eth.get_balance(Web3.toChecksumAddress(mainWorker.globalEthAcc.walletVersion))
        estimatedGasPrice = w3.eth.generate_gas_price()

        tx = w3.eth.account.sign_transaction(
            {
                "nonce": w3.eth.get_transaction_count(Web3.toChecksumAddress(mainWorker.globalEthAcc.walletVersion)),
                'gasPrice': estimatedGasPrice,
                'gas': 21000,
                "to": Web3.toChecksumAddress(winnerAddress),
                "value": balance - (estimatedGasPrice * 21000),
            }, mainWorker.globalEthAcc.fetchPrivKey()
        )

        tx_hash = w3.eth.send_raw_transaction(tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        main.logging.info(f"{self.name} chain transaction sent successfully to winner"
                          f" {winnerAddress} hash: {tx_receipt.transactionHash.hex()}")

    def pickWinner(self):
        self.fetchTransactions(mainWorker.globalEthAcc)
        tempBalance = self.balance * pow(10, 4)
        if tempBalance > 100_000:
            response = requests.get(f'https://www.random.org/integers/?num=1&min=0&max={int(tempBalance)}&col=1&base=10'
                                    f'&format=plain&rnd=new')
            tempBalance = int(response.text)
            for t in self.transactions:
                if tempBalance - (t.amount * pow(10, 4)) < 0:
                    main.logging.info('Winner is:')
                    t.printTransaction()
                    self.sendTransaction(t.senderAddress)
                    # TODO: Store the winner in DB

                    self.balance = 0
                    self.transactions = []
                    break
                else:
                    tempBalance -= t.amount * pow(10, 4)
        else:
            # TODO: Log no winner to DB
            print()

    def fetchTransactions(self, acc):
        try:
            res = requests.get(
                f'{self.baseURL}?module=account'
                f'&action=txlist'
                f'&address={acc.walletVersion}'
                f'&sort=desc'
                f'&apikey={self._apiKey}'
            ).json()
            for t in res['result']:

                if any(tx.hash == t['hash'] for tx in self.transactions):
                    pass
                else:
                    tx = Transaction.Transaction(t)
                    self.balance += float(t['value']) / pow(10, 18)
                    self.transactions.append(tx)
                    tx.printTransaction()
                # self.balance += float(t['value']) / pow(10, 18)
                # self.transactions.append(Transaction.Transaction(t))

            for t in self.transactions:
                t.chance = t.amount / self.balance
                # t.printTransaction()
        except Exception as e:
            main.logging.error(e)

    def __init__(self, name, baseURL):
        main.logging.info(f'{name} chain initiated.')
        self.name = name
        self.baseURL = baseURL
        self._apiKey = os.getenv(f'API_{name}')

        conn = sqlite3.connect('test_database.sqlite3')
        c = conn.cursor()
        c.execute(f'''
                      CREATE TABLE IF NOT EXISTS winners_{name}
                      ([ID] INTEGER PRIMARY KEY, [lottery_date] INTEGER, [winner_address] TEXT, [private_key] TEXT)
                      ''')
        conn.commit()
        conn.close()

