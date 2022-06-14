import time
import logging
from datetime import datetime
import ChainObject
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import AccountManager

# TODO: remove 'test' from db name.

globalEthAcc = AccountManager.AccountManager(randomSeed=10)
chains = []


def timeStampToDate(timestamp, resultFormat='%Y-%m-%d %H:%M:%S'):
    return datetime.utcfromtimestamp(timestamp).strftime(resultFormat)


def determineWinner():
    for c in chains:
        c.pickWinner()

    time.sleep(10 * 60)  # Sleep 10 mins after winner is selected. To create a new address.

    checkIfAddressExistsOrCreate()


def checkIfAddressExistsOrCreate():
    global globalEthAcc
    currentDateStr = timeStampToDate(time.time(), "%Y%m%d")
    conn = sqlite3.connect('database.sqlite3')
    c = conn.cursor()
    c.execute(f'''SELECT lottery_date, private_key FROM winners_{chains[0].name} ORDER BY lottery_date DESC''')
    smthData = c.fetchall()
    if len(smthData) == 0 or smthData[0][1] is None or int(smthData[0][0]) != int(currentDateStr):
        # Create
        response = requests.get('https://www.random.org/integers/?num=1&min=-999999999&max=999999999&col=1&base=10'
                                '&format=plain&rnd=new')
        globalEthAcc = AccountManager.AccountManager(randomSeed=int(response.text))
        logging.info(f'New day is added to the database. {globalEthAcc.walletVersion}')
        for chain in chains:
            c.execute(f'''INSERT INTO winners_{chain.name} 
                        (lottery_date, winner_address, private_key, wallet_version, tx_hash) VALUES (?, ?, ?, ?, ?)''',
                      (currentDateStr, "TBD", globalEthAcc.fetchPrivKey(), globalEthAcc.walletVersion, "TBD")
                      )

    else:
        # Already exists.
        globalEthAcc = AccountManager.AccountManager(privKey=smthData[0][1])
        logging.info(f'Already existing day reloaded. {globalEthAcc.walletVersion}')
    conn.commit()
    conn.close()


def execute():
    chains.append(ChainObject.Chain(name="Rinkeby", baseURL="https://api-rinkeby.etherscan.io/api", rpcURL='https://rinkeby.infura.io/v3/'))
    chains.append(ChainObject.Chain(name="Mainnet", baseURL="https://api.etherscan.io/api",         rpcURL='https://mainnet.infura.io/v3/'))
    chains.append(ChainObject.Chain(name="BSC",     baseURL="https://api.bscscan.com/api",          rpcURL='https://rinkeby.infura.io/v3/'))
    chains.append(ChainObject.Chain(name="Polygon", baseURL="https://api.polygonscan.com/api",      rpcURL='https://polygon-mainnet.infura.io/v3/'))

    scheduler = BackgroundScheduler()
    scheduler.configure(timezone="UTC")
    scheduler.add_job(determineWinner, 'cron', hour=23, minute=55, second=0, name='Winner winner chicken dinner.')
    checkIfAddressExistsOrCreate()
    scheduler.start()

    try:
        while True:
            logging.debug(f'Loop ran at {timeStampToDate(time.time())}')
            for c in chains:
                c.fetchTransactions(globalEthAcc)
            # time.sleep(5)
            # break
    except KeyboardInterrupt:
        logging.info(f'Keyboard interruption detected at {timeStampToDate(time.time())}')
        scheduler.shutdown()


if __name__ == '__main__':
    logging.warning('only worker called.')
    execute()
