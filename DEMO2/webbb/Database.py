import mysql.connector as ms
import hashlib
class Database:
    def __init__(self):
        host = "mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com"
        user = "root"
        password = "mypassword"
        db = "mydb"

        self.con = ms.connect(host=host, user=user, password=password, db=db)
        self.cur = self.con.cursor(buffered=True)
    def addUser(self,email,password):

        self.cur.execute("SELECT * from user WHERE email = (%s)", (email,))
        row_count = self.cur.rowcount
        if row_count == 0:
            hashpass = int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16) % 10 ** 8
            self.cur.execute("INSERT INTO user(email,password,balance) VALUES(%s,%s,%s)",(email,hashpass,'1000'))
            self.con.commit()
            return ["Account Created",email,"",1000]
        else:
            return "Account Already Exists, Please Log Out And Try Again"
    def validateLogin(self,email,password):

        self.cur.execute("SELECT * from user WHERE email = (%s)", (email,))
        result = self.cur.fetchall()
        print(result)
        print(email)
        row_count = self.cur.rowcount
        if row_count == 0:
            return ['Account does not exist, Please Log Out And Try Again',result[0][1],result[0][3],result[0][4]]
        hashpass = int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16) % 10 ** 8
        if(int(result[0][2],10) == hashpass):
            #this finds the password element in result, and then converts it to an integer to test against the hashed function
            return ['Successfully logged in',result[0][1],result[0][3],result[0][4]]

        else:
            return ['Wrong Password, Please Go To The Home Tab and Re-confirm Your Information',result[0][1],result[0][3],result[0][4]]

    def deposit(self,email,amt):

        self.cur.execute("SELECT * from user WHERE email = (%s)", (email,))
        result = self.cur.fetchall()
        newbal = float(result[0][4])+float(amt)
        print(result)
        print(email)
        x = str(newbal)
        self.cur.execute('UPDATE user SET balance = (%s) WHERE email = (%s)',(x,email))
        self.con.commit()
        return ["You have deposited $", x]


    def withdraw(self,email,amt):

        self.cur.execute("SELECT * from user WHERE email = (%s)", (email,))
        result = self.cur.fetchall()
        newbal = float(result[0][4])- float(amt)

        if(newbal > 0.0):
            self.cur.execute("UPDATE user SET balance = (%s) WHERE email = (%s)",(str(newbal),email))
            self.con.commit()
            return ["You have withdrawn $",str(newbal)]
        else:
            return ["Sorry, you dont have that much to withdraw",newbal]
    def printStockCode(self):
        self.cur.execute("SELECT stock_code from stock LIMIT 5")
        result = self.cur.fetchall()
        return result
