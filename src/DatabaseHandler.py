from mysql.connector import connect, Error


class DatabaseHandler():
    def __init__(self):      
        self.connection = connect(
                host='astronaut.snu.ac.kr', 
                port=7000, 
                user='DB2023_11225', 
                password='DB2023_11225', 
                database='DB2023_11225',
                charset='utf8'
            )

        self.cursor = self.connection.cursor()
        
        if self.connection.is_connected():
                print("connected")
    
    
    
    def initialization_database(self):
        create_dvd_table = """
        CREATE TABLE DVDS (
            d_id                INT         AUTO_INCREMENT  PRIMARY KEY,
            title               VARCHAR(50) NOT NULL,
            director            VARCHAR(40) NOT NULL,
            available_copies    INT         DEFAULT 2,
            total_rentals       INT         DEFAULT 0
        );
        """
        
        
        create_user_table = """
        CREATE TABLE USERS (
            id                  INT         AUTO_INCREMENT  PRIMARY KEY,
            name                VARCHAR(30) NOT NULL,
            age                 INT         NOT NULL,
            total_rentals       INT         DEFAULT 0,
            average_rating      FLOAT       DEFAULT NULL
        );
        """
        
        
        
        create_ratings_table = """
        CREATE TABLE RATINGS (
            user_id INT,
            dvd_id INT,
            rating INT CHECK(rating BETWEEN 1 AND 5),
            PRIMARY KEY (user_id, dvd_id),
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (dvd_id) REFERENCES DVDs(id)
        );
        """
        
        self.cursor.execute("DROP TABLE IF EXISTS Ratings;")
        self.cursor.execute("DROP TABLE IF EXISTS Users;")
        self.cursor.execute("DROP TABLE IF EXISTS DVDs;")
        
        self.cursor.execute(create_dvd_table)
        self.cursor.execute(create_user_table)
        self.cursor.execute(create_ratings_table)
    
        self.connection.commit()
        
        
        
        

    def reset_database(self):
        """
        Resets the database by dropping all tables and recreating them.
        """
        drop_ratings_table = "DROP TABLE IF EXISTS Ratings;"
        drop_user_table = "DROP TABLE IF EXISTS Users;"
        drop_dvd_table = "DROP TABLE IF EXISTS DVDs;"
        self.cursor.execute(drop_ratings_table)
        self.cursor.execute(drop_user_table)
        self.cursor.execute(drop_dvd_table)
        self.connection.commit()
        self.create_tables()
        print("Database reset successfully.")

    def insert(self, table_name, data):
        """
        Inserts a row into a specified table.
        :param table_name: Name of the table.
        :param data: Dictionary of column-value pairs to insert.
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        values = tuple(data.values())
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print(f"Inserted into {table_name}: {data}")
        except Error as e:
            print(f"Insert error: {e}")

    def update(self, table_name, data, condition):
        """
        Updates rows in a specified table.
        :param table_name: Name of the table.
        :param data: Dictionary of column-value pairs to update.
        :param condition: SQL condition string for the WHERE clause.
        """
        set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        values = tuple(data.values())
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print(f"Updated {table_name}: {data} where {condition}")
        except Error as e:
            print(f"Update error: {e}")

    def delete(self, table_name, condition):
        """
        Deletes rows from a specified table.
        :param table_name: Name of the table.
        :param condition: SQL condition string for the WHERE clause.
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Deleted from {table_name} where {condition}")
        except Error as e:
            print(f"Delete error: {e}")

    def select(self, table_name, columns="*", condition=None):
        """
        Executes a SELECT query and returns the results.
        :param table_name: Name of the table.
        :param columns: Columns to select (default: all columns).
        :param condition: SQL condition string for the WHERE clause.
        """
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Select error: {e}")
            return None

    def close_connection(self):
        """
        Closes the database connection and cursor.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")