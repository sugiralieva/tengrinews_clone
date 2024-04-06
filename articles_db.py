import sqlite3 as sq


class ArticlesDB:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

    def get_articles_announcement(self):
        try:
            self.cursor.execute('SELECT id, title, image FROM articles')
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