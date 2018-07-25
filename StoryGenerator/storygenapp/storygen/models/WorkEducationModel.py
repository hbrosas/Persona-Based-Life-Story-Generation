from storygenapp.storygen.dbconnection.DatabaseConnection import DatabaseConnection
from storygenapp.storygen.dbobjects.WorkAndEducation import WorkAndEducation

class WorkEducationModel:

    def getWorkAndEducation(self):
        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = 'SELECT * FROM work_and_education'
                cursor.execute(sql)
                row = cursor.fetchone()
                workandeducation = []

                while row is not None:
                    print(row)
                    organization = row['organization']
                    type = row['type']
                    yearstarted = row['yearstarted']
                    yearended = row['yearended']
                    # location = row['location']
                    courseorposition = row['courseorposition']
                    workanded = WorkAndEducation(organization, type, yearstarted, yearended, courseorposition)
                    workandeducation.append(workanded)
                    row = cursor.fetchone()
        finally:
            conn.close()

        return workandeducation

    def getSpecificWork(self):
        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM work_and_education WHERE type = 'Work'"
                cursor.execute(sql)
                row = cursor.fetchone()
                workList = []

                while row is not None:
                    organization = row['organization']
                    type = row['type']
                    yearstarted = row['yearstarted']
                    yearended = row['yearended']
                    courseorposition = row['courseorposition']
                    work = WorkAndEducation(organization, type, yearstarted, yearended, courseorposition)
                    workList.append(work)
                    row = cursor.fetchone()
        finally:
            conn.close()

        return workList

    def getSpecificEducation(self):
        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM work_and_education WHERE type != 'Work'"
                cursor.execute(sql)
                row = cursor.fetchone()
                educationList = []

                while row is not None:
                    organization = row['organization']
                    type = row['type']
                    yearstarted = row['yearstarted']
                    yearended = row['yearended']
                    courseorposition = row['courseorposition']
                    education = WorkAndEducation(organization, type, yearstarted, yearended, courseorposition)
                    educationList.append(education)
                    row = cursor.fetchone()
        finally:
            conn.close()

        return educationList