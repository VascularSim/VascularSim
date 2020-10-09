import sqlite3

conn = sqlite3.connect("vascularsim.db")
cursor = conn.cursor()
#con.execute('CREATE TABLE IF NOT EXISTS BUFFER(id INTEGER PRIMARY KEY, "zero" INTEGER, "one"  INTEGER, "two" INTEGER, "three" INTEGER, "four"  INTEGER, "five"  INTEGER, "six"  INTEGER, "seven"  INTEGER, "eight"  INTEGER , "nine"  INTEGER , "ten"  INTEGER, "eleven"  INTEGER, "twelve"  INTEGER, "thirteen"  INTEGER, "fourteen"  INTEGER) ')
#con.execute('CREATE TABLE IF NOT EXISTS HPN(id INTEGER PRIMARY KEY, HR INTEGER, PF INTEGER, N INTEGER, FLAG INTEGER)')

#print("Sucessfully connected")
#cursor.execute('INSERT INTO HPN("HR","PF","N","FLAG") VALUES(72,450,100,0)')

#for i in range(20000):
    #cursor.execute('INSERT INTO BUFFER("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen") VALUES(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)')
    #cursor.execute('UPDATE BUFFER SET "zero" = ?, "one" = ?,"two" = ?, "three" = ?, "four" = ?, "five" = ?, "six" = ?, "seven" = ?, "eight" = ?, "nine" = ?, "ten" = ?, "eleven" = ?, "twelve" = ?, "thirteen" = ?, "fourteen" = ? WHERE id = ?', (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, i+1) )

#cursor.execute('UPDATE HPN SET PF = 450, FLAG = 0 WHERE id = 1')

i = 1

cursor.execute('SELECT "one" FROM BUFFER WHERE ID BETWEEN ? AND ?', (1, 50)  )
rows = cursor.fetchall()
print(type(rows))

#con.commit()
conn.close()
#print("Sucessfully disconnected")
 