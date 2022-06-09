from flask import Flask, render_template, request, make_response
from threading import Thread
import worker as w
import logging

app = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s (%(threadName)s): %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('output.log')
    ]
)


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
        print(len(w.transactions))
        return render_template('main.html', value=w.transactions)


if __name__ == '__main__':
    t = Thread(target=w.execute, args=())
    t.start()
    # pool = Pool(processes=1) # Am I gonna need multiple threads?
    # pool.apply_async(w.execute)
    app.run()
