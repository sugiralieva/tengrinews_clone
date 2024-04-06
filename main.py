from base64 import b64encode
from flask import Flask
from flask import render_template, g
import sqlite3 as sq
import os
from articles_db import ArticlesDB


SECRET_KEY = 'fdgdfgdfggf786hfg6hfg6h7f'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)

app.config['DEBUG'] = True
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'instance/articles_tengrinews.db')))


def connect_db():
    conn = sq.connect(app.config['DATABASE'])
    conn.row_factory = sq.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = ArticlesDB(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')

@app.route('/article', methods=['GET', 'POST'])
def article():

    return render_template('article.html')


if __name__ == '__main__':
    app.run()