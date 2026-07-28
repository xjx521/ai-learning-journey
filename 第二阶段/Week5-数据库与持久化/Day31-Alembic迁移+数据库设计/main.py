import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()  # 创建游标对象
cursor.execute("SELECT name FROM sqlite_master WHERE type ='table'")
print(cursor.fetchall())
conn.close()
