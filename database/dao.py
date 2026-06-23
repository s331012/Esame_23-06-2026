from xml.sax.saxutils import prepare_input_source

from flet.core import row
from mysql.connector import cursor
from networkx.algorithms.approximation.ramsey import ramsey_R2

from database.DB_connect import DBConnect
from model.user import User

class Dao:
    def __init__(self):
        pass

    @staticmethod
    def read_all_users():
        print("Executing read from database using SQL query")

        results = []
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ SELECT * FROM Users """

        cursor.execute(query)

        for row in cursor:
            user = User(
                row["user_id"],
                row["votes_funny"],
                row["votes_useful"],
                row["votes_cool"],
                row["name"],
                row["average_stars"],
                row["review_count"]
            )

            results.append(user)

        cursor.close()
        cnx.close()

        return results

    @staticmethod
    def get_users_min_business(n_bus):

        results = []
        cnx = DBConnect.get_connection()

        if cnx is None:
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ SELECT u.user_id, u.votes_funny, u.votes_useful, u.votes_cool, u.name, u.average_stars, u.review_count
                    FROM Users u, Reviews r
                    WHERE u.user_id = r.user_id
                    GROUP BY u.user_id
                    HAVING COUNT(DISTINCT r.review_count) >= %s """

        cursor.execute((query, n_bus))
        for row in cursor:
            user = User(
            row["user_id"],
            row["votes_funny"],
                row["votes_useful"],
                row["votes_cool"],
                row["name"],
                row["average_stars"],
                row["review_count"]
        )
            results.append(user)

        cursor.close()
        cnx.close()

        return results

    @staticmethod
    def get_archi(id_map):
        results = []
        cnx = DBConnect.get_connection()

        if cnx is None:
            return None
        cursor = cnx.cursor(dictionary=True)


        query= """ SELECT r1.user_id AS u1, r2.user_id AS u2,
        COUNT(DISTINCT r1.business_id) AS peso 
            FROM Reviews r1, Reviews r2 
         WHERE r1.business_id= r2.business_id
        AND r1.user_id < r2.user_id
        GROUP BY r1.user_id, r2.user_id"""

        cursor.execute(query)

        for row in cursor:
            id1=row["u1"]
            id2=row["u2"]
            peso=row["peso"]
            if id1 in id_map and id2 in id_map:
                results.append((id_map[id1], id_map[id2], peso))
        cursor.close()
        cnx.close()

        return results