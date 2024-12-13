import mysql.connector
from mysql.connector import Error


class MyConnection:

    @staticmethod
    def get_connection():
        con = None
        try:
            # Establish the connection
            con = mysql.connector.connect(
                host='localhost',
                database='appuser',
                user='root',
                password='041423'
            )
            if con.is_connected():
                print("Connection successful!")
            else:
                print("Failed to connect to the database.")
        except Error as e:
            print(f"Error: {e}")
        return con


if __name__ == "__main__":
    connection = MyConnection.get_connection()
    if connection is not None and connection.is_connected():
        connection.close()
