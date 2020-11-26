import psycopg2
import psycopg2.extras
from flask import jsonify, abort
from flask_jwt_extended import create_access_token

from multiprocessing import Process
import datetime
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
                surname VARCHAR (250) NOT NULL,
                othernames VARCHAR (250) NOT NULL,
                email VARCHAR (250) NOT NULL UNIQUE,
                contact VARCHAR (250) NOT NULL UNIQUE,
                password VARCHAR (250) NOT NULL,
                date_created TIMESTAMP NULL,
                admin BOOLEAN NOT NULL DEFAULT FALSE,
                is_active BOOLEAN NOT NULL DEFAULT FALSE
            );
            CREATE TABLE IF NOT EXISTS bookings(
                booking_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                type_id FLOAT NOT NULL,
                type_name VARCHAR (50) NOT NULL,
                price INT NULL,
                rooms INT NOT NULL,
                total VARCHAR (250) NOT NULL,
                time TIMESTAMP NOT NULL,
                date_booked_for TIMESTAMP NOT NULL,
                payment_type varchar(25) check (payment_type in ('cash', 'bank transfer/visa')) DEFAULT 'pending',
                payment_status varchar(25) check (payment_status in ('pending', 'complete', 'canceled')) DEFAULT 'pending',
                payment_id VARCHAR (250) NULL,
                filled_status varchar(25) check (filled_status in ('pending', 'utilized', 'canceled')) DEFAULT 'pending'
            );
            CREATE TABLE IF NOT EXISTS room_categories(
                room_id SERIAL PRIMARY KEY,
                number INT NOT NULL,
                price INT NOT NULL,
                name VARCHAR (250) NOT NULL,
                time TIMESTAMP NOT NULL,
                description VARCHAR (250) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS payments(
                payment_id SERIAL PRIMARY KEY,
                time INT NOT NULL,
                amount INT NOT NULL
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
        INSERT INTO room_categories (number, price, name,  time, description)
        VALUES (40, 40000, 'Master Suite', now(), 'Spacious self contained room with double bed, Satelite TV, state of the art washrooms, 24/7 room service, breakfast included.'),
               (3, 60000, 'Presidential Suite', now(), 'Mini Gym within highly spacious self contained room with double bed, Satelite TV, state of the art washrooms, 24/7 room service, breakfast included.'),
               (200, 1000, 'Normal Suite', now(), 'Self contained room with single bed, Satelite TV, breakfast included.'),
               (100, 3000, 'Couple Suite', now(), 'Self contained room with double bed, Satelite TV, breakfast included.');
        """
        sql_command1="""
        SELECT EXISTS(SELECT TRUE FROM room_categories limit 1);
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
        INSERT INTO users (surname,othernames,email,contact,password,date_created,admin) 
        values ('Admin1','Saed','i-sendit@gmail.com','07888392838','doNot2114',now(),'t');
        INSERT INTO users (surname,othernames,email,contact,password,date_created,admin) 
        values ('Test','User','meKendit@gmail.com','0788892838','ddwoNot2114',now(),'f');
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

    def get_from_users(self, column, email, extra_params=''):
        """
        Get column from users table
        params:column name, username
        returns:password
        """
        sql_command="""
        SELECT {column} FROM users where email='{email}' {extra_params};
        """.format(email=email, column=column, extra_params=extra_params)
        db_value = self.execute_query(sql_command)
        if not db_value:
            abort(400, description="Invalid username or password.")
        return db_value[0]
    

    def validate_user_login(self,email,password):
        """
        Check if password password is equal to password in database
        """
        user = self.get_from_users('password,surname,email,contact,admin',email,"and password = '"+password+"'")
        access_token = create_access_token(
            identity={
            'surname':user.get('surname'),
            'email':user.get('email'),
            'contact':user.get('contact')
            },
            expires_delta=datetime.timedelta(days=40)
        )
        # print(db_password.get('password'))
        return access_token
    
    # select to_char(date_created::timestamp, 'DD Mon YYYY HH:MI:SSPM') from users
    def signup(self,email,password,surname, othernames, contact):
        """
        Check if password password is equal to password in database
        """
        insert_query="""
        INSERT INTO users (surname,othernames,email,contact,password,date_created,admin) 
        values ('{surname}','{othernames}','{email}','{contact}','{password}',now(),'f');\
        """.format(
            email=email,
            password=password,
            surname=surname,
            othernames=othernames,
            contact=contact
        )#sql query for inserting new users
        
        try:
            self.cursor.execute(insert_query)
            token = create_access_token(
            identity={
            'surname':surname,
            'email':email,
            'contact':contact,
            'activation':True
            },
            expires_delta=datetime.timedelta(days=4000)
            )
            return token
        except Exception as identifier:
            print(str(identifier))

            abort(400,description="user already exists")#aborts in case user email or contact already exists
        
    
    def activate_user(self,email):
        """
        Check if password password is equal to password in database
        """
        try:
            update_query="""
            update users set is_active='t' where email = '{email}' and is_active='f'
            """.format(
                email=email
            )#sql query for inserting new users
            self.cursor.execute(update_query)
            return True
        except Exception as identifier:
            print(str(identifier))
            abort(400,description="Invalid token activation.")#aborts in case user activation fails.


db = Database()
