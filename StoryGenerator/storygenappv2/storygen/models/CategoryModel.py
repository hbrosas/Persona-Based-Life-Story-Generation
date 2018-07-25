from storygenappv2.storygen.dbconnection.DatabaseConnection import DatabaseConnection
from storygenappv2.storygen.objects.Category import Category
import csv

class CategoryModel:

    def getCategoryByUserPref(self, user_pref):
        """

        :param user_pref:
        :returns the categories by specific user preference:
        """
        db = DatabaseConnection()
        conn = db.getconnection()

        try:
            with conn.cursor() as cursor:
                sql = "SELECT level1, level2, level3, level4 FROM category WHERE user_pref = " + user_pref
                cursor.execute(sql)
                row = cursor.fetchone()
                categories = []

                while row is not None:
                    # print("getCategoryByUserPref " + str(row))
                    category = Category(user_pref, level1=row['level1'], level2=row['level2'], level3=row['level3'], level4=row['level4'])
                    categories.append(category)
                    row = cursor.fetchone()
        finally:
            conn.close()

        return categories

    def checkIfContainsCategory(self, pref_type, user_pref):
        """
        checks if the type parameter of the assertion contains one of the categories

        :param pref_type type parameter of the assertion:
        :param user_pref:
        :returns if it contains the category (true or false) and Category object containing the three-level category:
        """
        db = DatabaseConnection()
        conn = db.getconnection()
        isContain = False
        category = None

        try:
            with conn.cursor() as cursor:
                sql = "SELECT level1, level2, level3 FROM categories " \
                      "WHERE user_pref = '" + user_pref + "' AND " \
                      "(level1 = '" + pref_type + "' OR level2 = '" + pref_type + "' OR level3 = '" + pref_type + "') "
                cursor.execute(sql)
                row = cursor.fetchone()

                if row is not None:
                    isContain = True
                    category = Category(row['level1'], row['level2'], row['level3'])
        finally:
            conn.close()

        return [isContain, category]
