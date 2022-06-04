from flask import Flask, render_template, request, make_response
from threading import Thread
import worker as w
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


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


def test():
    print('test')


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(test, 'cron', second=3)
    scheduler.start()
    t = Thread(target=w.execute, args=())
    t.start()
    # pool = Pool(processes=1) # Am I gonna need multiple threads?
    # pool.apply_async(w.execute)
    app.run()
    scheduler.shutdown()