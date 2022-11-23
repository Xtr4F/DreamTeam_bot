import sqlite3

#Раота с БД
class botDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

#Проверка на наличее юзера в БД
    def user_exists(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
            return bool(len(result.fetchall()))

    def add_user(self, user_id):
        with self.conn:
            self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
            try:
                self.cursor.execute("INSERT INTO `users_stats` (`user_id`) VALUES (?)", (user_id,))
                self.cursor.execute("INSERT INTO `moderation` (`user_id`) VALUES (?)", (user_id,))
            except:
                pass

    def add_first_name(self, first_name, user_id):
        with self.conn:
            return self.cursor.execute("UPDATE users SET first_name = ? WHERE user_id = ?", (first_name, user_id,))

    def add_last_name(self, last_name, user_id):
         with self.conn:
            return self.cursor.execute("UPDATE users SET last_name = ? WHERE user_id = ?", (last_name, user_id,))

    def add_user_tag(self, user_tag, user_id):
        with self.conn:
            return self.cursor.execute("UPDATE users SET user_tag = ? WHERE user_id = ?", (user_tag, user_id,))

    def add_join_date(self, join_date, user_id):
        with self.conn:
            return self.cursor.execute("UPDATE users SET join_date = ? WHERE user_id = ?", (join_date, user_id,))

    def get_all_users(self, user_id):
        with self.conn:
            if user_id != None:
                user_data = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
                return user_data
            else:
                user_data = self.cursor.execute("SELECT * FROM users").fetchall()
                return user_data


    def get_all_users_stats(self, user_id):
        with self.conn:
            if user_id != 0:
                user_data = self.cursor.execute("SELECT * FROM users_stats WHERE user_id = ?", (user_id,)).fetchone()
                return user_data
            else:
                user_data = self.cursor.execute("SELECT * FROM users_stats").fetchall()
                return user_data


    def get_all_moderation(self, user_id):
        with self.conn:
            user_data = self.cursor.execute("SELECT * FROM `moderation` WHERE `user_id` = ?", (user_id,)).fetchone()
            return user_data


    def get_all_configs(self):
        with self.conn:
            user_data = self.cursor.execute("SELECT * FROM `bot_configs`").fetchone()
            return user_data

    def update_date(self, date):
        with self.conn:
            return self.cursor.execute("UPDATE bot_configs SET date_now = ?", (date,))

    def set_messages(self, user_id, messages, day_messages, week_messages, month_messages):
        with self.conn:
            if day_messages != 0:
                self.cursor.execute("UPDATE users_stats SET day_messages = ? WHERE user_id = ?", (day_messages, user_id,))
            if week_messages != 0:
                self.cursor.execute("UPDATE users_stats SET week_messages = ? WHERE user_id = ?", (week_messages, user_id,))
            if month_messages != 0:
                self.cursor.execute("UPDATE users_stats SET month_messages = ? WHERE user_id = ?", (month_messages, user_id,))
            if messages != 0:
                self.cursor.execute("UPDATE users_stats SET messages = ? WHERE user_id = ?", (messages, user_id,))
            return


    def change_role(self, user_id, role):
        with self.conn:
            self.cursor.execute("UPDATE moderation SET role = ? WHERE user_id = ?", (role, user_id,))
            return

    def get_by_username(self, username):
        with self.conn:
            return self.cursor.execute("SELECT * FROM users WHERE user_tag = ?", (username,)).fetchall()

    def change_reputation(self, user_id, operation):
        with self.conn:
            if operation == '+':
                return self.cursor.execute("UPDATE users_stats SET reputation = reputation + 1 WHERE user_id = ?", (user_id,))
            elif operation == '-':
                return self.cursor.execute("UPDATE users_stats SET reputation = reputation - 1 WHERE user_id = ?", (user_id,))
            return





