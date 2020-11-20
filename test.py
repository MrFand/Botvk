import sqlite3
def drop():
	connection = sqlite3.connect('Database.db')
	cursorObj = connection.cursor()

	cursorObj.execute('DROP table if exists employees')

	connection.commit()

connection = sqlite3.connect('Database.db')
cursorObj = connection.cursor()
cursorObj.execute('SELECT user_id,mode,word,blank,right_letter,letter, error FROM employees')
rows = cursorObj.fetchall()
print(rows)
