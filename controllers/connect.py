import requests

import psycopg2
import psycopg2.extras
from flask import jsonify, abort
from flask_jwt_extended import create_access_token, get_jwt_identity



import datetime
import time
from  uuid import uuid4

from controllers.emails import Emails
from controllers.extensions import task_after_function
from models.constants import DATABASE_URL, MM_URL, FL_KEY, FRONTEND_URL

currency = 'UGX'
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
    
    def __del__(self): 
        """
        Close database connection
        """
        self.cursor.close()


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
                email varchar(250) not null,
                name varchar(250) not null,
                contact varchar(250) not null,
                time TIMESTAMP NOT NULL,
                date_booked_for TIMESTAMP NOT NULL,
                payment_type varchar(25) check (payment_type in ('cash on arrival', 'bank transfer/visa', 'mobile money')) DEFAULT 'cash on arrival',
                payment_status varchar(25) check (payment_status in ('pending', 'successful', 'failed','expired')) DEFAULT 'pending',
                payment_id VARCHAR (250) NULL,
                filled_status varchar(25) check (filled_status in ('pending', 'utilized', 'canceled')) DEFAULT 'pending'
            );
            CREATE TABLE IF NOT EXISTS room_categories(
                room_id SERIAL PRIMARY KEY,
                number INT NOT NULL,
                price INT NOT NULL,
                name VARCHAR (250) NOT NULL,
                time TIMESTAMP NOT NULL,
                description VARCHAR (250) NOT NULL,
                room_url VARCHAR (250) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS mobile_payments(
                id SERIAL PRIMARY KEY,
                amount INT NOT NULL,
                price INT NOT NULL,
                user_id INT NOT NULL,
                tx_ref VARCHAR (250) NOT NULL unique,
                phone_number VARCHAR (250) NOT NULL,
                time TIMESTAMP NOT NULL
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
        INSERT INTO room_categories (number, price, name,  time, description, room_url)
        VALUES (40, 40000, 'Master Suite', now(), 'Spacious self contained room with double bed, Satelite TV, state of the art washrooms, 24/7 room service, breakfast included.', 'https://drive.google.com/uc?export=view&id=1ulWMbY04h1zwx4X9hekAonm60RDcux00'),
               (3, 60000, 'Presidential Suite', now(), 'Mini Gym within highly spacious self contained room with double bed, Satelite TV, state of the art washrooms, 24/7 room service, breakfast included.','https://drive.google.com/uc?export=view&id=1gIqDMudg670RT72n_-XnIcKNSF_GBGay'),
               (200, 1000, 'Normal Suite', now(), 'Self contained room with single bed, Satelite TV, breakfast included.','https://drive.google.com/uc?export=view&id=1yPBKJ5hypHjFU15m6AVO9KlBDSodCDfX'),
               (100, 3000, 'Couple Suite', now(), 'Self contained room with double bed, Satelite TV, breakfast included.','https://drive.google.com/uc?export=view&id=1BQ0OOR2cBtuujdTiNdUAR0UunoOWjvsu');
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
        INSERT INTO users (surname,othernames,email,contact,password,date_created,admin,is_active) 
        values ('Admin1','Saed','i-sendit@gmail.com','07888392838','doNot2114',now(),'t', 't');
        INSERT INTO users (surname,othernames,email,contact,password,date_created,admin, is_active) 
        values ('Test','User','meKendit@gmail.com','0788892838','ddwoNot2114',now(),'f', 't');
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
        user = self.get_from_users('user_id,password,surname,email,contact,admin',email,"and password = '"+password+"' and is_active=true")
        contact = user.get('contact')
        surname= user.get('surname')
        admin = user.get('admin')
        access_token = create_access_token(
            identity={
            'surname':surname,
            'user_id':user.get('user_id'),
            'admin':admin,
            'email':email,
            'contact':contact
            },
            expires_delta=datetime.timedelta(days=40)
        )
        # print(db_password.get('password'))
        return {'token': access_token,'email':email,'username':surname,'contact': contact, 'admin':admin} 
    
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


    def insertPayment(self,data):
        """
        Check if password password is equal to password in database
        """



        user_info = get_jwt_identity()
        user_id = user_info.get('user_id')
        email =data['email']= user_info.get('email')
        type_id = data.get('type_id')
        type_name = data.get('type_name')
        amount =data['amount']= int(data.get('price'))*int(data.get('rooms'))
        rooms = data.get('rooms')
        price= data.get('price')
        name=data['fullname']= data.get('name')
        date_booked_for = data.get('date_booked_for')
        phone_number = data.get('phone_number')
        payment_id = data['tx_ref']='mobilemoney_'+str(uuid4()).replace('-', '')
        print(amount)
        
        insert_query="""
        INSERT INTO bookings (user_id, type_id, type_name, price, rooms,email, contact, name, total, time, date_booked_for, payment_type,  payment_id) 
        values ('{user_id}','{type_id}','{type_name}','{price}','{rooms}','{email}','{phone_number}','{name}','{amount}',now(),'{date_booked_for}','mobile money','{payment_id}');
        INSERT INTO mobile_payments (amount, price, tx_ref,user_id,phone_number, time ) 
        values ('{amount}','{price}','{payment_id}','{user_id}','{phone_number}',now());
        """.format(
            amount=amount,
            user_id=user_id,
            email=email,
            name=name,
            type_id=type_id,
            type_name=type_name, 
            rooms=rooms,
            price=price,
            date_booked_for=date_booked_for,
            phone_number=phone_number,
            payment_id=payment_id
        )#sql query for inserting new users
        
        try:
            data['redirect_url']= FRONTEND_URL+'/success'
            print(MM_URL)
            print(data['redirect_url'])
            response = requests.post(url=MM_URL,data=data, headers={'Authorization': 'Bearer '+FL_KEY})
            task_after_function(
                target=Database.execute_after_request,
                args=[insert_query,],
                daemon=True
            ).start()

            return (response.json())['meta']['authorization']['redirect']
            # return insert_query
        except Exception as identifier:
            print(str(identifier))

            abort(400,description=str(identifier))#aborts in case user email or contact already exists
        
    
    
    def get_all_transactions(self):
        """
        Get all user transactions
        """
        user_info=get_jwt_identity()
        user_id = user_info.get('user_id')
        is_admin = user_info.get('admin')
        transactions_query="""
        select users.surname||' ' || users.othernames as name, bookings.booking_id,
        users.contact,
        bookings.date_booked_for, bookings.total, bookings.rooms, bookings.type_name,
        bookings.payment_status, bookings.filled_status, users.email
        from users join bookings on
        bookings.user_id=users.user_id
        """
        if not is_admin:
            transactions_query+=" and users.user_id='{user_id}'".format(user_id=user_id)
        return self.execute_query(transactions_query)


    def get_accomodation_categories(self):
        """
        Get all user transactions
        """
        transactions_query="""
        select room_categories.* from room_categories
        """
        return self.execute_query(transactions_query)



    def get_bookings_stats(self):
        """
        Get booking stats for line chart
        """
        if (get_jwt_identity()).get('admin'):
            stats_query="""
            SELECT time::timestamp::date as date, 
            cast(sum(total::decimal) as integer) as "money" 
            FROM "bookings"
            WHERE 
            bookings.payment_status='successful'
            GROUP BY time::timestamp::date
            ORDER BY time::timestamp::date DESC
            """
            return self.execute_query(stats_query)
        abort(401, description="unauthorized")
        

    @staticmethod# so that ts callable without initializing the class
    def update_payment(status,payment_id):
        """Update payment
        """
        try:
            update_query="""update bookings set payment_status='{status}'
            where payment_id = '{payment_id}' and payment_status!='successful'
            returning bookings.email
            """.format(
                status=status,
                payment_id=payment_id
            )  
            execution=Database()
            user = execution.execute_query(update_query)[0]
            email = user.get('email')
            amount = user.get('amount')
            print('successful update')
            Emails.send_purchase_email(email,amount)
        except Exception as error:
            print('failed to udpate transaction\n')
            print(str(error))
        
    
    @staticmethod# so that ts callable without initializing the class
    def execute_after_request(query):
        """
        executes query after request response is returned.
        The function also logs any issues that may occur during execution
        params: 
            :query (str): query that will be run
        returns:
            :None
        """
        try:
            connection = Database()
            execution = connection.cursor.execute(query)
            print('successful execution after request')
        except Exception as error:
            print('Error on execution after request\n',str(error))



db = Database()
