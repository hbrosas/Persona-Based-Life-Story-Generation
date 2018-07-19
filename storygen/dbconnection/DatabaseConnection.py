import pymysql


class DatabaseConnection:
    host = 'localhost'
    username = 'root'
    password = 'root'
    database = 'data_sample'

    def getconnection(self):
        return pymysql.connect(host='localhost', user='root', password='root', database='data_sample', charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor, autocommit=True)

    def getdatabasename(self):
        return "data_sample"
