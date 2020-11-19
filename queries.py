import sqlite3

def query():
    conn = sqlite3.connect("vascularsim.db")
    cursor = conn.cursor()

    conn.execute('CREATE TABLE IF NOT EXISTS BUFFER(id INTEGER PRIMARY KEY, "zero" INTEGER, "one"  INTEGER, "two" INTEGER, "three" INTEGER, "four"  INTEGER, "five"  INTEGER, "six"  INTEGER, "seven"  INTEGER, "eight"  INTEGER , "nine"  INTEGER , "ten"  INTEGER, "eleven"  INTEGER, "twelve"  INTEGER, "thirteen"  INTEGER, "fourteen"  INTEGER) ')
    conn.execute('CREATE TABLE IF NOT EXISTS HPN(id INTEGER PRIMARY KEY, HR INTEGER, PF INTEGER, N INTEGER, FLAG INTEGER, PEP_1 INTEGER, PEP_2 INTEGER, PEP_3 INTEGER, PEP_4 INTEGER, PEP_5 INTEGER, PEP_6 INTEGER, PEP_7 INTEGER, PEP_8 INTEGER, PEP_9 INTEGER, PEP_10 INTEGER, PEP_11 INTEGER, PWV_1 INTEGER, PWV_2 INTEGER, PWV_3 INTEGER, PWV_4 INTEGER, PWV_5 INTEGER, PWV_6 INTEGER, PWV_7 INTEGER, PWV_8 INTEGER, PWV_9 INTEGER, PWV_10 INTEGER, PWV_11 INTEGER)')
    
    #cursor.execute('INSERT INTO HPN("HR","PF","N","FLAG") VALUES(72,450,100,0)')
    for i in range(20000):
        #cursor.execute('INSERT INTO BUFFER("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen") VALUES(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)')
        cursor.execute('UPDATE BUFFER SET "zero" = ?, "one" = ?,"two" = ?, "three" = ?, "four" = ?, "five" = ?, "six" = ?, "seven" = ?, "eight" = ?, "nine" = ?, "ten" = ?, "eleven" = ?, "twelve" = ?, "thirteen" = ?, "fourteen" = ? WHERE id = ?', (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, i+1) )
    
    cursor.execute('UPDATE HPN  SET PF = 450, HR = 60, FLAG = 0, N = 0, PEP_1 = 0,  PEP_2 = 0, PEP_3 = 0, PEP_4 = 0, PEP_5 = 0, PEP_6 = 0, PEP_7 = 0, PEP_8 = 0, PEP_9 = 0, PEP_10 = 0, PEP_11 = 0, PWV_1 = 0, PWV_2 = 0, PWV_3 = 0, PWV_4 = 0, PWV_5 = 0, PWV_6 = 0, PWV_7 = 0, PWV_8 = 0, PWV_9 = 0, PWV_10 = 0, PWV_11 = 0  WHERE id = 1')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    query()