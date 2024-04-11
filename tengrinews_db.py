import sqlite3 as sq


class ArticlesDB:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

    def get_news_for_main(self):
        try:
            self.cursor.execute('SELECT id, title, image, publication_date FROM news ORDER BY publication_date DESC LIMIT 4')
            res = self.cursor.fetchall()
            return res
        except sq.Error as e:
            print('Ошибка получения новостей' + str(e))
        return False

    def get_articles_for_main(self):
        try:
            self.cursor.execute('SELECT id, title, image, publication_date FROM articles ORDER BY publication_date DESC LIMIT 4')
            res = self.cursor.fetchall()
            return res
        except sq.Error as e:
            print('Ошибка получения книг по категории' + str(e))
        return False

    def get_kazakhstan_future_news_for_main(self):
        try:
            self.cursor.execute('SELECT id, title, image, publication_date FROM kazakhstan_future ORDER BY publication_date DESC LIMIT 4')
            res = self.cursor.fetchall()
            return res
        except sq.Error as e:
            print('Ошибка получения новостей из категории Что будет с Казахстаном?' + str(e))
        return False

    def get_search_result(self, search_data):
        try:
            self.cursor.execute(f'''
SELECT id, title, image, publication_date
FROM news
WHERE title LIKE '%{search_data}%' OR news_text LIKE '%{search_data}%'
''')
            res = self.cursor.fetchall()
            return res
        except sq.Error as e:
            print('Ошибка получения новостей из категории Что будет с Казахстаном?' + str(e))
        return False

    def get_news_asc(self):
        try:
            self.cursor.execute('SELECT id, title, image, publication_date FROM news ORDER BY publication_date DESC')
            res = self.cursor.fetchall()
            return res
        except sq.Error as e:
            print('Ошибка получения новостей' + str(e))
        return False

    def get_news_desc(self):
        try:
            self.cursor.execute('SELECT id, title, image, publication_date FROM news ORDER BY publication_date ASC')
            res = self.cursor.fetchall()
            return res
        except sq.Error as e:
            print('Ошибка получения новостей' + str(e))
        return False

    def get_full_news(self, news_id):
        try:
            self.cursor.execute('SELECT title, news_text, publication_date, image FROM news WHERE id=?', (news_id,))
            res = self.cursor.fetchone()
            return res
        except sq.Error as e:
            print('Ошибка получения новости' + str(e))
        return False

    def get_articles_asc(self):
        try:
            self.cursor.execute('SELECT id, title, image, publication_date FROM articles ORDER BY publication_date DESC')
            res = self.cursor.fetchall()
            return res
        except sq.Error as e:
            print('Ошибка получения книг по категории' + str(e))
        return False

    def get_articles_desc(self):
        try:
            self.cursor.execute('SELECT id, title, image, publication_date FROM articles ORDER BY publication_date ASC')
            res = self.cursor.fetchall()
            return res
        except sq.Error as e:
            print('Ошибка получения книг по категории' + str(e))
        return False

    def get_full_article(self, article_id):
        try:
            self.cursor.execute('SELECT title, article_text, publication_date, image FROM articles WHERE id=?', (article_id,))
            res = self.cursor.fetchone()
            return res
        except sq.Error as e:
            print('Ошибка получения книг по категории' + str(e))
        return False

    def get_kazakhstan_future_asc(self):
        try:
            self.cursor.execute('SELECT id, title, image, publication_date FROM kazakhstan_future ORDER BY publication_date DESC')
            res = self.cursor.fetchall()
            return res
        except sq.Error as e:
            print('Ошибка получения новостей из категории Что будет с Казахстаном?' + str(e))
        return False

    def get_kazakhstan_future_desc(self):
        try:
            self.cursor.execute('SELECT id, title, image, publication_date FROM kazakhstan_future ORDER BY publication_date ASC')
            res = self.cursor.fetchall()
            return res
        except sq.Error as e:
            print('Ошибка получения новостей из категории Что будет с Казахстаном?' + str(e))
        return False

    def get_full_kazakhstan_future_news(self, news_id):
        try:
            self.cursor.execute('SELECT title, news_text, publication_date, image FROM kazakhstan_future WHERE id=?', (news_id,))
            res = self.cursor.fetchone()
            return res
        except sq.Error as e:
            print('Ошибка получения новости из категории Что будет с Казахстаном?' + str(e))
        return False
