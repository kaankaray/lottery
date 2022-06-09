import os
import time
import main
from datetime import datetime
import ChainObject
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import AccountManager

# TODO: Date check to detirmine the winner. Create address.
# TODO: remove 'test' from db name.
# TODO:
# TODO:

date = 0
globalEthAcc = AccountManager.AccountManager(randomSeed=10)
chains = []


def timeStampToDate(timestamp, resultFormat='%Y-%m-%d %H:%M:%S'):
    return datetime.utcfromtimestamp(timestamp).strftime(resultFormat)


def test():
    print('test')


def determineWinner():
    # TODO: actually determine the winner lol

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
        main.logging.info('New day is added to the database.')
        response = requests.get('https://www.random.org/integers/?num=1&min=-999999999&max=999999999&col=1&base=10'
                                '&format=plain&rnd=new')
        globalEthAcc = AccountManager.AccountManager(randomSeed=response)
        c.execute('''INSERT INTO winners_Rinkeby (lottery_date, winner_address, private_key) 
            VALUES (?, ?, ?)''', (currentDateStr, None, globalEthAcc.fetchPrivKey())
                  )
    else:
        # Already exists.
        main.logging.info('Already existing day reloaded.')
        globalEthAcc = AccountManager.AccountManager(privKey=smthData[0][1])
    conn.commit()
    conn.close()


def execute():
    os.remove("test_database.sqlite3")  # REMOVE ON LAUNCH
    chains.append(ChainObject.Chain(name="Rinkeby", baseURL="https://api-rinkeby.etherscan.io/api"))

    scheduler = BackgroundScheduler()
    scheduler.configure(timezone="UTC")
    scheduler.add_job(test, 'interval', seconds=5, name='Smth')
    scheduler.add_job(determineWinner, 'cron', hour=0, minute=0, second=0, name='Winner winner chicken dinner.')
    checkIfAddressExistsOrCreate()
    scheduler.start()

    while True:
        main.logging.info(f'Loop ran at {timeStampToDate(time.time())}')
        for c in chains:
            print(c)
        time.sleep(120)  # fetching is slow enough 1-2 secs.
        break
    scheduler.shutdown()


if __name__ == '__main__':
    main.logging.warning('only worker called.')
    execute()
