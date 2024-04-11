from flask import Flask
from flask import render_template, g, request, redirect, session
import sqlite3 as sq
import os
from tengrinews_db import ArticlesDB
import schedule
import time
import threading
from parsing.parse_news_tengrinews import UpdateNews
from parsing.parse_articles_tengrinews import UpdateArticles
from parsing.parse_Kazakhstan_future_tengrinews import UpdateKazakhstanNews


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


db_lock = threading.Lock()

def update_db():
    with db_lock:
        url_news = UpdateNews()
        urls_pages_news = url_news.parse_news_urls()
        url_news.parse_news_pages(urls_pages_news)
        print('done news')

        url_articles = UpdateArticles()
        urls_pages_articles = url_articles.parse_articles_urls()
        url_articles.parse_articles_pages(urls_pages_articles)
        print('done articles')

        url_kaz = UpdateKazakhstanNews()
        url_pages_kaz = url_kaz.parse_kazakhstan_news_urls()
        url_kaz.parse_kazakhstan_news_pages(url_pages_kaz)
        print('done kaz news')


def scheduled_task():
    schedule.every(1).day.do(update_db)

    while True:
        schedule.run_pending()
        time.sleep(1)


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
    news_main = dbase.get_news_for_main()
    articles_main = dbase.get_articles_for_main()
    kazakhstan_future_news_for_main = dbase.get_kazakhstan_future_news_for_main()

    return render_template('index.html', news_main=news_main, articles_main=articles_main, kazakhstan_future_news_for_main=kazakhstan_future_news_for_main)


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query')
    search_result = dbase.get_search_result(query)

    return render_template('search.html', news=news, search_result=search_result, query=query)


@app.route('/news', methods=['GET'])
def news():
    sort_by = request.args.get('sort_by')
    if sort_by:
        session['sort_by'] = sort_by  # Сохраняем выбор пользователя в сессии
    else:
        sort_by = session.get('sort_by', 'date_asc')

    if sort_by == 'date_asc':
        news = dbase.get_news_asc()
    elif sort_by == 'date_desc':
        news = dbase.get_news_desc()
    else:
        news = dbase.get_news_asc()

    page = request.args.get('page', 1, type=int)
    per_page = 12
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(news) + per_page -1) // per_page

    items_on_page = news[start:end]

    return render_template('news.html', news=news, page=page, total_pages=total_pages, items_on_page=items_on_page, sort_by=sort_by)


@app.route('/new/<int:new_id>', methods=['GET', 'POST'])
def new(new_id):
    full_news = dbase.get_full_news(new_id)

    return render_template('new.html', full_news=full_news)


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    sort_by = request.args.get('sort_by')
    if sort_by:
        session['sort_by'] = sort_by  # Сохраняем выбор пользователя в сессии
    else:
        sort_by = session.get('sort_by', 'date_asc')

    if sort_by == 'date_asc':
        articles = dbase.get_articles_asc()
    elif sort_by == 'date_desc':
        articles = dbase.get_articles_desc()
    else:
        articles = dbase.get_articles_asc()

    page = request.args.get('page', 1, type=int)
    per_page = 12
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(articles) + per_page - 1) // per_page

    items_on_page = articles[start:end]

    return render_template('articles.html', articles=articles, page=page, total_pages=total_pages, items_on_page=items_on_page, sort_by=sort_by)


@app.route('/article/<int:article_id>', methods=['GET', 'POST'])
def article(article_id):
    full_article = dbase.get_full_article(article_id)

    return render_template('article.html', full_article=full_article)


@app.route('/kazakhstan_future', methods=['GET', 'POST'])
def kazakhstan_future_news():
    sort_by = request.args.get('sort_by')
    if sort_by:
        session['sort_by'] = sort_by  # Сохраняем выбор пользователя в сессии
    else:
        sort_by = session.get('sort_by', 'date_asc')

    if sort_by == 'date_asc':
        kazakhstan_news = dbase.get_kazakhstan_future_asc()
    elif sort_by == 'date_desc':
        kazakhstan_news = dbase.get_kazakhstan_future_desc()
    else:
        kazakhstan_news = dbase.get_kazakhstan_future_asc()

    page = request.args.get('page', 1, type=int)
    per_page = 12
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(kazakhstan_news) + per_page - 1) // per_page

    items_on_page = kazakhstan_news[start:end]

    return render_template('kazakhstan_future.html', kazakhstan_news=kazakhstan_news, page=page, total_pages=total_pages, items_on_page=items_on_page, sort_by=sort_by)


@app.route('/kazakhstan_future_new/<int:kazakhstan_news_id>', methods=['GET', 'POST'])
def kazakhstan_future_new(kazakhstan_news_id):
    kazakhstan_new = dbase.get_full_kazakhstan_future_news(kazakhstan_news_id)

    return render_template('kazakhstan_future_news.html', kazakhstan_new=kazakhstan_new)


update_thread = threading.Thread(target=scheduled_task)
update_thread.start()


if __name__ == '__main__':
    app.run(use_reloader=False)
