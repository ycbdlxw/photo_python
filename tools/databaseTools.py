import sqlite3
from datetime import datetime

def connect_db():
    """
    连接数据库，返回连接对象和游标对象
    """
    conn = sqlite3.connect('photo.db')
    c = conn.cursor()
    return conn, c

def create_photo_main():
    """
    创建photo_main表，如果表不存在
    """
    conn, c = connect_db()
    c.execute('''CREATE TABLE IF NOT EXISTS photo_main
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, fileName TEXT, extentName TEXT, 
                  size INTEGER, DateTimeOriginal DATETIME,
                 createTime DATETIME, updateTime DATETIME)''')
    # 创建photo_person表
    c.execute('''CREATE TABLE IF NOT EXISTS photo_person
             (id INTEGER PRIMARY KEY AUTOINCREMENT, photo_index INTEGER,
             make TEXT, GPS BOOLEAN, person INTEGER, face INTEGER,
             FOREIGN KEY(photo_index) REFERENCES photo_main(id) ON DELETE CASCADE)''')
    

    # 创建photo_info表
    c.execute('''CREATE TABLE IF NOT EXISTS photo_info 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, photo_index INTEGER, mode TEXT,
             make TEXT, GPS BOOLEAN, person INTEGER, face INTEGER, holiday TEXT,title TEXT,
             createTime DATETIME, updateTime DATETIME,
             FOREIGN KEY(photo_index) REFERENCES photo_main(id) ON DELETE CASCADE)''')
    conn.commit()
    conn.close()

def insert_data_photo_main(file_name, extent_name, size, date_time_original):
    """
    向photo_main表插入一条数据
    """
    conn, c = connect_db()
    c.execute("INSERT INTO photo_main (fileName, extentName,  size, DateTimeOriginal, createTime, updateTime) VALUES (?, ?,  ?, ?, ?, ?)",
              (file_name, extent_name,  size, date_time_original, datetime.now(), datetime.now()))
    last_id = c.lastrowid
    conn.commit()
    conn.close()
    return last_id
def insert_photo_info(photo_index, mode, make, GPS):
    """
    向insert_photo_info表插入一条数据
    """
    conn, c = connect_db()
    c.execute("INSERT INTO photo_info (photo_index, mode, make, GPS) VALUES (?, ?, ?, ?)",
              (photo_index, mode, make, GPS))
    conn.commit()
    conn.close()