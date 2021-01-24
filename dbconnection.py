import psycopg2


class Connection:

    def __init__(self, host=None, service=None, user=None, passwd=None):
        self.host = host        
        self.service = service
        self.user = user
        self.passwd = passwd        


    def execute_statement(self, statement):
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute(statement)
        mydb.commit()


    def connect(self):
        mydb = psycopg2.connect(
                host="161.35.60.197",
                database="tcs7",
                user="modulo4",
                password="modulo4")                      
        return mydb

    def close(self): 
        self.mydb.close()
