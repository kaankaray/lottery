import time
import logging
from datetime import datetime
import ChainObject
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import AccountManager

# TODO: remove 'test' from db name.

date = 0
globalEthAcc = AccountManager.AccountManager(randomSeed=10)
chains = []


def timeStampToDate(timestamp, resultFormat='%Y-%m-%d %H:%M:%S'):
    return datetime.utcfromtimestamp(timestamp).strftime(resultFormat)


def test():
    print('test')


def determineWinner():
    for c in chains:
        c.pickWinner()

    time.sleep(10 * 60)  # Sleep 10 mins after winner is selected. To create a new address.

    checkIfAddressExistsOrCreate()


def checkIfAddressExistsOrCreate():
    global globalEthAcc
    currentDateStr = timeStampToDate(time.time(), "%Y%m%d%S")
    conn = sqlite3.connect('test_database.sqlite3')
    c = conn.cursor()
    c.execute(f'''SELECT lottery_date, private_key FROM winners_Rinkeby ORDER BY lottery_date DESC''')
    smthData = c.fetchall()

    if len(smthData) == 0 or smthData[0][1] is None:
        # Create
        response = requests.get('https://www.random.org/integers/?num=1&min=-999999999&max=999999999&col=1&base=10'
                                '&format=plain&rnd=new')
        globalEthAcc = AccountManager.AccountManager(randomSeed=response)
        logging.info(f'New day is added to the database. {globalEthAcc.walletVersion}')
        c.execute('''INSERT INTO winners_Rinkeby (lottery_date, winner_address, private_key) 
            VALUES (?, ?, ?)''', (currentDateStr, None, globalEthAcc.fetchPrivKey())
                  )
    else:
        # Already exists.
        globalEthAcc = AccountManager.AccountManager(privKey=smthData[0][1])
        logging.info(f'Already existing day reloaded. {globalEthAcc.walletVersion}')
    conn.commit()
    conn.close()


def execute():
    # os.remove("test_database.sqlite3")  # REMOVE ON LAUNCH
    chains.append(ChainObject.Chain(name="Rinkeby", baseURL="https://api-rinkeby.etherscan.io/api"))
    # chains.append(ChainObject.Chain(name="Mainnet", baseURL="https://api-rinkeby.etherscan.io/api"))
    # chains.append(ChainObject.Chain(name="BSC", baseURL="https://api-rinkeby.etherscan.io/api"))
    # chains.append(ChainObject.Chain(name="Polygon", baseURL="https://api-rinkeby.etherscan.io/api"))

    scheduler = BackgroundScheduler()
    scheduler.configure(timezone="UTC")
    # scheduler.add_job(test, 'interval', seconds=30, name='test')
    scheduler.add_job(determineWinner, 'cron', hour=23, minute=55, second=0, name='Winner winner chicken dinner.')
    checkIfAddressExistsOrCreate()
    scheduler.start()

    try:
        while True:
            logging.info(f'Loop ran at {timeStampToDate(time.time())}')
            for c in chains:
                c.fetchTransactions(globalEthAcc)
            test()
            time.sleep(10)
            # break
    except KeyboardInterrupt:
        logging.info(f'Keyboard interruption detected at {timeStampToDate(time.time())}')
        scheduler.shutdown()


if __name__ == '__main__':
    logging.warning('only worker called.')
    execute()
