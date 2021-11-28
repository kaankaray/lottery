from flask import Flask

app = Flask(__name__)

print('')

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    print('PyCharm')
    app.run()

