
import mysql.connector
from exceptions.custom_exceptions import DatabaseConnectionException

class DBConnUtil:
    @staticmethod
    def get_db_connection():
        try:
            connection = mysql.connector.connect(
                host="local host",
                database="payxpert",
                user="root",
                password="root"
            )
            return connection
        except mysql.connector.Error as e:
            raise DatabaseConnectionException("Failed to connect to database")
