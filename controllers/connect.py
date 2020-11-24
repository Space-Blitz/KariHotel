import psycopg2
import psycopg2.extras
from flask import jsonify, abort

import time

from models.constants import DATABASE_URL


class Database():
    """
    Handle database connections
    """
    
    def __init__(self):
        """
        initialise database connection
        """
        connection = psycopg2.connect(DATABASE_URL)
        connection.autocommit = True
        self.cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.create_tables()


    def create_tables(self):
        """
        Create necessary tables in database
        params:n/a
        returns:n/a
        """
        sql_command = """
            CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY,
                username VARCHAR (250) NOT NULL UNIQUE,
                email VARCHAR (250) NOT NULL UNIQUE,
                contact VARCHAR (250) NOT NULL,
                password VARCHAR (250) NOT NULL,
                date_created TIMESTAMP NOT NULL,
                admin BOOLEAN NOT NULL DEFAULT FALSE
            );
            CREATE TABLE IF NOT EXISTS parcels(
                parcel_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                parcel_description VARCHAR (50) NOT NULL,
                weight_kgs FLOAT NULL,
                price INT NULL,
                recipient VARCHAR (250) NOT NULL,
                recipient_contact VARCHAR (250) NOT NULL,
                pickup_location VARCHAR (250) NOT NULL,
                current_location VARCHAR (250) NULL,
                destination VARCHAR (250) NOT NULL,
                status varchar(25) check (status in ('pending', 'delivered', 'in transit', 'canceled')) DEFAULT 'pending',
                date_created TIMESTAMP,
                date_to_be_delivered TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS weight_categories(
                weight_id SERIAL PRIMARY KEY,
                weight_kgs NUMRANGE NOT NULL UNIQUE,
                price INT NOT NULL UNIQUE
            );
		"""
        self.cursor.execute(sql_command)
        self.insert_into_weight_categories()
        self.insert_admin_user()


    def insert_into_weight_categories(self):
        """
        insert default values into weight categories
        params:n/a
        returns:n/a
        """
        sql_command = """
        INSERT INTO weight_categories (price, weight_kgs)
        VALUES (2000,'[0, 0.1)'),
               (3000,'[0.1, 0.5)'),
               (6000,'[0.5, 1)'),
               (10000,'[1, 2)'),
               (15000,'[2, 5)'),
               (20000,'[5, 10)'),
               (25000,'[10, 20)'),
               (30000,'[20, 30)'),
               (40000,'[30, 50)'),
               (70000,'[50, 100)'),
               (100000,'[100, 200)'),
               (200000,'[200, 500)'),
               (700000,'[500, 1000)');
        """
        sql_command1="""
        SELECT EXISTS(SELECT TRUE FROM weight_categories WHERE price=3000);
        """
        self.populate_default_data(sql_command1,sql_command)
    
    def populate_default_data(self,sql_command1,sql_command2):
        """
        Enter Default data to database
        """
        table_empty = self.execute_query(sql_command1)
        if not table_empty[0]['exists']:
            self.cursor.execute(sql_command2)



    def insert_admin_user(self):
        """
        create an admin if non existent
        params:n/a
        returns:n/a
        """
        sql_command = """
        INSERT INTO users (username,email,contact,password,date_created,admin) 
        values ('Admin1','i-sendit@gmail.com','07888392838','doNot2114',now(),'t');
        INSERT INTO users (username,email,contact,password,date_created,admin) 
        values ('TestUser','meKendit@gmail.com','07888392838','ddwoNot2114',now(),'f');
        """
        sql_command1 = """
        SELECT EXISTS(SELECT TRUE FROM users where admin='true');
        """
        self.populate_default_data(sql_command1,sql_command)

    def execute_query(self, sql_command):
        """
        Execute query
        params: sql query statement
        returns: result
        """
        self.cursor.execute(sql_command)
        rows_returned = self.cursor.fetchall()

        return rows_returned

    def get_from_users(self, column, username):
        """
        Get column from users table
        params:column name, username
        returns:password
        """
        sql_command="""
        SELECT {column} FROM users where username='{username}';
        """.format(username=username, column=column)
        db_value = self.execute_query(sql_command)
        if not db_value:
            abort(400, description="Invalid username or password.")
        return db_value[0][column]
    

    # def create_usersaP

    def my_func(say):
        time.sleep(10)
        print("Process finished",say )

db = Database()