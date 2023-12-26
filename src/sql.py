  
import re
from bs4 import BeautifulSoup
import urllib.request
import ssl
import pymysql
from info import passwrd
from info import username
from location import loc_list



connection = pymysql.connect(host ='localhost',
                             user = username,
                             password = passwrd,
                             database = 'police')
database = 'police',
table_name = 'info',
column_name = 'police_location'


# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Create the SQL query for inserting a list of values into a column
insert_query = f"INSERT INTO {table_name} ({column_name}) VALUES ({', '.join(['%s' for _ in loc_list])})"

# Execute the query with the list of values
cursor.execute(insert_query, loc_list)

# Commit the changes and close the connection
connection.commit()
connection.close()
