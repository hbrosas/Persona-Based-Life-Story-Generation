from dbobjects.DirectAssertion import DirectAssertion
from dbobjects.AssertionType import AssertionType
from dbobjects.LikedPagesAndEvents import LikedPagesAndEvents
from dbconnection.DatabaseConnection import DatabaseConnection
import csv


class AssertionModel:

    def getAssertionByUserPreference(self, user_pref):
        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT A.user_pref, AST.type, A.parameters FROM assertions A LEFT JOIN assertions_types AST ON A.assertion_type = AST.type_id WHERE A.user_pref = '" + user_pref + "' ORDER BY A.assertion_type"
                cursor.execute(sql)
                row = cursor.fetchone()
                directassertion = []

                while row is not None:
                    # print("getAssertionByUserPreference " + str(row))
                    userpref = row['user_pref']
                    assertiontype = row['type']
                    parameters = row['parameters']
                    assertion = DirectAssertion(userpref, assertiontype, parameters)
                    directassertion.append(assertion)
                    row = cursor.fetchone()
        finally:
            conn.close()

        return directassertion

    def getLikedPagesAndEvents(self):
        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT AST.type, A.parameters FROM assertions A LEFT JOIN assertions_types AST ON A.assertion_type = AST.type_id WHERE AST.type LIKE 'likes' OR AST.type LIKE 'event'"
                cursor.execute(sql)
                row = cursor.fetchone()
                likeseventslist = []

                while row is not None:
                    # print("getLikedPagesAndEvents " + str(row))
                    type = row['type']
                    parameters = row['parameters']
                    likesevents = LikedPagesAndEvents(type, parameters)
                    likeseventslist.append(likesevents)
                    row = cursor.fetchone()
        finally:
            conn.close()

        return likeseventslist

    def getAssertionType(self, assertiontype):
        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM assertions_types WHERE type = '" + assertiontype + "'"
                cursor.execute(sql)
                row = cursor.fetchone()

                #print("getAssertionType " + str(row))
                userpref = row['user_pref']
                assertiontype = row['type']
                parameters = row['parameter']
                assertiontype = AssertionType(userpref, assertiontype, parameters)

        finally:
            conn.close()

        return assertiontype

    def addAssertion(self, user_pref, assertion_type, parameters):
        db = DatabaseConnection()
        conn = db.getconnection()

        # print(parameters)

        type_id = self.getAssertionTypeID(self=self, assertion_type=assertion_type)
        try:
            with conn.cursor() as cursor:
                # sql = "INSERT INTO assertions(user_pref, assertion_type, parameters) VALUES(" + user_pref + ", " + str(type_id) + ", " + parameters + ")"
                sql = "INSERT INTO assertions(user_pref, assertion_type, parameters) VALUES(%s, %s, %s)"
                data = (user_pref, type_id, parameters)
                cursor.execute(sql, data)
                # cursor.execute(sql)
                conn.commit()
        finally:
            conn.close()

    def getAssertionTypeID(self, assertion_type):
        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT type_id FROM assertions_types WHERE type = '" + assertion_type + "'"
                cursor.execute(sql)
                row = cursor.fetchone()
                type_id = row['type_id']

        finally:
            conn.close()

        return type_id

    def createAssertionTable(self):
        db = DatabaseConnection()
        conn = db.getconnection()

        dbname = db.getdatabasename()

        try:
            cursor = conn.cursor()
            sql = "CREATE TABLE `" + dbname + "`.`assertions` ( " \
                  "`id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '', " \
                  "`user_pref` VARCHAR(45) NULL COMMENT '', " \
                  "`assertion_type` INT(11) NULL COMMENT '', " \
                  "`parameters` LONGTEXT NULL COMMENT '', " \
                  "PRIMARY KEY (`id`)  COMMENT '', " \
                  "UNIQUE INDEX `id_UNIQUE` (`id` ASC)  COMMENT '')"

            cursor.execute(sql)

        finally:
            conn.close()

    def createAssertionTypesTable(self):
        db = DatabaseConnection()
        conn = db.getconnection()

        dbname = db.getdatabasename()

        try:
            cursor = conn.cursor()
            sql = "CREATE TABLE `" + dbname + "`.`assertions_types` (" \
                  "`type_id` int(11) NOT NULL AUTO_INCREMENT, " \
                  "`user_pref` varchar(45) DEFAULT NULL, " \
                  "`type` varchar(100) DEFAULT NULL, " \
                  "`parameter` varchar(100) DEFAULT NULL, " \
                  "PRIMARY KEY (`type_id`), " \
                  "UNIQUE KEY `type_id_UNIQUE` (`type_id`))"

            cursor.execute(sql)

        finally:
            conn.close()

        # self.insertAssertionTypes(self=self)

    def insertAssertionTypes(self):
        db = DatabaseConnection()
        conn = db.getconnection()

        with open('C:\\Users\\denis_000\\PycharmProjects\\storygen\\assertions_types.csv') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # print(row['type_id'], row['user_pref'], row['type'], row['parameter'])
                sql = "INSERT INTO `assertions_types`(`type_id`, `user_pref`, `type`, `parameter`) VALUES(%s, %s, %s, %s)"
                cursor = conn.cursor()
                cursor.executemany(sql, [(row['type_id'], row['user_pref'], row['type'], row['parameter'])])
                conn.escape_string(sql)
                conn.commit()
