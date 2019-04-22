class Database:
    def __init__(self):
        host = "mydb.cwtgu3tqnwx8.us-east-2.rds.amazonaws.com"
        user = "root"
        password = "mypassword"
        db = "mydb"

        self.con = ms.connect(host=host, user=user, password=password, db=db)
        self.cur = self.con.cursor(buffered=True)
    def addUser(self):
        email =  request.args.get('useremail', 0, type=str)
        password = request.args.get('userpassword', 0, type=str)
        self.cur.execute("SELECT * from user WHERE email = (%s)", (email,))
        row_count = self.cur.rowcount
        if row_count == 0:
            hashpass = int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16) % 10 ** 8
            self.cur.execute("INSERT INTO user(email,password,balance) VALUES(%s,%s,%s)",(email,hashpass,'1000'))
            self.con.commit()
            return "Account Created"
        else:
            return "Account Already Exists"
    def validateLogin(self):
        email = request.args.get('loginemail', 0, type=str)
        password = request.args.get('loginpassword', 0, type=str)
        self.cur.execute("SELECT * from user WHERE email = (%s)", (email,))
        result = self.cur.fetchall()
        print(result)
        print(email)
        row_count = self.cur.rowcount
        if row_count == 0:
            return 'Account does not exist'
        hashpass = int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16) % 10 ** 8
        if(int(result[0][2],10) == hashpass):
            #this finds the password element in result, and then converts it to an integer to test against the hashed function
            return 'Successfully logged in'

        else:
            return 'wrong password'
    def AccountInfo(self):
        self.cur.execute("SELECT * from user WHERE email = (%s)", (email,))
        result = self.cur.fetchall()
        email = result[0][1]
        balance = result[0][4]
        array = [email, balance]
        #this returns the email and the balance, needs to be further tweaked for portfolio but ill take care of that in a bit
        return jsonify(array)




    def printStockCode(self):
        self.cur.execute("SELECT stock_code from stock LIMIT 5")
        result = self.cur.fetchall()
        return result