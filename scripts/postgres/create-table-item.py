import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="postgres",
                                  password="TldhTl1!",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres_db")

    cursor = connection.cursor()
    # SQL query to create a new table
    create_table_query = '''CREATE TABLE item ( 
	item_id serial NOT NULL PRIMARY KEY, 
	item_name VARCHAR (100) NOT NULL, 
	purchase_time timestamp NOT NULL,
	price INTEGER NOT NULL );'''
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")