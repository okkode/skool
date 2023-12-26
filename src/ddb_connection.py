import pymysql
from info import passwrd
from info import username
from info import mydatabase

connection = pymysql.connect(host ='localhost',
                             user = username,
                             password = passwrd,
                             database = mydatabase)

with connection.cursor() as cursor:
        # Read a single record
        #sql = "SELECT * FROM table1"
        sql2 = "INSERT INTO table1 (id, notes) VALUES (3, 'kiscica')"
        cursor.execute(sql2)
        result = cursor.fetchall()
        connection.commit()
        
for record in result:
    print(type(record))
    