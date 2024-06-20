import sqlite3 

class DataBase():
    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

    def addbalance(self, balance, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_id,))

    def register_users_id(self, user_id):                                 
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, balance, isDownload) VALUES (?, 0, 1)", (user_id,))

    def get_balance(self, user_id):
            self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()[0]
            return result

    def write_balance(self, user_id, staff):
        with self.connection:
            self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
            balance = self.cursor.fetchone()[0] + staff
            self.cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_id,))

    def or_balance(self, user_id, sum, m):
        with self.connection:
            if m == '+':
                self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
                balance = self.cursor.fetchone()[0] + sum
                self.cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_id,))
            elif m == '-':
                self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
                balance = self.cursor.fetchone()[0] - sum
                self.cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_id,))          

    def update_subscribe(self, user_id, podpiska):
        with self.connection:
            self.cursor.execute("UPDATE users SET podpiska = ? WHERE user_id = ?", (podpiska, user_id,))
        
    def true_user_id(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
            try:
                self.cursor.fetchone()[0]
                return True
            except:
                return False
    
    def isDownload(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT isDownload FROM users WHERE user_id = ?", (user_id,))
            try:
                self.cursor.fetchone()[0]
                return True
            except:
                return False
            
    def check_balance(self, balance, amount_symbol, user_id):
        with self.connection:
            if balance >= amount_symbol / 10:
                self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
                balance = self.cursor.fetchone()[0] 
                return True
            else:
                return False
    
    
