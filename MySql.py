
import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(user='FishTripFinder', password='20080921',
                                  host='localhost',
                                  database='satorentals')

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    if cnx and cnx.is_connected():

        with cnx.cursor() as cursor:

            cursor.execute("select * from rental_quotes")
            rows = cursor.fetchall()

            for rows in rows:
                print(rows)

        cnx.close()
    print("Connected")
    print(cnx)
    cnx.close()


