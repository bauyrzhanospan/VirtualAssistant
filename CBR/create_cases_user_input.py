import pymysql
import random

con = pymysql.connect(host='0.0.0.0', unix_socket='/tmp/mysql.sock', user=None, passwd=None, db='virtass')
cur = con.cursor()

usertypes = ["adult", "younger", "elder"]
reasons = ["energy", "entertainment", "food", "health", "security", "work"]

start = "INSERT INTO `cases` (`id`, `usertypeIN`, `usertypeOUT`, `reasonIN`, `reasonOUT`, `output`) VALUES ('"

divider = "', '"

k = 1
while k < 40:
    user1 = random.choice(usertypes)
    user2 = random.choice(usertypes)
    reason1 = random.choice(reasons)
    reason2 = random.choice(reasons)

    str1 = str(k) + divider + user1 + divider + user2 + divider + \
           reason1 + divider + reason2 + divider
    k += 1

    value = input(str1)
    str1 = start + str1 + value + "');"
    cur.execute(str1)
    con.commit()

cur.execute('SELECT * FROM `cases`')
print(cur.fetchall())
cur.close()
con.close()
