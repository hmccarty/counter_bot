import sqlite3
import os
import sys
import json

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

def open_db():
    return sqlite3.connect(config["db"], timeout=10)

with open_db() as c:
    c.execute("CREATE TABLE IF NOT EXISTS channels(channel INT, last_count TEXT, last_counter INT, count_type TEXT, score INT)")
    c.execute("CREATE TABLE IF NOT EXISTS members(member INT, score INT)")

class CountingChannel(object):
    @staticmethod
    def get(channel_id: int):
        """
        Fetches a counting channel from the database.
        """
        try:
            with open_db() as c:
                result = c.execute(
                    "SELECT * FROM channels WHERE channel=(?)", (channel_id,)
                ).fetchone()
                if result is not None:
                    return CountingChannel(result[0], result[1], result[2], result[3], result[4])
                else:
                    return None
        except sqlite3.Error as e:
            return None
    
    @staticmethod
    def create(channel_id: int, last_count: str = "", last_counter: int = 0,
        count_type: str = "basic", score: int = 0):
        try:
            with open_db() as c:
                c.execute(
                    "INSERT INTO channels VALUES (?, ?, ?, ?, ?)",
                    (channel_id, last_count, last_counter, count_type, score)
                )
                return CountingChannel(channel_id, last_count, 0, count_type, score)
        except sqlite3.Error as e:
            return None

    def __init__(self, channel_id: int, last_count: str, last_counter: int,
        count_type: str, score: int):
        self.channel_id = channel_id
        self.last_count = last_count
        self.count_type = count_type
        self.score = score
        self.last_counter = last_counter

    def update(self, last_count: str, last_counter: int):
        with open_db() as c:
            c.execute(
                "UPDATE channels SET last_count=(?), last_counter=(?), score=(?) WHERE channel=(?)",
                (last_count, last_counter, self.score + 1, self.channel_id)
            )
            self.last_count = last_count
            self.last_counter = last_counter

class CountingMember(object):
    @staticmethod
    def get_or_create(member_id: int, score: int = 0):
        """
        Fetches a counting member from the database. One will be created
        if it doesn't exist.
        """
        try:
            with open_db() as c:
                result = c.execute(
                    "SELECT * FROM members WHERE member=(?)", (member_id,)
                ).fetchone()
                if result is not None:
                    return CountingMember(result[0], result[1])
                else:
                    c.execute(
                        "INSERT INTO members VALUES (?, ?)", (member_id, 0)
                    )
                    return CountingMember(member_id, score)
        except sqlite3.Error as e:
            return None
    
    @staticmethod
    def get_best(n: int = 10):
        try:
            with open_db() as c:
                results = c.execute(
                    "SELECT * FROM members ORDER BY score desc LIMIT (?)",
                    (n,)
                ).fetchall()

                members = []
                for i in results:
                    members.append(CountingMember(i[0], i[1]))
                return members
        except sqlite3.Error as e:
            return None

    def __init__(self, member_id: int, score: int):
        self.member_id = member_id
        self.score = score

    def update(self, score):
        with open_db() as c:
            c.execute(
                "UPDATE members SET score=(?) WHERE member=(?)",
                (score, self.member_id)
            )
            self.score = score
