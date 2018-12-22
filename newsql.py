import sqlite3

conn = sqlite3.connect('shoplog')
c =	conn.cursor()
c.execute('CREATE VIRTUAL TABLE act USING FTS5 (topic,post,category)')
