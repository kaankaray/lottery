import os
import unittest
import main
from ChainObject import Chain
import AccountManager
import time
from web3 import Web3, HTTPProvider
import json
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.rpc import rpc_gas_price_strategy

exChain = Chain(name="Rinkeby", baseURL="https://api-rinkeby.etherscan.io/api")
globalEthAcc = AccountManager.AccountManager(randomSeed=10)
print(exChain)


class MyTestCase(unittest.TestCase):
    def test_API_key_exists(self):
        self.assertIsNotNone(os.environ.get(f'API_{exChain.name}'))

    def test_fetchTransactions(self):
        exChain.fetchTransactions(globalEthAcc)
        main.logging.info(f'Transaction count is: {len(exChain.transactions)}')
        self.assertGreater(len(exChain.transactions), 0)

    def test_fetchBalance(self):
        exChain.fetchTransactions(globalEthAcc)
        main.logging.info(f'Balance is {exChain.balance} ETH')
        self.assertNotEqual(exChain.balance, 0)

    def test_infura_connection(self):
        w3 = Web3(Web3.HTTPProvider(f'https://rinkeby.infura.io/v3/{os.getenv("infuraProjectID")}'))
        # print(w3.eth.estimate_gas())
        self.assertTrue(w3.isConnected())

    def test_infura_send_eth(self):
        w3 = Web3(Web3.HTTPProvider(f'https://rinkeby.infura.io/v3/{os.getenv("infuraProjectID")}'))
        testAddr = '0x49351B9E33155cf5441B47D63eC6E6909422c18c'
        firstBalance = w3.eth.get_balance(testAddr)
        w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
        tx_create = w3.eth.account.sign_transaction(
            {
                "nonce": w3.eth.get_transaction_count(Web3.toChecksumAddress(globalEthAcc.walletVersion)),
                "gasPrice": w3.eth.generate_gas_price(),
                "gas": 21000,
                "to": Web3.toChecksumAddress(testAddr),
                "value": 100000000000000,  # 0.01 ETH
            },
            globalEthAcc.fetchPrivKey(),
        )
        tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        main.logging.debug(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")
        time.sleep(3)
        lastBalance = w3.eth.get_balance(testAddr)
        self.assertEqual(100000000000000, lastBalance - firstBalance)


if __name__ == '__main__':
    unittest.main()


