import mysql.connector
from .config import mysql_db, mysql_host, mysql_pass, mysql_port, mysql_timeout, mysql_user

class MySQL():
    def __init__(self):
        self.mydb = mysql.connector.connect(
		    user = mysql_user,
		    password = mysql_pass,
		    host = mysql_host,
		    port = mysql_port,
		    database = mysql_db,
		    connect_timeout=mysql_timeout
		)
        
        self.mycursor = self.mydb.cursor()
        
    def query_once(self, query):
        self.mycursor.execute(query)
        return self.mycursor.fetchone()

    def query_all(self, query):
        self.mycursor.execute(query)
        return self.mycursor.fetchall()
    
    def query_update(self, query):
        pass
        
class Account():
    def __init__(self):
        self.mysql = MySQL()
        
    def login(self, username, password):
        query = f"SELECT acc_id, acc_username, acc_password FROM account WHERE acc_username = '{username}' AND acc_password = '{password}'"
        data = self.mysql.query_once(query)
        
        code = 200 if data else 204
        return data, code
    
    def register(self):
        pass
    
    def update(self):
        pass
    
    def delete(self):
        pass
