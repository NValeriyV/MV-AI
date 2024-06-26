import sqlite3 
import time
import datetime
from datetime import datetime

class DataBase():
    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

    def addbalance(self, balance, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_id,))

    def register_users_id(self, user_id):                                 
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, balance, isDownload) VALUES (?, 1000, 1)", (user_id,))

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

    def set_mode(self, mode):
        with self.connection:
            self.cursor.execute("UPDATE users SET mode= ?", (mode,))

    def amount_audio(self, user_id, video, s, amount_audio):
        with self.connection:
            if s == '+':
                self.cursor.execute("SELECT amount_audio FROM users WHERE user_id = ?", (user_id,))
                balance = self.cursor.fetchone()[0] + video
                self.cursor.execute("UPDATE users SET amount_audio = ? WHERE user_id = ?", (amount_audio, user_id,))
        
    def total_audio(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT amount_audio FROM users WHERE user_id = ?", (user_id))
            user_id = self.cursor.fetchone()[0]

    def isEnable(self, tokens):
        with self.connection:
            self.cursor.execute("UPDATE users SET isEnable WHERE tokens = ?", (tokens))  
            tokens = self.cursor.fetchone()[0] 
            return True
        
    def change_status_token(self, token, isEnable):
        with self.connection:
            self.cursor.execute("UPDATE tokens SET isEnable = ? WHERE token = ?", (isEnable, token,))

    def get_tokens_true(self):
        with self.connection:
            self.cursor.execute("SELECT token FROM tokens WHERE isEnable = ?", (1,))
            return [token[0] for token in self.cursor.fetchall()]
        
    def set_language(self, language, user_id):
        with self.connection:
            self.cursor.execute("UPDATE users FROM language = ? WHERE user_id = ?",(language,user_id,))

    def read_language(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT language FROM users WHERE user_id = ? ",(user_id))

    def set_time(self,user_id, date):
        with self.connection:
            self.cursor.execute("UPDATE users SET time = ? WHERE user_id = ?", (date, user_id,))

    def get_time(self, time_str):
        time = datetime.datetime.strptime(time_str, '%H:%M:%S')
        return time.strftime('%H-%M-%S')

cl = DataBase('test.db')
print(cl.set_time(5500790836, '26-06-24'))


    
