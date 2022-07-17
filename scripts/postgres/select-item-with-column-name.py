import datetime

import psycopg2

try:
    connection = psycopg2.connect(user="postgres",
                                  password="TldhTl1!",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres_db")

    cursor = connection.cursor()
    insert_query = """ INSERT INTO item (item_Id, item_name, purchase_time, price) VALUES (%s, %s, %s, %s)"""
    item_purchase_time = datetime.datetime.now()
    item_tuple = (12, "Keyboard", item_purchase_time, 150)
    cursor.execute(insert_query, item_tuple)
    connection.commit()
    print("1 item inserted successfully")

    # Read PostgreSQL purchase timestamp value into Python datetime
    item_id = 12
    select_query = f'SELECT purchase_time from item where item_id={item_id}'
    print(select_query)
    cursor.execute(select_query)
    purchase_datetime = cursor.fetchone()
    print("Item Purchase date is  ", purchase_datetime[0].date())
    print("Item Purchase time is  ", purchase_datetime[0].time())

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")