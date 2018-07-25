from storygenappv2.storygen.dbconnection.DatabaseConnection import DatabaseConnection
import csv, json
import csv, json
from storygenappv2.storygen.JSONHandler.JSONReader import JSONReader
from storygenappv2.storygen.models.AssertionModel import AssertionModel

def populate_categories(self):
    db = DatabaseConnection()
    conn = db.getconnection()

    cursor = conn.cursor()


    try:
        cursor.execute("DROP TABLE IF EXISTS categories")
    finally:
        sql = "CREATE TABLE categories ( " \
              "id  INT (11) NOT NULL AUTO_INCREMENT," \
              "user_pref  VARCHAR (45) NULL," \
              "level1 VARCHAR (100) NULL, " \
              "level2 VARCHAR (100) NULL," \
              "level3 VARCHAR (100) NULL," \
              "PRIMARY KEY (id))"

        cursor.execute(sql)

    with open('storygenappv2\\data\\Categories.csv', newline='') as csvfile:
        readcsv = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in readcsv:
            sql = "INSERT INTO categories(user_pref, level1, level2, level3) VALUES(%s, %s, %s, %s)"

            cursor.executemany(sql, [(row[0], row[1], row[2], row[3])])
            conn.escape_string(sql)
            conn.commit()
