from flask import Flask, render_template, request, url_for, redirect
from threading import Thread
import mainWorker as w
import logging

app = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s (%(filename)s / %(funcName)s): %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('output.log')
    ]
)


# @app.route('/', methods=['GET', 'POST'])
# def home():
#     return 'Hello'
#     return redirect(url_for('hello'))


@app.route('/', methods=['GET', 'POST'])
def hello():
    # In case I need button handling.
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            pass  # do something
        elif request.form['submit_button'] == 'Do Something Else':
            pass  # do something else
        else:
            pass  # unknown
    elif request.method == 'GET':
        selectedChain = request.args.get('chain')
        selectedChainID = -1
        for c in range(0, len(w.chains)):
            if w.chains[c].name.lower() == selectedChain:
                selectedChainID = c
                selectedChain = w.chains[c].name
        return render_template('main.html',
                               value=w.chains[selectedChainID if selectedChainID != -1 else 0].transactions,
                               selectedChain=selectedChain if selectedChainID != -1 else 'Mainnet')



if __name__ == '__main__':
    t = Thread(target=w.execute, args=())
    t.start()
    # pool = Pool(processes=1) # Am I gonna need multiple threads?
    # pool.apply_async(w.execute)


    app.run()
