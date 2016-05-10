from flask import Flask, url_for, render_template, request
from models import Request, Result

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/tbell_route', methods=['POST'])
def result():
    # do stuff to get
    pass

if __name__ == '__main__':
    app.run(debug=True)
