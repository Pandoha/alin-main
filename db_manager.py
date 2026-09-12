# db_manager.py
# This file manages all interactions with the database using a class-based approach.

from datetime import datetime
import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Establish connection to the database"""
        if self.database:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        else:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
    
    def reconnect(self, database=None):
        if self.conn and self.conn.is_connected():
            self.conn.close()
        if database:
            self.database = database
        self._connect()
    
    def show_databases(self):
        cursor = self.conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor]
        cursor.close()
        return databases
    
    def create_database(self, db_name):
        if db_name not in self.show_databases():
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE DATABASE `{db_name}`")
            cursor.close()
            print(f"Database {db_name} created successfully.")
    
    def show_tables(self):
        if not self.database:
            raise ValueError("No database selected.")
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor]
        cursor.close()
        return tables
    
    def create_table(self, table_name, params):
        if not self.database:
            raise ValueError("No database selected.")
        tables = self.show_tables()
        if table_name not in tables:
            cursor = self.conn.cursor()
            query = f"CREATE TABLE `{table_name}` {params}"
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
            print(f"Table {table_name} created successfully.")
    
    def delete_table(self, table_name):
        if not self.database:
            raise ValueError("No database selected.")
        tables = self.show_tables()
        if table_name in tables:
            cursor = self.conn.cursor()
            cursor.execute(f"DROP TABLE `{table_name}`")
            self.conn.commit()
            cursor.close()
            print(f"Table {table_name} deleted successfully.")

    def insert_row(self, table_name, column_names, column_types, column_values):
        """
        Insert a row safely using Parameterized Queries (SQL Injection Prevention)
        """
        if not self.database:
            raise ValueError("No database selected.")
        tables = self.show_tables()
        if table_name in tables:
            cursor = self.conn.cursor()
            query = f"INSERT INTO `{table_name}` {column_names} VALUES {column_types}"
            cursor.execute(query, column_values)
            self.conn.commit()
            cursor.close()
            print(f"Row inserted into table {table_name} successfully.")

    def delete_row(self, table_name, column_name, column_value):
        """
        Delete a row safely without string concatenation
        """
        if not self.database:
            raise ValueError("No database selected.")
        tables = self.show_tables()
        if table_name in tables:
            cursor = self.conn.cursor()
            query = f"DELETE FROM `{table_name}` WHERE `{column_name}` = %s"
            cursor.execute(query, (column_value,))
            self.conn.commit()
            cursor.close()
            print(f"Row deleted from table {table_name} successfully.")

    def get_all_rows(self, table_name):
        if not self.database:
            raise ValueError("No database selected.")
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM `{table_name}`")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_rows_with_value(self, table_name, column_name, column_value):
        """
        Get rows safely using prepared statements (%s)
        """
        if not self.database:
            raise ValueError("No database selected.")
        tables = self.show_tables()
        if table_name in tables:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM `{table_name}` WHERE `{column_name}` = %s"
            cursor.execute(query, (column_value,))
            rows = cursor.fetchall()
            cursor.close()
            return rows
        return []

    def update_row(self, table_name, primary_key_column, primary_key_value, column_names, column_values):
        """
        Update rows safely using Parameterized Queries
        """
        if not self.database:
            raise ValueError("No database selected.")
        tables = self.show_tables()
        if table_name in tables:
            cursor = self.conn.cursor()
            set_clause = ", ".join(f"`{col}` = %s" for col in column_names)
            query = f"UPDATE `{table_name}` SET {set_clause} WHERE `{primary_key_column}` = %s"
            values = list(column_values) + [primary_key_value]
            cursor.execute(query, values)
            self.conn.commit()
            cursor.close()
            print(f"Row in table {table_name} updated successfully.")

    def insert_decrypted_media(self, user_id, media_type_id, path):
        if not self.database:
            raise ValueError("No database selected.")
        tables = self.show_tables()
        if "decrypted_media" in tables:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO decrypted_media (user_id, media_type_id, path_to_decrypted_media)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (user_id, media_type_id, path))
            self.conn.commit()
            cursor.close()
            print(f"Media record inserted: User ID={user_id}, Media Type={media_type_id}, Path={path}")

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            self.conn = None
            print("Database connection closed.")