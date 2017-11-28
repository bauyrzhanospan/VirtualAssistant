import sqlite3
import random

con = sqlite3.connect('./database/db')
cur = con.cursor()

# cur.execute('CREATE TABLE preferences (id INTEGER PRIMARY KEY, User VARCHAR(20), Usertype VARCHAR(20), Usertype_level '
#             'INTERGER, Energy INTERGER, Entertainment INTERGER, Food INTERGER, Health INTERGER, Security INTERGER, '
#             'Work INTERGER)')
# con.commit()


usertypes = ["adult", "younger", "older"]
users = ["Father", "Mother", "Grandpa", "Son"]

str1 = 'INSERT INTO preferences (id, Usertype_changer, Reason_changer, Usertype_before, Reason_before, Reason) VALUES(0, ' \
       '"adult", "Health", "younger","Work", 1) '
start = 'INSERT INTO preferences (id, User, Usertype, Usertype_level, Energy, Entertainment, Food, Health, Security, Work) VALUES('

k = 0
for el in users:
    str1 = str(k) + ', "' + str(el) + '", "' + random.choice(usertypes) + '",1,1,1,1,1,1,1'
    k += 1
    str1 = start + str1 + ')'
    cur.execute(str1)
    con.commit()

print(cur.lastrowid)

cur.execute('SELECT * FROM cases')
print(cur.fetchall())
con.close()
