import mysql.connector

class DB:
    def __init__(self, host, user, passwd, port, db_name=None):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db_name = db_name
        self.cursor = None

    def db_info(self):
        print(f"Connect to MySQL server at {self.db.server_host}")
        print(f"Database: {self.db_name}")
        print(f"Server version: {self.db.get_server_info()}")
        print(f"Protocol version: {self.db._protocol_version}")
        print(f"Server connection: {self.db.connection_id}")
        print(f"Server charset: {self.db.charset}")
        print(f"Server time zone: {self.db.time_zone}")

    def set_db_name(self, db_name):
        self.db_name = db_name

    def set_cursor_buffered_true(self):
        self.cursor = self.db.cursor(buffered=True)

    # Connect to the database
    def connect(self):
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            port=self.port,
            database=self.db_name
        )
        self.cursor = self.db.cursor()

        if self.db.is_connected():
            print("Connected to the database")
        else:
            print("Failed to connect to the database")

    def buffered_connect(self):
        self.connect()
        self.set_cursor_buffered_true()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()
    
    def close(self):
        self.db.close()

    # Execute a query
    def execute(self, operation, params=None, multi=False):
        return self.cursor.execute(operation, params, multi)

    def fetchall(self):
        return self.cursor.fetchall()

    def create_table(self, table_name, columns, primary_key=None, foreign_key=None):
        self.execute(f"CREATE TABLE {table_name} ({columns}) PRIMARY KEY ({primary_key}), FOREIGN KEY ({foreign_key})")
        self.commit()
    
    def drop_table(self, table_name):
        self.execute(f"DROP TABLE {table_name}")
        self.commit()
    
    def select(self, table_name, columns, condition=None):
        if condition:
            self.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}")
        else:
            self.execute(f"SELECT {columns} FROM {table_name}")
        return self.fetchall()
    
    def update(self, table_name, set_values, condition):
        self.execute(f"UPDATE {table_name} SET {set_values} WHERE {condition}")
        self.commit()

    def insert(self, table_name, columns, values):
        self.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
        self.commit()

    def delete(self, table_name, condition):
        self.execute(f"DELETE FROM {table_name} WHERE {condition}")
        self.commit()

