import os
import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime, timedelta
import sqlite3 as sq

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}

list_article_urls = []

db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'tengrinews.db')
images_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'img', 'images_articles')

class UpdateArticles:
    def create_table_articles(self):
        with sq.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT(256),
    article_text TEXT,
    publication_date TIMESTAMP,
    image TEXT)
    ''')

    def insert_data_to_table_articles(self, title, article_text, publication_date, image):
        with sq.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO articles (title, article_text, publication_date, image) VALUES(?, ?, ?, ?)', (title, article_text, publication_date, image))

    def download(self, url):
        resp = requests.get(url, stream=True)
        r = open(images_path + '\\' + url.split("/")[-1], "wb")

        for value in resp.iter_content(1024*1024):
            r.write(value)
        r.close()

    def convert_date_from_str_to_datetime(self, publication_date):
        days = {'января': '01',
                'февраля': '02',
                'марта': '03',
                'апреля': '04',
                'мая': '05',
                'июня': '06',
                'июля': '07',
                'августа': '08',
                'сентября': '09',
                'октября': '10',
                'ноября': '11',
                'декабря': '12'}

        for key, value in days.items():
            if key in publication_date:
                publication_date = publication_date.replace(key, value)
                publication_date = publication_date.replace(' ', '-', 2)

        if 'Вчера' in publication_date:
            publication_date = publication_date.replace('Вчера', str(datetime.today().date() - timedelta(days=1)))
            publication_date = datetime.strptime(publication_date, "%Y-%m-%d %H:%M")
            publication_date = publication_date.strftime("%d-%m-%Y %H:%M")
        elif 'Сегодня' in publication_date:
            publication_date = publication_date.replace('Сегодня', str(datetime.today().date() - timedelta(days=1)))
            publication_date = datetime.strptime(publication_date, "%Y-%m-%d %H:%M")
            publication_date = publication_date.strftime("%d-%m-%Y %H:%M")

        publication_date = datetime.strptime(publication_date, "%d-%m-%Y %H:%M")
        return publication_date

    def parse_articles_urls(self):
        for page in range(1, 3):
            sleep(1)
            url = f'https://tengrinews.kz/article/page/{page}/'

            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            data = soup.find_all('div', class_="content_main_item")

            for i in data:
                article_url = "https://tengrinews.kz" + i.find("a").get("href")
                list_article_urls.append(article_url)
        return list_article_urls

    def parse_articles_pages(self, list_article_urls):
        for article_url in list_article_urls:
            response = requests.get(article_url)
            soup = BeautifulSoup(response.text, "lxml")
            data = soup.find("section", class_="first")
            title = data.find("h1", class_="head-single").text
            time_ = data.find("div", class_="date-time").text
            time_ = self.convert_date_from_str_to_datetime(time_)
            article_text = data.find("div", class_="content_main_text")
            article_text = str(article_text)
            try:
                picture = data.find("picture", class_="content_main_thumb_img")
                url_img = "https://tengrinews.kz" + picture.find("img").get("src")
                img_name = url_img.split("/")[-1]
            except AttributeError:
                video = data.find("video", playsinline="playsinline")
                url_img = "https://tengrinews.kz" + video.find("source").get("src")
                img_name = url_img.split("/")[-1]

            d = (datetime.today().date()).strftime("%Y-%m-%d %H:%M")
            time_ = time_.strftime("%Y-%m-%d %H:%M")

            if time_ >= d: # сравниваем даты, если дата сегодня, записываем в БД
                self.download(url_img)
                self.create_table_articles()
                self.insert_data_to_table_articles(title, article_text, time_, img_name)
