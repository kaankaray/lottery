import os
import time
import logging
from datetime import datetime
import ChainObject

# TODO: Date check to detirmine the winner. Create address.
# TODO: remove 'test' from db name.
# TODO:
# TODO:


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s (%(threadName)s): %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('output.log')
    ]
)

date = 0


def timeStampToDate(timestamp, resultFormat='%Y-%m-%d %H:%M:%S'):
    return datetime.utcfromtimestamp(timestamp).strftime(resultFormat)


def execute():
    os.remove("test_database.sqlite3")

    chains = [
        ChainObject.Chain(name="Rinkeby", baseURL="https://api-rinkeby.etherscan.io/api")
    ]

    while True:
        logging.info(f'Loop ran at {timeStampToDate(time.time())}')
        for c in chains:
            print(c)

        break
        time.sleep(10)  # fetching is slow enough 1-2 secs.


if __name__ == '__main__':
    logging.warning('only worker called.')
    execute()
