import sqlite3 as sq


class ArticlesDB:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()