from storygenappv2.storygen.dbobjects.DirectAssertion import DirectAssertion
from storygenappv2.storygen.dbobjects.AssertionType import AssertionType
from storygenappv2.storygen.dbobjects.LikedPagesAndEvents import LikedPagesAndEvents
from storygenappv2.storygen.dbconnection.DatabaseConnection import DatabaseConnection
import csv


class AssertionModel:

    def getAssertionByUserPreference(self, user_pref):
        """

        :param user_pref:
        :returns the assertions by user preference:
        """

        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT A.user_pref, AST.assertion_type, A.parameters FROM assertions A LEFT JOIN assertions_types AST ON A.assertion_type = AST.id WHERE A.user_pref = '" + user_pref + "' ORDER BY A.assertion_type"
                cursor.execute(sql)
                row = cursor.fetchone()
                directassertion = []

                while row is not None:
                    print("getAssertionByUserPreference " + str(row))
                    userpref = row['user_pref']
                    assertiontype = row['assertion_type']
                    parameters = row['parameters']
                    assertion = DirectAssertion(userpref, assertiontype, parameters)
                    directassertion.append(assertion)
                    row = cursor.fetchone()
        finally:
            conn.close()

        return directassertion

    def getLikedPagesAndEvents(self):
        """

        :returns list of LikedPagesAndEvents object:
        """

        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT AST.assertion_type, A.parameters FROM assertions A LEFT JOIN assertions_types AST ON A.assertion_type = AST.id WHERE AST.assertion_type LIKE 'likes' OR AST.assertion_type LIKE 'events'"
                cursor.execute(sql)
                row = cursor.fetchone()
                likeseventslist = []

                while row is not None:
                    # print("getLikedPagesAndEvents " + str(row))
                    type = row['assertion_type']
                    parameters = row['parameters']
                    likesevents = LikedPagesAndEvents(type, parameters)
                    likeseventslist.append(likesevents)
                    row = cursor.fetchone()
        finally:
            conn.close()

        return likeseventslist

    def getAssertionType(self, assertiontype, user_pref):
        """

        :param assertiontype:
        :param user_pref:
        :returns the assertion types of a specific user preference:
        """
        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM assertions_types WHERE assertion_type = '" + assertiontype + "' AND user_pref = '" + user_pref + "'"
                cursor.execute(sql)
                row = cursor.fetchone()

                #print("getAssertionType " + str(row))
                userpref = row['user_pref']
                assertiontype = row['assertion_type']
                parameters = row['parameter']
                assertiontype = AssertionType(userpref, assertiontype, parameters)

        finally:
            conn.close()

        return assertiontype

    def getAssertionTypeID(self, assertion_type, user_pref):
        """

        :param assertion_type:
        :param user_pref:
        :returns the id of the assertion type of a specific user preference:
        """

        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT id FROM assertions_types WHERE assertion_type = '" + assertion_type + "' AND user_pref = '" + user_pref + "'"
                cursor.execute(sql)
                row = cursor.fetchone()
                type_id = row['id']

        finally:
            conn.close()

        return type_id