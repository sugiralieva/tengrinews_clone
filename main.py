from flask import Flask
from flask import render_template, g
import sqlite3 as sq
import os
from tengrinews_db import ArticlesDB


SECRET_KEY = 'fdgdfgdfggf786hfg6hfg6h7f'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)

app.config['DEBUG'] = True
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'instance/tengrinews.db')))


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
    news = dbase.get_news_announcement()

    return render_template('index.html', news=news)


@app.route('/news/<int:news_id>', methods=['GET', 'POST'])
def news(news_id):
    full_news = dbase.get_full_news(news_id)

    return render_template('news.html', full_news=full_news)


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    articles = dbase.get_articles_announcement()

    return render_template('articles.html', articles=articles)


@app.route('/article/<int:article_id>', methods=['GET', 'POST'])
def article(article_id):
    full_article = dbase.get_full_article(article_id)

    return render_template('article.html', full_article=full_article)


@app.route('/kazakhstan_future', methods=['GET', 'POST'])
def kazakhstan_future_news():
    kazakhstan_news = dbase.get_kazakhstan_future_announcement()

    return render_template('kazakhstan_future.html', kazakhstan_news=kazakhstan_news)


@app.route('/kazakhstan_future_new/<int:kazakhstan_news_id>', methods=['GET', 'POST'])
def kazakhstan_future_new(kazakhstan_news_id):
    kazakhstan_new = dbase.get_full_kazakhstan_future_news(kazakhstan_news_id)

    return render_template('kazakhstan_future_news.html', kazakhstan_new=kazakhstan_new)


if __name__ == '__main__':
    app.run()