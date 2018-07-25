import pymysql


class DatabaseConnection:
    host = 'localhost'
    username = 'root'
    password = 'root'
    database = 'story_db'

    def getconnection(self):
        """

        :returns the database connection:
        """
        return pymysql.connect(host='localhost', user='root', password='root', database='foodie_sampledb_v2', charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor, autocommit=True)

    def getdatabasename(self):
        """

        :returns the database name:
        """
        return "story_db"
