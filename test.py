import sqlite3
import random

con = sqlite3.connect('./database/db')
cur = con.cursor()

cur.execute('CREATE TABLE cases (id INTEGER PRIMARY KEY, Usertype_changer VARCHAR(20), Reason_changer VARCHAR(20), '
            'Usertype_before VARCHAR(20), Reason_before VARCHAR(20), Reason BOOLEAN)')
con.commit()

k = list(range(0, 40))
usertypes = ["adult", "younger", "older"]
reasons = ["Energy", "Entertainment", "Food", "Health", "Secuirity", "Work"]
str1 = 'INSERT INTO cases (id, Usertype_changer, Reason_changer, Usertype_before, Reason_before, Reason) VALUES(0, ' \
       '"adult", "Health", "younger","Work", 1) '
start = 'INSERT INTO cases (id, Usertype_changer, Reason_changer, Usertype_before, Reason_before, Reason) VALUES('

for el in k:
    str1 = str(el) + ', "' + random.choice(usertypes) + '", "' + random.choice(reasons) + '", "' + random.choice(
        usertypes) + '", "' + random.choice(reasons) + '", '

    str1 = start + str1 + str(input(str1)) + ')'
    cur.execute(str1)
    con.commit()

print(cur.lastrowid)

cur.execute('SELECT * FROM cases')
print(cur.fetchall())
con.close()
