import os

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

assert "MYSQL_HOST" in os.environ
assert "MYSQL_DBNAME" in os.environ
assert "MYSQL_USER" in os.environ
assert "MYSQL_PASSWORD" in os.environ

print("connecting to: '%s'" % os.environ["MYSQL_HOST"])
print("using: '%s'" % os.environ["MYSQL_DBNAME"])
print("as: '%s':'%s'" % (os.environ["MYSQL_USER"], os.environ["MYSQL_PASSWORD"]))

try:
  connection = mysql.connector.connect(host=os.environ["MYSQL_HOST"],
                                       database=os.environ["MYSQL_DBNAME"],
                                       user=os.environ["MYSQL_USER"],
                                       password=os.environ["MYSQL_PASSWORD"])

  ins_tx = "INSERT INTO txs (txid) VALUES ('1')"
  ins_in = "INSERT INTO ins (txid, input_txid) VALUES ('1', '2')"
  ins_ot = "INSERT INTO outs (txid, address) VALUES ('1', '0')"

  cursor = connection.cursor()
  print("inserting transaction id...")
  result = cursor.execute(ins_tx)
  print("inserting inputs...")
  result = cursor.execute(ins_in)
  print("inserting outputs...")
  result = cursor.execute(ins_ot)
  print("committing...")
  connection.commit()
  print("db transaction complete")
  cursor.close()
except mysql.connector.Error as error:
  print("transaction insert failed: {}".format(error))
finally:
  if (connection.is_connected()):
    connection.close()
    print("connection is closed")
