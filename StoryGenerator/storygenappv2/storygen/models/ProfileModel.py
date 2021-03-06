from storygenappv2.storygen.dbconnection.DatabaseConnection import DatabaseConnection
from storygenappv2.storygen.dbobjects.DirectKnowledge import DirectKnowledge


class ProfileModel:

    def getprofile(self):
        """

        :returns a list containing the profile information of the user:
        """
        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = 'SELECT * FROM profile'
                cursor.execute(sql)
                row = cursor.fetchone()
                field_names = [i[0] for i in cursor.description]
                dklist = []

                print(field_names)

                for fn in field_names:
                    data = row[fn]
                    type = fn

                    dk = DirectKnowledge(data, type)
                    dklist.append(dk)


        finally:
            conn.close()

        return dklist

    def getspecificdirectknowledge(self, type):
        """

        :param type information needed in the user's profile:
        :returns a specific information in the user's profile:
        """
        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT " + type +" FROM profile"
                cursor.execute(sql)
                row = cursor.fetchone()

                data = row[type]
        finally:
            conn.close()

        return data

