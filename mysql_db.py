import MySQLdb
import os

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']


class MySQL_Database:
    _db_conn = None
    _db_cursor = None

    # Constructor for database connection
    def __init__(self):

        # Create Database connection and cursor
        try:
            self._db_conn = MySQLdb.connect(host=DB_HOST, port=3306, user=DB_USER, passwd=DB_PASSWORD, database=DB_NAME)
            self._db_cursor = self._db_conn.cursor(MySQLdb.cursors.DictCursor)
            print("Database configured and initialised")
        except MySQLdb.Error as e:
            print("Connection/cursor error on initialization")
            print(e.args)
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))

    # Query method with parameters
    def query(self, sql, parameters):
        try:
            self._db_cursor.execute(sql, parameters)
            print("Query completed")
            return self._db_cursor.fetchall()

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            return None
        finally:
            self._db_conn.close()
            print("Connection closed")

    # Insertion method with parameters
    def insert(self, sql, parameters):
        try:
            result = self._db_cursor.execute(sql, parameters)
            self._db_conn.commit()
            print("Insertion completed")
            return result
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print("Insertion error")
            print(e)
            self._db_conn.rollback()
            return None
        finally:
            self._db_conn.close()
            print("Connection closed")

    # Insertion method with parameters
    def update(self, sql, parameters):
        try:
            result = self._db_cursor.execute(sql, parameters)
            self._db_conn.commit()
            print("Update completed")
            return result
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print("Update error")
            print(e)
            self._db_conn.rollback()
            return None
        finally:
            self._db_conn.close()
            print("Connection closed")

    # Method to check DB connection status
    def check_connection(self):
        print(self._db_conn)

