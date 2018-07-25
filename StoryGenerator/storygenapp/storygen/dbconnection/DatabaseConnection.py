import pymysql


class DatabaseConnection:
    host = 'localhost'
    username = 'root'
    password = 'root'
    database = 'story_db'

    def getconnection(self):
        return pymysql.connect(host='localhost', user='root', password='root', database='foodie_sampledb', charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor, autocommit=True)

    def getdatabasename(self):
        return "story_db"
